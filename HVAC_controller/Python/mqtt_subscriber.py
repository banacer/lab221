import pika
import sys

__mqtt_host = '172.26.50.120'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=__mqtt_host))
channel = connection.channel()

queue_name = sys.argv[1]
#result = channel.queue_declare(queue=queue_name,exclusive=True)

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,queue=queue_name,no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
