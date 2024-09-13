//ReadMe

1.The python code for server can be executed as  " python3 project_server.py ".

2.Similarly python code for client i.e train_1 and train_2 can be executed as " python3 train1_client.py " and 
" python3 train2_client.py "


//Working and Cases Covered:

1.We are establishing and ensuring single client to server communication. This step uses hashing to enable authentication to ensure only valid entities can join the server.

2.The TID (Tag ID) are utilised to check the distance between the trains based on the sequence of ID i.e. whether it is incrementing or decrementing and this helps to decide the direction of the train.

3.The collision case is detected based on the thresholding of the distance between the trains and it is estimated as the difference in the sequence of the TID.

4.Furthermore we have also allowed the server to realise if the trains are exceeding the permissible speeding limits for the tracks that it runs on and the warning is sent.

5.MultiThreading is used to allow the multiple trains to connect to server parallely and also to cross communicate data to each other via server.

6.Also, emulated the packet loss condition using netem to show the sustenance of network even if packet loss condition exists. 

-->Run the following       :sudo tc qdisc add dev wlan0 root netem loss 5%
-->For packet Corruption   :sudo tc qdisc add dev wlan0 root netem corrupt 30%
The truncated ip message in the ppt indicates this loss of packets (given in ppt). We explored options of tcp_NoDelay and tcp_DelayedAck to handled these cases.









