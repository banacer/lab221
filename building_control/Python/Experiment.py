'''
This module implements the 4 strategies needed for the comfort experiment.
Just call run()
'''

from threading import Thread, Lock
from time import sleep
import json

import pika
import SerialSender

class Experiment(object):
    '''
    Class implements the experiment functions needed
    '''
    rabbitmq_host = '172.26.50.120'
    __rabbitmq_port = 1883
    __arduino_serial = '/dev/ttyACM1'
    __arduino_addr = 0x2211
    __mutex = Lock()
    __sender = SerialSender.SerialSender(__arduino_serial)

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        self.topic_in = ''
        self.topic_out = ''
        #self.sender = Sender(self.__arduino_serial, self.__arduino_addr)

    def push_to_queue(self, obj):
        """
        Push object to queue
        :param obj: the object to send
        :return: nothing
        """
        self.channel.basic_publish(exchange='',
                                   routing_key=self.topic_out, body=obj,
                                   properties=pika.BasicProperties(delivery_mode=2,))

    def subscribe_to_queue(self, q_name, func):
        """
        Subscribe to queue
        :param q_name: the queue to subscribe to
        :param func: the callback function
        :return: nothing
        """
        self.channel.basic_consume(func, queue=q_name, no_ack=True)

    def __init_queues(self, num):
        """
        Initialize the strategy<num>/in and strategy<num>/out
        :param num: the strategy number
        :return:  nothing
        """
        self.topic_in = 'strategy%d/in' % num
        self.topic_out = 'strategy%d/out' % num
        self.channel.queue_declare(queue=self.topic_in)
        self.channel.queue_declare(queue=self.topic_out)

    def strategy1(self, temp_preference):
        """
        executes strategy 1
        :param temp_preference: the temperature preference
        """
        # initializing queues
        self.__init_queues(1)
        #set the room temperature to 4 degrees higher
        initial_change = 4
        current_temp = Experiment.__sender.get_temp()
        change = temp_preference + initial_change - current_temp
        self.adjust_room(change)
        self.subscribe_to_queue(self.topic_in, self.__handle_change)


    def strategy2(self, temp_preference):
        """
        executes strategy 2
        :param temp_preference: the temperature preference
        """
        print 'strategy 2 running!'

        #initializing queues
        self.__init_queues(2)
        # set the room temperature to 4 degrees lower
        initial_change = -4
        current_temp = Experiment.__sender.get_temp()
        change = temp_preference + initial_change - current_temp
        self.adjust_room(change)
        self.subscribe_to_queue(self.topic_in, self.__handle_change)

    def strategy3(self, temp_preference):
        """
        executes strategy 3
        :param temp_preference: the temperature preference
        """

        #initializing queues
        self.__init_queues(3)
        # set the room temperature to 4 degrees higher
        initial_change = 4
        current_temp = Experiment.__sender.get_temp()
        change = temp_preference + initial_change - current_temp
        self.adjust_room(change)
        Experiment.__sender.send_damper_command(100) #open the damper 100%
        self.subscribe_to_queue(self.topic_in, self.wait_for_stop)

    def strategy4(self, temp_preference):
        """
        executes strategy 4
        :param temp_preference: the temperature preference
        """

        #initializing queues
        self.__init_queues(4)
        # set the room temperature to 4 degrees higher
        initial_change = -4
        current_temp = Experiment.__sender.get_temp()
        change = temp_preference + initial_change - current_temp
        self.adjust_room(change)
        #expect the user to turn on heater
        self.subscribe_to_queue(self.topic_in, self.wait_for_stop)

    def __monitor_loading(self, start, target):
        while start != target:
            sleep(10)
            current = Experiment.__sender.get_temp()
            loading = float(current - start) / float(target - start) * 100
            self.push_to_queue(str(loading))

    def __handle_change(self, ch, method, properties, body):
        """
        Adjusts the room to the change requested
        :param ch: keep none
        :param method:  keep none
        :param properties: keep none
        :param body: message received in callback
        :return:
        """
        change = float(body)
        self.adjust_room(change)

    def wait_for_stop(self, ch, method, properties, body):
        """
        stops the experiment when user wants.
        :param ch: keep none
        :param method: keep none
        :param properties: keep none
        :param body: the message. Expected to be 'stop'
        :return:
        """
        if body.lower() == 'stop':
            self.__stop()
        else:
            self.push_to_queue('wrong message! Expected to receive stop')

    def adjust_room(self, change):
        """
        Adjust room to the change requested
        :param change: the changed requested
        :return: nothing
        """
        if change == 0:  # experiment done
            self.__stop()
        current_temp = Experiment.__sender.get_temp()
        target_temp = current_temp + change
        p = Thread(target=Experiment.__sender.set_temp,args=(target_temp,current_temp))
        p.start()
        self.__monitor_loading(current_temp, target_temp)

    def __stop(self):
        """
        Stops the experiment when the end is reached
        :return: nothing
        """
        temp = Experiment.__sender.get_temp()
        self.push_to_queue(self.topic_out, temp) # send final temperature value at end of experiment
        self.channel.close()
        self.connection.close()

    @staticmethod
    def execute_strategy(ch, method, properties, body):
        """
        Callback function to execute function chosen
        :param ch: keep none
        :param method: keep none
        :param properties: keep none
        :param body: the information object should be dictionary
            with num (strategy number) key and temp key and their respective values
        :return:
        """
        print 'yes we received', body
        obj = json.loads(body)
        strategy_num = int(obj['num'])
        temp_preference = int(obj['temp'])
        exp = Experiment()
        if strategy_num == 1:
            exp.strategy1(temp_preference)
        elif strategy_num == 2:
            exp.strategy2(temp_preference)
        elif strategy_num == 3:
            exp.strategy3(temp_preference)
        elif strategy_num == 4:
            exp.strategy4(temp_preference)
        else:
            print 'Strategy not recognized'

def run():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=Experiment.rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue='strategy')
    channel.basic_consume(Experiment.execute_strategy, queue='strategy', no_ack=True)
    print ' [*] Waiting for messages. To exit press CTRL+C'
    channel.start_consuming()

if __name__ == '__main__':
    run()