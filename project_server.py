import socket
import threading
import os
import hashlib
import time
import sys
import json
import re

train_list = {
    'Meenakshi':'467eb98e1866708e03cd9ab9f8a7f4e53fc92738ea0700ac00af93c4074a870f',
    'Bhanu':'109de0eff6a8ea2b37bb3ef364f7ecbdd61d4e8d97908f93a2a94e25c16aadc8'
}


def authenticate_client(client_socket,client_address):
   passkey = client_socket.recv(4096).decode().split(':')
   if train_list[passkey[0]] == passkey[1]:
     client_socket.send(b"Authentication successful.")
     print(f"Accepted connection from {client_address}")
     return 1
   else:
     client_socket.send(b"Authentication Failed.")
     print(f"Denied connection from {client_address}")
     client_socket.close()
     return 0


# Function to handle each client's communication
def handle_client(client_socket, client_address, target_client, target_address, a1, a2, speed, direction_in, dist, cnt):
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    target_client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    target_client.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
    if a1[0] == 1 and a2[0] == 1:
      try:
          data = client_socket.recv(1024)
          if not data:
              #info = "RFID Data not detected"
              #client_socket.send(info.encode())
              return
          #print (data.decode())
          speed[0] = speed_check(data)
          dist[0] = margin(data)
          direction_in[0] = direction(data,cnt)
      except:
          a1[0] = 0
          a2[0] = 1
          client_socket.close()
      try:
          target_client.send("".encode())  # Forward data to the target client
      except:
          a1[0] = 1
          a2[0] = 0


# Permissible speed check
def speed_check(dta):
  try:
    dta = dta.decode()
    dta = json.loads(dta)
    train_time = dta["SPEED"]
    allowed = dta["PERMISSIBLE SPEED"]
    if allowed < train_time:
        return "EXCEEDING PERMISSIBLE SPEED"
    else:
        return "OK"
  except:
    return


def margin (dta):
  try:
    dta = dta.decode()
    dta = json.loads(dta)
    dist = dta["TID"]
    dist = int(dist.split('R')[1])
    return dist
  except:
    return



# Direction of Train
def direction(dta,cnt):
  try:
    #global cnt
    dta = dta.decode()
    #if not dta:
       # info = "RFID data not detected"
       # return info
    dta = json.loads(dta)
    direction = dta["TID"]
    direction = int(direction.split('R')[1])
    if cnt[0] == 0:
        cnt[0] = direction
    else:
        direction = direction - cnt[0]
        if direction > 0:
            return "FORWARD"
        elif direction < 0:
            return "BACKWARD"
        elif direction == 0:
            return "STATIONARY"
  except:
    return


def compare(c1, c2, ca1, ca2, s1, s2, dis1, dis2, d1, d2):
    if s1[0] == "EXCEEDING PERMISSIBLE SPEED" or s2[0] == "EXCEEDING PERMISSIBLE SPEED":
        try:
            mrgn = abs(dis1[0] - dis2[0])
        except:
            return
        print("**********************",mrgn,"**********************")
        if mrgn <= 5000 and d1[0] != d2[0]:
            msg_send = "STOP"
            #sys.exit(0)
        else:
            msg_send = "SLOW DOWN"
    else:
        msg_send = ""
    #print ("MSG_SEND:",msg_send)
    #print("Speed:",s1[0], s1[0])
    #print("Direction:",d1[0],d2[0])
    #print("printing value")
    msg_send1 = json.dumps([s1[0], ca2, d1[0], msg_send])
    msg_send2 = json.dumps([s2[0], ca1, d2[0], msg_send])
    c1.send(msg_send1.encode())
    c2.send(msg_send2.encode())
    return





# Server function to manage the communication between clients
def start_server():

    refresh = 0
    auth1 = [0]
    auth2 = [0]
    speed1 = [0]
    speed2 = [0]
    direction1 = [0]
    direction2 = [0]
    client1_address = 0
    client2_address = 0
    cnt1 = [0]
    cnt2 = [0]
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('10.114.240.13', 65532))
    #server_socket.settimeout(t)
    server_socket.listen(2)  # Allow two clients to connect


    print("Server is listening for connections...")
    ack = "ACK"
    dist1 = [0]
    dist2 = [0]
    while True:
        # Wait till both auth is zero

        #print(auth1[0])
        #print("******")
        #print(auth2[0])
        if auth1[0] == 1 and auth2[0] == 1 and client1_address[0] == client2_address[0]:
           auth1[0] = 0
           auth2[0] = 1
        elif auth1[0] == 1 and auth2[0] == 1 and client1_address[0] != client2_address[0]:
        # Create threads to handle communication for each client
           client1_thread = threading.Thread(target=handle_client, args=(client1_socket, client1_address, client2_socket, client2_address, auth1, auth2, speed1, direction1, dist1, cnt1))
           client2_thread = threading.Thread(target=handle_client, args=(client2_socket, client2_address, client1_socket, client1_address, auth2, auth1, speed2, direction2, dist2, cnt2))
           msg_tx = threading.Thread(target=compare, args=(client1_socket, client2_socket, client1_address, client2_address, speed1, speed2, dist1, dist2, direction1, direction2))
        # Start the threads
           client1_thread.start()
           client2_thread.start()
           msg_tx.start()
           client1_thread.join()
           client2_thread.join()
           msg_tx.join()
        elif auth1[0] == 1 and auth2[0] == 0:
           try:
               data = client1_socket.recv(1024)
               print(data.decode())
               speed = speed_check(data)
               dir = direction(data,cnt1)
               speed = json.dumps([speed, dir])
               client1_socket.send(speed.encode())
           except:
               auth1[0] = 0
               auth2[0] = 0
               continue
           try:
               server_socket.settimeout(2)
               client2_socket, client2_address = server_socket.accept()
               auth2[0] = authenticate_client(client2_socket,client2_address)
           except socket.timeout:
               continue
        elif auth1[0] == 0 and auth2[0] == 1:
           try:
               data = client2_socket.recv(1024)
               print(data.decode())
               speed = speed_check(data)
               dir = direction(data,cnt2)
               speed = json.dumps([speed, dir])
               client2_socket.send(speed.encode())
           except:
               auth1[0] = 0
               auth2[0] = 0
           try:
               server_socket.settimeout(2)
               client1_socket, client1_address = server_socket.accept()
               auth1[0] = authenticate_client(client1_socket,client1_address)
           except socket.timeout:
               continue
        elif auth1[0] == 0 and auth2[0] == 0:
             if refresh == 1:
                server_socket.settimeout(8)
             try:
                client1_socket, client1_address = server_socket.accept()
                auth1[0] = authenticate_client(client1_socket,client1_address)
                data = client1_socket.recv(1024)
                client1_socket.send(ack.encode())
                print(data.decode())
             except socket.timeout:
                print("Connection Failure!!!")
                sys.exit(1)
             refresh = 1
             server_socket.settimeout(2)

if __name__ == "__main__":
    start_server()
