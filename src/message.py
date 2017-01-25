#!/usr/bin/env python3

#
# message.py
# Created by Stephen Brimhall on 1/24/17
# Copyright (c) SST CTF and Stephen Brimhall 2017. All Rights Reserved.
#
# Implements a data structure for messages sent
#

# Begin system imports
import json
# End system imports

# Begin static var declarations
json_coder = json.JSONDecoder();
# End static var declarations

class Message:
    # Message -- Data structure for sending and receiving messages

    def __init__(self, user, message, metadata={}):
        # Takes username, message, and other metadata and returns a new Message.
        # Used metadata includes color (one of the standard ANSI colors),
        # channel, target (user to direct-message).

        # Add user to metadata (this will be sent as JSON)
        metadata['user'] = user

        # Add message to metadata (also sent as JSON)
        metadata['message'] = message

        # Store metadata in object
        self._data = metadata

    def get_json(self):
        # Returns the JSON representation of this message

        return json_coder.encode(self._data)

    def add_data(self, key, value):
        # Takes a key and value for the new metadata, adding it to the message

        self._data[key] = value

    def get_bytes(self):
        # Returns the byte array of the JSON representation of this message

        return self.get_json().encode("utf-8")

    @staticmethod
    def from_json(json_string):
        # Takes a JSON string and decodes it, storing it in a Message object.

        # Decode string
        contents = json_coder.decode(json_string)

        # Add specific variables
        user = contents['user']
        message = contents['message']

        # Create new message and return it
        return Message(user, message, contents)

    @staticmethod
    def from_bytes(byte_array):
        # Takes a bytearray and decodes it, storing it in a Message object.
        
        return Message.from_json(byte_array.decode('utf-8')
