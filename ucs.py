import pika
import grpc
from threading import Thread
from concurrent import futures
from time import sleep
from comms_pb2 import sendCommandToDevice, receiveResponse
from comms_pb2_grpc import SmartHomeServiceServicer,add_SmartHomeServiceServicer_to_server

umidity = 60
current_umidity = umidity
temporary_umidity = umidity

class umidity_control_system():
    def __init__(self):
        self.umidificador = False
        self.desumidificador = False
    
    def on_off_umidificador(self,tf):
        global temporary_umidity
        
        if(tf == True and self.umidificador == False):
            self.umidificador = True
            temporary_umidity += 10
        elif(tf == False and self.umidificador == True):
            temporary_umidity -= 10
            self.umidificador = False
    
    def on_off_desumidificador(self,tf):
        global temporary_umidity
        
        if(tf == True and self.desumidificador == False):
            self.desumidificador = True
            temporary_umidity -= 10
        elif(tf == False and self.desumidificador == True):
            temporary_umidity += 10
            self.desumidificador = False

def temp_sensor():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='SensorLogs', exchange_type='fanout')
    
    while True:
        global current_umidity
        sleep(5)
        if(temporary_umidity > current_umidity):
            current_umidity += 2
        elif(temporary_umidity < current_umidity):
            current_umidity -= 2
        channel.basic_publish(exchange='SensorLogs',
                        routing_key='',
                        body="Umidity sensor: " + str(current_umidity))

t1 = Thread(target=temp_sensor)
t1.start()

class SmartHomeServiceActuator(SmartHomeServiceServicer):
    def __init__(self):
        self.ucs = umidity_control_system() 
        super().__init__()
    
    def Command(self, request, context):
        if(request.command.split()[0] == 'set_status_u'):
            print(request.command.split()[1].upper())
            if(request.command.split()[1].upper() == 'TRUE'):
                self.ucs.on_off_umidificador(True)
                return receiveResponse(response = "Umidificador ligado!")
            else:
                self.ucs.on_off_umidificador(False)
                return receiveResponse(response = "Umidificador desligado!")    
        elif(request.command.split()[0] == 'set_status_du'):
            if(request.command.split()[1].upper() == 'TRUE'):
                self.ucs.on_off_desumidificador(True)
                return receiveResponse(response = "Desumidificador ligado!")
            else:
                self.ucs.on_off_desumidificador(False)
                return receiveResponse(response = "Desumidificador desligado!")    

        else:
            return receiveResponse(response = "Não foi possível realizar o comando!")

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
smart_home_service_actuator = SmartHomeServiceActuator()
add_SmartHomeServiceServicer_to_server(smart_home_service_actuator, server)

server.add_insecure_port('localhost:8050')
server.start()
server.wait_for_termination()
