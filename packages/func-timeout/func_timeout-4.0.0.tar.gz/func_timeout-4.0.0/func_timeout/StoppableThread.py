'''
    Copyright (c) 2016, 2017 Tim Savannah All Rights Reserved.

    Licensed under the Lesser GNU Public License Version 3, LGPLv3. You should have recieved a copy of this with the source distribution as
    LICENSE, otherwise it is available at https://github.com/kata198/func_timeout/LICENSE
'''

import os
import ctypes
import threading
import time
import sys

__all__ = ('StoppableThread', 'JoinThread')

class StoppableThread(threading.Thread):
    '''
        StoppableThread - A thread that can be stopped by forcing an exception in the execution context.
    '''


    def _stopThread(self, exception):
        if self.isAlive() is False:
            return True

        self._stderr = open(os.devnull, 'w')
        joinThread = JoinThread(self, exception)
        joinThread._stderr = self._stderr
        joinThread.start()
        joinThread._stderr = self._stderr

class JoinThread(threading.Thread):
    '''
        JoinThread - The workhouse that stops the StoppableThread
    '''

    def __init__(self, otherThread, exception, repeatEvery=2.0):
        threading.Thread.__init__(self)
        self.otherThread = otherThread
        self.exception = exception
        self.repeatEvery = repeatEvery
        self.daemon = True

    def run(self):

        # Try to silence default exception printing.
        self.otherThread._Thread__stderr = self._stderr
        if hasattr(self.otherThread, '_Thread__stop'):
            # If py2, call this first to start thread termination cleanly.
            #   Python3 does not need such ( nor does it provide.. )
            self.otherThread._Thread__stop()
        while self.otherThread.isAlive():
            # We loop raising exception incase it's caught hopefully this breaks us far out.
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.otherThread.ident), ctypes.py_object(self.exception))
            self.otherThread.join(self.repeatEvery)

        try:
            self._stderr.close()
        except:
            pass


