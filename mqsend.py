#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.37.94', port=5672))
channel = connection.channel()

channel.basic_publish(exchange='piracyAnalysis',
                      routing_key='',
                      body="hello")

print(" [x] Sent 'Hello World!'")
connection.close()
