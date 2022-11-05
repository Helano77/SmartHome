import pika
import grpc
from random import randint
from threading import Thread
from concurrent import futures
from time import sleep
from comms_pb2 import sendCommandToDevice, receiveResponse
from comms_pb2_grpc import SmartHomeServiceServicer,add_SmartHomeServiceServicer_to_server

smoke = False

class incendiary_control_system():
    def __init_(self):
        self.status = False
    
    def set_status(self,tf):
        global smoke
        if tf == True:
            self.status = tf
            smoke = False

def smoke_sensor():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='SensorLogs', exchange_type='fanout')
    
    while True:
        global smoke
        sleep(5)
        probability_smoke = randint(0,101)
        if(probability_smoke > 70):
            smoke = True
        
        if(smoke):
            channel.basic_publish(exchange='SensorLogs',
                                  routing_key='',
                                  body="Sensor de fumaça: Fumaça Detectada!")
        else:
            channel.basic_publish(exchange='SensorLogs',
                                  routing_key='',
                                  body="Sensor de fumaça: Sem fumaça!")

t1 = Thread(target=smoke_sensor)
t1.start()

class SmartHomeServiceActuator(SmartHomeServiceServicer):
    def __init__(self):
        self.ics = incendiary_control_system() 
        super().__init__()
    
    def Command(self, request, context):
        if(request.command.split()[0] == 'set_status'):
            if(request.command.split()[1].upper() == 'TRUE'):
                self.ics.set_status(True)
                return receiveResponse(response = "Sistema de controle de incendio Ligado!")
            elif(request.command.split()[1].upper() == 'FALSE'):
                self.ics.set_status(bool(request.command.split()[1]))
                return receiveResponse(response = "Sistema de controle de incendio Desligado!")    

        else:
            return receiveResponse(response = "Não foi possível realizar o comando!")

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
smart_home_service_actuator = SmartHomeServiceActuator()
add_SmartHomeServiceServicer_to_server(smart_home_service_actuator, server)

server.add_insecure_port('localhost:8080')
server.start()
server.wait_for_termination()
