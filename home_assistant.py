import pika
import grpc
import socket
from threading import Thread
from comms_pb2 import sendCommandToDevice
from comms_pb2_grpc import SmartHomeServiceStub

def receiveSensorInformation():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='SensorLogs', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='SensorLogs', queue=queue_name)

    channel.queue_declare(queue='SensorsQueue')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode('utf-8'))

    channel.basic_consume(queue=queue_name,
                        auto_ack=True,
                        on_message_callback=callback)

    channel.start_consuming()

t1 = Thread(target=receiveSensorInformation)
t1.start()

def receive_commands():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    sock.bind(server_address)
    sock.listen(1)
    while True:
        con, addr = sock.accept()
        while True:
            comando = con.recv(1024).decode('utf-8')
            if(comando.split()[2] == 'AC'):            
                smart_home_service_channel = grpc.insecure_channel('localhost:8000')
                smart_home_service_actuator = SmartHomeServiceStub(smart_home_service_channel)
                comando = comando.split()[0] + " " + comando.split()[1]
                send_command = sendCommandToDevice(command = comando)
                response = smart_home_service_actuator.Command(send_command)
                print(response.response)
            elif(comando.split()[2] == 'ICS'):
                smart_home_service_channel = grpc.insecure_channel('localhost:8080')
                smart_home_service_actuator = SmartHomeServiceStub(smart_home_service_channel)
                comando = comando.split()[0] + " " + comando.split()[1]
                send_command = sendCommandToDevice(command = comando)
                response = smart_home_service_actuator.Command(send_command)
                print(response.response)
            elif(comando.split()[2] == 'UCS'):
                smart_home_service_channel = grpc.insecure_channel('localhost:8050')
                smart_home_service_actuator = SmartHomeServiceStub(smart_home_service_channel)
                comando = comando.split()[0] + " " + comando.split()[1]
                send_command = sendCommandToDevice(command = comando)
                response = smart_home_service_actuator.Command(send_command)
                print(response.response)

t2 = Thread(target=receive_commands)
t2.start()