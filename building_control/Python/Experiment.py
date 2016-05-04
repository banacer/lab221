
from sender import Sender
import SerialSender
from multiprocessing import Process
from time import sleep
import json
import pika


class Experiment:
    rabbitmq_host = '172.26.50.120'
    __rabbitmq_host = '172.26.50.120'
    __rabbitmq_port = 1883
    __arduino_serial = '/dev/ttyACM1'
    __arduino_addr = 0x2211

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.__rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        self.sender = SerialSender.SerialSender(self.__arduino_serial)
        #self.sender = Sender(self.__arduino_serial, self.__arduino_addr)

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

    def __init_queues(self,num):
        self.topic_in = 'strategy%d/in' % num
        self.topic_out = 'strategy%d/out' % num
        self.channel.queue_declare(queue=self.topic_in)
        self.channel.queue_declare(queue=self.topic_out)

    def __strategy1(self, temp_preference):
        """
        executes strategy 1
        :param temp_preference: the temperature preference
        """
        # initializing queues
        self.__init_queues(1)
        #set the room temperature to 4 degrees higher
        initial_change = 4
        self.adjust_room(initial_change)
        self.subscribe_to_queue(self.topic_in, self.__handle_change)


    def __strategy2(self,temp_preference):
        """
        executes strategy 2
        :param temp_preference: the temperature preference
        """
        print 'strategy 2 running!'

        #initializing queues
        self.__init_queues(2)
        # set the room temperature to 4 degrees lower
        initial_change = -4
        self.adjust_room(initial_change)
        self.subscribe_to_queue(self.topic_in, self.__handle_change)

    def __strategy3(self,temp_preference):
        """
        executes strategy 3
        :param temp_preference: the temperature preference
        """

        #initializing queues
        self.__init_queues(3)
        # set the room temperature to 4 degrees higher
        initial_change = 4
        self.adjust_room(initial_change)
        self.sender.sendDamperCmd(100) #open the damper 100%
        self.subscribe_to_queue(self.topic_in,self.wait_for_stop)

    def __strategy4(self,temp_preference):
        """
        executes strategy 4
        :param temp_preference: the temperature preference
        """

        #initializing queues
        self.__init_queues(4)
        # set the room temperature to 4 degrees higher
        initial_change = -4
        self.adjust_room(initial_change)
        #expect the user to turn on heater
        self.subscribe_to_queue(self.topic_in, self.wait_for_stop)

    def __monitor_loading(self,start, target):
        while start != target:
            current = self.sender.getTemp()
            loading  = float(current - start) / float(target - start) * 100
            self.push_to_queue(str(loading))
            sleep(10)

    def __handle_change(self,ch, method, properties, body):
        change = float(body)
        self.adjust_room(change)

    def wait_for_stop(self, ch, method, properties, body):
        if body.lower() == 'stop':
            self.__stop()
        else:
            self.push_to_queue('wrong message! Expected to receive stop')

    def adjust_room(self,change):
        print 'you are here'
        if change == 0:  # experiment done
            self.__stop()
        current_temp = self.sender.getTemp()
        target_temp = current_temp + change
        p = Process(target=self.sender.set_temp, args=(target_temp,))  # create thread to execute process
        self.__monitor_loading(current_temp, target_temp)
        # Process(target=MQTT.__monitor_loading,args=(current_temp,target_temp,userdata,))

    def __stop(self):
        temp = self.sender.getTemp()
        self.push_to_queue(self.topic_out,temp) # send final temperature value at end of experiment
        self.channel.close()
        self.connection.close()

    @staticmethod
    def execute_strategy(ch, method, properties, body):
        print 'yes we received', body
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


connection = pika.BlockingConnection(pika.ConnectionParameters(host=Experiment.rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue='strategy')
channel.basic_consume(Experiment.execute_strategy,queue='strategy',no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

