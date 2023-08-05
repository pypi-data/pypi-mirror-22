from .message import (
    Message,
    MessageOpcode,
    MessageSerializer,
    MessageDeserializer
)

import json
import socket
import ssl
import struct
import time

class HeurisClient:
    HOST = 'hmp.heuris.io'
    PORT = 21099

    def __init__(self, username, token):
        self.socket = self.create_secure_socket()
        self.login(username, token)
    
    def send_measurement(self, entries, **kwargs):
        begin = self.utcnow()
        measurement = Message(MessageOpcode.MEASUREMENT)
        measurement.entries = entries
        self.add_time_if_needed(measurement)
        self.send_message(measurement)
        self.handle_response()
        self.sleep_if_needed(begin, kwargs)
    
    def create_secure_socket(self):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        return context.wrap_socket(
            socket.socket(),
            server_hostname = self.HOST)
    
    def login(self, username, token):
        self.connect()
        msg = Message(MessageOpcode.LOGIN)
        msg.entries['username'] = username
        msg.entries['token'] = token
        self.send_message(msg)
        self.handle_response()
    
    def connect(self):
        self.socket.connect((self.HOST, self.PORT))
    
    def send_message(self, msg):
        data = MessageSerializer.serialize(msg)
        self.socket.send(struct.pack('>I', len(data)))
        self.socket.send(data)
    
    def handle_response(self):
        reply = self.read_message()
        if reply.opcode == MessageOpcode.ERROR:
            raise Exception(reply.entries['message'])
    
    def read_message(self):
        length = self.read_message_length()
        return self.read_message_payload(length)

    def read_message_length(self):
        header = self.socket.recv(4)
        return struct.unpack('>I', header)[0]
    
    def read_message_payload(self, length):
        payload = self.socket.recv(length)
        return MessageDeserializer.deserialize(payload)
    
    def add_time_if_needed(self, measurement):
        if 'time' not in measurement.entries:
            measurement.entries['time'] = self.utcnow()

    def utcnow(self):
        return int(round(time.time() * 1000))
    
    def sleep_if_needed(self, begin, kwargs):
        if 'period' in kwargs:
            self.sleep(max(0, kwargs['period'] - (self.utcnow() - begin)))
        if 'wait' in kwargs:
            self.sleep(kwargs['wait'])

    def sleep(self, milliseconds):
        time.sleep(milliseconds / 1000.0)
