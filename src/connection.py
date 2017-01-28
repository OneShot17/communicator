#!/usr/bin/env python3

#
# connection.py
# Created by Stephen Brimhall on 1/24/17
# Copyright (c) SST CTF and Stephen Brimhall 2017. All Rights Reserved.
#
# Implements connection to server
#

# Begin system imports
import socket;
from threading import Thread;
from threading import RLock as Lock;
import os;
# End system imports

# Begin local imports
from src.message import Message
# End local imports

# Begin global vars
disconnect = False
disconnect_lock = Lock();

class Server(Thread):
    # Server -- Represents the server object. Receiving runs as separate thread

    def __init__(self, user, address, port, keypair):
        # Creates a new server object with given username and address

        # Initialize instance variables
        self._address = (address, port)
        self._user = user
        self._pubkey = keypair[0]
        self._privkey = keypair[1]
        self._socket = socket.socket()

        # Attempt to connect to server
        try:
            self._socket.connect(self._address)
        except socket.timeout:
            # If timeout, print error message and exit with error code 1 print("Err: Connection timed out")
            os.exit(1);
            return;

        Thread.__init__(self);

        # Send hello message
        self._socket.send(user.encode('utf-8'))
        self._socket.send(self._pubkey.encode('utf-8'))

        # Receive server pubkey
        self._servkey = self._socket.recv(4096).decode('utf-8')

    def send_message(self, msg):
        #Encodes message into json and json into utf-8.
        #Sends through socket
        self._socket.send(msg.get_json().encode('utf-8'))

    def run(self):
        # Runs the thread

        while True:

            # Block until new message received
            enc_msg = self._socket.recv(4096)

            # Decrypt message
            # TODO: Implement encryption

            # Decode message for displaying
            message = Message.decode_bytes(enc_msg)

            # Run display code

            #Log
            MessageLog.get().post_message(msg)

            # Check for end value
            with disconnect_lock:
                if disconnect:
                    break
