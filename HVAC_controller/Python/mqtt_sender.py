
import pika
import sys
import json

def send(queue_name,message):
    """

    :param queue_name: queue name
    :param message: message
    """
    __mqtt_host = '172.26.50.120'
    __mqtt_port = 1883
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=__mqtt_host))
    channel = connection.channel()

    #channel.queue_declare(queue=queue_name)

    channel.basic_publish(exchange='',routing_key=queue_name,body=message)
    print" [x] Sent %s" % message
    connection.close()