from django.test import override_settings
from rest_framework.exceptions import ValidationError
from logpipe import Consumer
from logpipe.exceptions import InvalidMessageError, UnknownMessageVersionError
from logpipe.tests.common import BaseTest, TOPIC_STATES
from moto import mock_kinesis
import boto3


LOGPIPE = {
    'OFFSET_BACKEND': 'logpipe.backend.kinesis.ModelOffsetStore',
    'PRODUCER_BACKEND': 'logpipe.backend.kinesis.Producer',
    'CONSUMER_BACKEND': 'logpipe.backend.kinesis.Consumer',
}


class ConsumerTest(BaseTest):
    @override_settings(LOGPIPE=LOGPIPE)
    @mock_kinesis
    def test_normal_consume(self):
        self.make_stream_with_record('NY', b'json:{"message":{"code":"NY","name":"New York"},"version":1,"type":"us-state"}')

        # Test the values sent to our serializer match the message
        def save(ser):
            self.assertEqual(ser.validated_data['code'], 'NY')
            self.assertEqual(ser.validated_data['name'], 'New York')
        FakeStateSerializer = self.mock_state_serializer(save)

        # Consume a message
        consumer = Consumer(TOPIC_STATES)
        consumer.register(FakeStateSerializer)

        consumer.run(iter_limit=10)
        self.assertEqual(self.serializers['state'].save.call_count, 1)
        consumer.run(iter_limit=10)
        self.assertEqual(self.serializers['state'].save.call_count, 1)


    @override_settings(LOGPIPE=LOGPIPE)
    @mock_kinesis
    def test_multi_shard_consume(self):
        # Send a bunch of messages to a bunch of shards
        key = 1
        value = b'json:{"message":{"code":"NY","name":"New York"},"version":1,"type":"us-state"}'
        client = self.make_stream_with_record(str(key), value, shard_count=20)
        for i in range(100):
            key += 1
            client.put_record(
                StreamName=TOPIC_STATES,
                Data=value,
                PartitionKey=str(key))

        # Test the values sent to our serializer match the message
        test = { 'i': 0 }

        def save(ser):
            self.assertEqual(ser.validated_data['code'], 'NY')
            self.assertEqual(ser.validated_data['name'], 'New York')
            test['i'] += 1

        FakeStateSerializer = self.mock_state_serializer(save)

        # Consume messages. Log should have 101 messages in it now.
        consumer = Consumer(TOPIC_STATES)
        consumer.register(FakeStateSerializer)
        consumer.run(iter_limit=2000)
        self.assertEqual(FakeStateSerializer.call_count, 101)
        self.assertEqual(test['i'], 101)


    @override_settings(LOGPIPE=LOGPIPE)
    @mock_kinesis
    def test_missing_version(self):
        self.make_stream_with_record('NY', b'json:{"message":{"code":"NY","name":"New York"}}')

        consumer = Consumer(TOPIC_STATES, consumer_timeout_ms=500)
        with self.assertRaises(InvalidMessageError):
            consumer.run(iter_limit=1)


    @override_settings(LOGPIPE=LOGPIPE)
    @mock_kinesis
    def test_missing_message(self):
        self.make_stream_with_record('NY', b'json:{"version":1}')
        consumer = Consumer(TOPIC_STATES, consumer_timeout_ms=500)
        with self.assertRaises(InvalidMessageError):
            consumer.run(iter_limit=1)


    @override_settings(LOGPIPE=LOGPIPE)
    @mock_kinesis
    def test_unknown_version(self):
        self.make_stream_with_record('NY', b'json:{"message":{"code":"NY","name":"New York"},"version":2,"type":"us-state"}')
        FakeStateSerializer = self.mock_state_serializer()

        consumer = Consumer(TOPIC_STATES, consumer_timeout_ms=500)
        consumer.register(FakeStateSerializer)
        with self.assertRaises(UnknownMessageVersionError):
            consumer.run(iter_limit=1)
        self.assertEqual(FakeStateSerializer.call_count, 0)


    @override_settings(LOGPIPE=LOGPIPE)
    @mock_kinesis
    def test_invalid_message(self):
        self.make_stream_with_record('NY', b'json:{"message":{"code":"NYC","name":"New York"},"version":1,"type":"us-state"}')
        FakeStateSerializer = self.mock_state_serializer()

        consumer = Consumer(TOPIC_STATES, consumer_timeout_ms=500)
        consumer.register(FakeStateSerializer)
        with self.assertRaises(ValidationError):
            consumer.run(iter_limit=1)
        self.assertEqual(FakeStateSerializer.call_count, 1)
        self.assertEqual(self.serializers['state'].save.call_count, 0)


    def make_stream_with_record(self, key, value, shard_count=1):
        client = boto3.client('kinesis', region_name='us-east-1')
        client.create_stream(
            StreamName=TOPIC_STATES,
            ShardCount=shard_count)
        client.put_record(
            StreamName=TOPIC_STATES,
            Data=value,
            PartitionKey=key)
        return client
