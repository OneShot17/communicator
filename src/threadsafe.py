#!/usr/bin/env python3

#
# threadsafe.py
# Created by Stephen Brimhall on 1/27/17
# Copyright (c) SST CTF and Stephen Brimhall 2017.
#
# Implements threadsafe data structure

from threading import RLock as Lock

class ThreadsafeData:

    def __init__(data):
        # Takes data of any type and returns a ThreadsafeData object

        # Store data
        self.data = data

        # Save lock
        self._lock = Lock()

    def __enter__():
        # Entering `with` statements

        # Enable lock
        self._lock.aquire()

    def __exit__():
        # Exiting the `with` statement

        # Disable lock
        self._lock.release()
