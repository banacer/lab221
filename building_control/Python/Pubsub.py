import pika
import sys

__mqtt_host = '172.26.50.120'
__mqtt_port = 1883

def printit(ch, method, properties, body):
    """
    prints the body message. It's the default callback method
    :param ch: keep null
    :param method: keep null
    :param properties: keep null
    :param body: the message
    :return:
    """
    print(" [x] %r" % body)

def sub(queue_name,callback=printit):
    """
    Connects to queue
    :param queue_name: the queue to subscribe to
    :param callback: optional callback function
    :return:
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=__mqtt_host))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(callback,queue=queue_name,no_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def pub(queue_name,message):
    """
    publish to queue
    :param queue_name: queue name
    :param message: message
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=__mqtt_host))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='',routing_key=queue_name,body=message)
    print" [x] Sent %s" % message
    connection.close()