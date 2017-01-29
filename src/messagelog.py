#!/usr/bin/env python3

#
# MessageLog.py
# Created by Stephen Brimhall on 1/27/17
# Copyright (c) SST CTF and Stephen Brimhall 2017.
#
# Implements a message log which represents the screen of messages

# Begin system imports
import curses
import textwrap
# End system imports

# Begin local imports
from src.threadsafe import ThreadsafeData as Data

log = None

class MessageLog:
    # MessageLog -- Represents the message list on-screen.

    def __init__(self, user, logwindow):
        # Store instance variables

        # Channel list, needs to be threadsafe because both typing and output
        # threads can access it.
        self.channels = Data([
            "general",
            "OneShot17"
        ])

        # Store username given on initialization
        self.username = Data(user)

        # Store window given on init
        self.window = logwindow

        # Store line number we're on
        self.line = 0

        # Store this object in the log variable
        log = self
        
    def post_message(self,message):
        # Posts a new message to the message board if we're subscribed to it

        with self.channels:

            # Make sure we are in the given channel. We're always in global and
            # our username.
            if not message in self.channels.data:
                return

            # Make sure that if it's private, it's to us.
            with self.username:
                if message['private'] and message['channel'] != self.username.data:
                    return

            # Get screen width/height
            height,width = self.window.getmaxyx()
            
            # Get wrapped string list
            str_to_wrap = self._line_length(message['message'],
                                            message['user'], message['channel'])
            wrapped_list = self._wrap(str_to_wrap, width)

            # Create color pairs for this list
            # 1 is for channel, 2 is for users
            curses.init_pair(1, 4, 0)
            curses.init_pair(1, message['color'], 0)
            
            # Begin printing
            i = 0;
            for line in wrapped_list:
                # Set scroll value (default false)
                scroll = False
                
                # Check if we need to scroll it
                if self.line == height - 1:
                    self.window.scroll()
                    # This way at the end of the loop we know if we have to
                    # increment the line number
                    scroll = True

                # Move to beginning of newline
                self.window.setyx(self.line, 0)

                # Make sure we print the channel and username
                if i == 0:
                    self.window.addstr("#" + message['channel'] + ": ",
                                       curses.color_pair(1) | curses.A_BOLD)
                    self.window.addstr(message['user'] + "> ",
                                       curses.color_pair(2))

                # Print line
                self.window.addstr(line, curses.color_pair(0))

                # Check to see if we need to increment self.line
                if not scroll:
                    self.line += 1

                # Increment i
                i += 1

            # Draw screen
            self.window.refresh()
                    
    def _wrap(self,string,width):
        # Hard-newline strings that are too wide to fit in the window.

        return textwrap.wrap(string,width)

    def _line_length(self, string, sender, channel):
        # Returns the string with spaces for sender and channel, to _wrap() it.

        # Store window width
        _,width = self.window.getmaxyx();

        # Create prefix string
        prefix = "#" + channel + ": " + sender + "> "

        # Add `prefix` spaces to the beginning of string
        for i in range(0,prefix):
            string = " " + string

        # Return string
        return string

    @staticmethod
    def get():
        # Returns the stored log.

        return log
