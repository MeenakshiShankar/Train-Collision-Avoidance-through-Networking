import socket
import fcntl
import struct
import sys
import datetime
import json
import random

from colored import fg

color = fg('red')


def generate_packet(pkt):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    TID = "R00"+str(pkt)
    permit = 110 - random.randint(1,15)
    rfid_data = {
        "TID": TID,
        "SPEED": 100,
        "PERMISSIBLE SPEED": permit,
        "TSTAMP": time
    }

    train_payload = json.dumps(rfid_data)
    return train_payload


def get_ip_address(ifname):
    c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(c.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

print("Wifi: ", get_ip_address(b'wlan0'))

HOST = get_ip_address(b'wlan0')     # Standard loopback interface address (localhost)
PORT = 50001             # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
   c.bind((HOST,PORT))
  # c.listen()

SERVER_IP = "10.114.240.13"
SERVER_PORT = 65532
pkt_no = 10000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
   s.connect((SERVER_IP,SERVER_PORT))
   s.send(b"Meenakshi:467eb98e1866708e03cd9ab9f8a7f4e53fc92738ea0700ac00af93c4074a870f")  ##hashed password 
   conn_msg = s.recv(4096)
   print (conn_msg)
   if (conn_msg.decode() == "Authentication successful."):
       while(True):
          pkt_no = pkt_no-1                                                         ##its incrementing in one client and decrementing in the other
          #pkt_no_bytes = bytes(pkt_no)
          #print (pkt_no)
#     s.send(pkt_no_bytes)
          train_payload = generate_packet(pkt_no)
          print ("pkt_send:",train_payload)
          s.send(train_payload.encode())
          pkt_send_time = datetime.datetime.now()
          print ("Send time: ",pkt_send_time)
          data = s.recv(1024)
          #speed_val = s.recv(1024)
          print ("rcv_pkt:",data.decode())
          #if (data.decode() == "STOP"):
           #   print("rcv_pkt:")
            #  print(color + data.decode())
          #else:
           #   print("rcv_pkt:",data.decode())
          #print(speed_val)
          pkt_recv_time = datetime.datetime.now()
          print ("Recv time:",pkt_recv_time)
