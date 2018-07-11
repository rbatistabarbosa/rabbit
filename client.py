#!/usr/bin/env python
import pika
import uuid
import json

class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='35.199.98.99'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, order):
        order_str = json.dumps(order)
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=order_str)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

fibonacci_rpc = FibonacciRpcClient()

order = {'id': 1, 'side': 'buy', 'price': 2.1, 'quantity': 2, 'symbol': 'USD'}
print(" [x] Sending order {}".format(order))
response = fibonacci_rpc.call(order)
print(" [.] Got %r" % response)
