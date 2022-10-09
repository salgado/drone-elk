#!/usr/bin/python3


import threading
import socket
import time
import logging      # DEBUG/INFO/WARNING/ERROR/CRITICAL
import json
from datetime import datetime as dt


datefmt='%Y-%m-%d.%H:%M:%S'

#logging.basicConfig(filename='logs/drone.log')
#logging.Formatter(
##    fmt='%(asctime)s.%(msecs)03d :%(message)',
#    datefmt='%Y-%m-%d,%H:%M:%S', 
#)

logging.basicConfig(filename='logs/drone.json', level=logging.DEBUG,
format='%(message)s',
datefmt='%Y-%m-%d,%H:%M:%S.ffff')

"""
@brief  Host IP address. 0.0.0.0 referring to current 
        host/computer IP address.
"""
host_ip = "0.0.0.0"
# host_ip = "192.168.10.1"

"""
@brief  UDP port to receive response msg from Tello.
        Tello command response will send to this port.
"""
response_port = 8890

""" Welcome note """
print("\nTello Sensor States Program\n")


class Tello:
    def __init__(self):
        self._running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host_ip, response_port))  # Bind for receiving

    def terminate(self):
        self._running = False
        self.sock.close()

    def recv(self):
        """ Handler for Tello states message """
        while self._running:
            try:
                msg, _ = self.sock.recvfrom(1024)  # Read 1024-bytes from UDP socket
                # print("states: {}".format(msg.decode(encoding="utf-8")))
                msg = msg.decode("utf-8")
                drone = msg.split(";")
                
                myjson= ''
                #drone = row.split(";")

                for i in range(0,15):
                    key = drone[i].split(":")[0]
                    value = drone[i].split(":")[1] 
                    print (value)
                    myjson = myjson + '"' + key + '": ' + value + ','

                print (myjson)
                d_created_at = dt.now().strftime(datefmt)

                myjson = '{"created_at": "' + d_created_at + '", ' + myjson[:-1:] + "}"
                print (myjson)

                logging.info(myjson)
                
                
            except Exception as err:
                #print(err)
                logging.error(err)

""" Start new thread for receive Tello response message """
t = Tello()
recvThread = threading.Thread(target=t.recv)
recvThread.start()

while True:
    try:
        # Get input from CLI
        msg = input()

        # Check for "end"
        if msg == "bye":
            t.terminate()
            recvThread.join()
            print("\nGood Bye\n")
            break
    except KeyboardInterrupt:
        t.terminate()
        recvThread.join()
        break
