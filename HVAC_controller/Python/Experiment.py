
from sender import Sender
from multiprocessing import Process
from time import sleep
import json
import pika


class Experiment:
    rabbitmq_host = '172.26.50.120'
    __rabbitmq_host = '172.26.50.120'
    __rabbitmq_port = 1883
    __arduino_serial = '/dev/ttyUSB0'
    __arduino_addr = 0x2211

    def __init__(self,topic):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.__rabbitmq_host))
        self.channel = self.connection.channel()
        self.topic_in = topic + '/in'
        self.topic_out = topic + '/out'
        self.channel.queue_declare(queue=self.topic_in)
        self.channel.queue_declare(queue=self.topic_out)
        self.channel.basic_qos(prefetch_count=1)
        self.sender = Sender(self.__arduino_serial, self.__arduino_addr)

    def push_to_queue(self, obj):
        print 'pushing to queue ',self.topic_out, ' val ', obj
        self.channel.basic_publish(exchange='',
                              routing_key=self.topic_out,
                              body=obj,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))

    def subscribe_to_queue(self, q_name, func):
        self.channel.basic_consume(func, queue=q_name, no_ack=True)


    @staticmethod
    def execute_strategy(ch, method, properties, body):
        print 'yes we received',body
        obj = json.loads(body)
        strategy_num = obj['num']
        temp_preference = obj['temp']

        if strategy_num == 1:
            exp = Experiment('strategy1')
            exp.__strategy1(temp_preference)
        elif strategy_num == 2:
            exp = Experiment('strategy2')
            exp.__strategy2(temp_preference)
        elif strategy_num == 3:
            exp = Experiment('strategy3')
            exp.__strategy3(temp_preference)
        elif strategy_num == 4:
            exp = Experiment('strategy4')
            exp.__strategy4(temp_preference)
        else:
            print 'Strategy not recognized'


    def __strategy1(self, temp_preference):
        print 'strategy 1 running!'
        #set the room temperature to 4 degrees higher
        initial_change = 4
        self.adjust_room(initial_change,self)
        self.subscribe_to_queue(self.topic_in, self.__handle_change)


    @staticmethod
    def __strategy2(temp_preference):
        pass

    @staticmethod
    def __strategy3(temp_preference):
        pass

    @staticmethod
    def __strategy4(temp_preference):
        pass

    def __monitor_loading(self,start, target, mqtt):
        print 'monitor loading!!'
        while start != target:
            current = self.sender.getTemp()
            loading  = float(current - start) / float(target - start) * 100
            self.push_to_queue(str(loading))
            sleep(10)

    def __handle_change(self,ch, method, properties, body):
        change = float(body)
        self.adjust_room(change)

    def adjust_room(self,change,mqtt):
        if change == 0:  # experiment done
            self.__stop(mqtt)
        current_temp = mqtt.sender.getTemp()
        target_temp = current_temp + change
        p = Process(target=mqtt.sender.set_temp, args=(target_temp,))  # create thread to execute process
        print 'you are here!'
        self.__monitor_loading(current_temp, target_temp, mqtt)
        # Process(target=MQTT.__monitor_loading,args=(current_temp,target_temp,userdata,))


    def __stop(self):

        temp = self.sender.getTemp()
        self.push_to_queue(self.topic_out,temp) # send final temperature value at end of experiment

connection = pika.BlockingConnection(pika.ConnectionParameters(host=Experiment.rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue='strategy')
channel.basic_consume(Experiment.execute_strategy,queue='strategy',no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

