import pika
import grpc
from threading import Thread
from concurrent import futures
from time import sleep
from comms_pb2 import sendCommandToDevice, receiveResponse
from comms_pb2_grpc import SmartHomeServiceServicer,add_SmartHomeServiceServicer_to_server

ambient_temperature = 26
current_temperature = ambient_temperature
temporary_temperature = ambient_temperature
class Ar_Condicionado():
    def __init_(self):
        self.temp = 26
        self.status = False
    
    def set_status(self,tf):
        if self.status != tf:
            self.status = tf
    
    def set_temperature(self,value):
        global current_temperature
        global temporary_temperature

        if value >= 16 and value <= 30:
            self.temp = value
            temporary_temperature = value

def temp_sensor():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='SensorLogs', exchange_type='fanout')
    
    while True:
        global current_temperature
        sleep(5)
        if(temporary_temperature > current_temperature):
            current_temperature += 1
        elif(temporary_temperature < current_temperature):
            current_temperature -= 1
        channel.basic_publish(exchange='SensorLogs',
                        routing_key='',
                        body="Temperature sensor: " + str(current_temperature))

t1 = Thread(target=temp_sensor)
t1.start()

class SmartHomeServiceActuator(SmartHomeServiceServicer):
    def __init__(self):
        self.ac = Ar_Condicionado() 
        super().__init__()
    
    def Command(self, request, context):
        if(request.command.split()[0] == 'set_temperature'):
            if(int(request.command.split()[1]) >= 16 and int(request.command.split()[1]) <= 30):
                self.ac.set_temperature(int(request.command.split()[1]))
                return receiveResponse(response = f'Temperatura do ar-condicionado: {int(request.command.split()[1])}')
        
        elif(request.command.split()[0] == 'set_status'):
            self.ac.set_status(request.command.split()[1])
            if(request.command.split()[1] == True):
                return receiveResponse(response = "Ar condicionado Ligado!")
            else:
                return receiveResponse(response = "Ar condicionado Desligado!")    

        else:
            return receiveResponse(response = "Não foi possível realizar o comando!")

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
smart_home_service_actuator = SmartHomeServiceActuator()
add_SmartHomeServiceServicer_to_server(smart_home_service_actuator, server)

server.add_insecure_port('localhost:8000')
server.start()
server.wait_for_termination()
