from django.db import transaction
from .exceptions import InvalidMessageError, UnknownMessageTypeError, UnknownMessageVersionError
from .backend import get_offset_backend, get_consumer_backend
from .format import parse
from . import settings
import itertools
import logging
import time


logger = logging.getLogger(__name__)


class Consumer(object):
    _client = None

    def __init__(self, topic_name, **kwargs):
        self.consumer = get_consumer_backend(topic_name, **kwargs)
        self.serializer_classes = {}


    def commit(self, message):
        get_offset_backend().commit(self.consumer, message)


    def register(self, serializer_class):
        message_type = serializer_class.MESSAGE_TYPE
        version = serializer_class.VERSION
        if message_type not in self.serializer_classes:
            self.serializer_classes[message_type] = {}
        self.serializer_classes[message_type][version] = serializer_class


    def run(self, iter_limit=0):
        i = 0
        for message, serializer in self:
            with transaction.atomic():
                serializer.save()
                self.commit(message)
            i += 1
            if iter_limit > 0 and i >= iter_limit:
                break


    def __iter__(self):
        return self


    def __next__(self):
        message = next(self.consumer)

        info = (message.key, message.topic, message.partition, message.offset)
        logger.debug('Received message with key "%s" from topic "%s", partition "%s", offset "%s"' % info)

        # Wait?
        timestamp = getattr(message, 'timestamp', None) or (time.time() * 1000)
        lag_ms = (time.time() * 1000) - timestamp
        logger.debug("Message lag is %sms" % lag_ms)
        wait_ms = settings.get('MIN_MESSAGE_LAG_MS', 0) - lag_ms
        if wait_ms > 0:
            logger.debug("Respecting MIN_MESSAGE_LAG_MS by waiting %sms" % wait_ms)
            time.sleep(wait_ms / 1000)
            logger.debug("Finished waiting")

        serializer = self._unserialize(message)
        return message, serializer


    def __str__(self):
        return '<logpipe.consumer.Consumer topic="%s">' % self.consumer.topic_name


    def _unserialize(self, message):
        data = parse(message.value)
        if 'type' not in data:
            raise InvalidMessageError('Received message missing missing a top-level "type" key.')
        if 'version' not in data:
            raise InvalidMessageError('Received message missing missing a top-level "version" key.')
        if 'message' not in data:
            raise InvalidMessageError('Received message missing missing a top-level "message" key.')

        message_type = data['type']
        if message_type not in self.serializer_classes:
            raise UnknownMessageTypeError('Received message with unknown type "%s" in topic %s' % (message_type, message.topic))

        version = data['version']
        if version not in self.serializer_classes[message_type]:
            raise UnknownMessageVersionError('Received message of type "%s" with unknown version "%s" in topic %s' % (message_type, version, message.topic))

        serializer_class = self.serializer_classes[message_type][version]

        instance = None
        if hasattr(serializer_class, 'lookup_instance'):
            instance = serializer_class.lookup_instance(**data['message'])
        serializer = serializer_class(instance=instance, data=data['message'])
        serializer.is_valid(raise_exception=True)
        return serializer



class MultiConsumer(object):
    def __init__(self, *consumers):
        self.consumers = consumers

    def run(self):
        for consumer in itertools.cycle(self.consumers):
            consumer.run(iter_limit=1)
