# Train-Collision-Avoidance-through-Networking
This repository contains the code files for the miniproject submitted as part of my coursework for TCP/IP course at IISc

# Train Collision Avoidance System using TCP/IP

This project implements a **Train Collision Avoidance System** where trains running on the same track communicate via a TCP/IP client-server model to avoid collisions. The system leverages **RFID tags** placed along the track to gather real-time data about the trains' speed, distance, and direction, which are then exchanged between nearby trains to facilitate safe operation.

## Key Features

- **Train-to-Train Communication**: Trains use TCP/IP to communicate with each other in real-time.
- **RFID Tags**: RFID tags are placed along the tracks to provide data about train positioning.
- **Speed Monitoring**: Each train monitors its speed and compares it with a permissible limit.
- **Collision Avoidance**: Trains exchange speed, distance, and direction data to decide whether to stop or slow down based on proximity and direction.
- **Client-Server Model**: A server acts as a bridge between two or more trains, allowing them to exchange critical information such as speed, distance, and movement direction.

## How It Works

1. **RFID System**: RFID tags placed at regular intervals along the track are read by a train's onboard RFID reader. These tags provide the train's current location and direction.
2. **Data Communication**: The train sends a packet containing its speed, permissible speed, direction, and other relevant information to a central server via TCP/IP.
3. **Server**: The server authenticates the train and forwards its information to other nearby trains. It also calculates the distance between trains and warns them if a collision risk is detected.
4. **Collision Detection**: If two trains are too close and moving toward each other, the system instructs one or both trains to stop or slow down to prevent a collision.
5. **Client-Server Interaction**: Both trains communicate via the server, sending data packets periodically to update the system on their current status.

## Technologies Used

- **TCP/IP Networking**: For communication between the trains and the central server.
- **Python Socket Programming**: For implementing client-server communication.
- **RFID Technology**: To track the position of the trains along the track.
- **Multithreading**: For handling multiple clients (trains) simultaneously on the server.
- **JSON**: For sending and receiving train data in a structured format.

## Code Flow

### Server

1. **Server Initialization**:
   - The server listens for incoming connections from two trains at the same time using the `socket` module.
   - The server is designed to allow a maximum of two trains to connect simultaneously.
   
2. **Authentication**:
   - When a train connects, the server authenticates it by comparing its credentials (train name and hashed password) with a predefined list of valid trains.
   - If the authentication fails, the server closes the connection with the client.

3. **Handling Client Communication**:
   - Once both trains are authenticated, the server creates separate threads for each train to handle incoming data.
   - Each train sends its speed, distance from RFID tags, and direction data to the server.
   
4. **Collision Detection**:
   - The server calculates the distance between the two trains by analyzing the RFID tag data from both.
   - It checks if the trains are moving towards each other and whether the permissible speed is being exceeded.
   
5. **Sending Control Messages**:
   - Based on the proximity of the trains and their speed, the server sends a message to the trains:
     - **STOP**: If the trains are too close.
     - **SLOW DOWN**: If the trains are approaching each other but not at critical risk of collision.
   
6. **Multithreading**:
   - The server handles multiple clients (trains) simultaneously using multithreading to ensure that communication is smooth and real-time.
   - It waits for both trains to connect before starting to exchange messages.

### Client (Train)

1. **Client Initialization**:
   - Each train acts as a client and connects to the central server using TCP/IP.
   - The client uses an RFID reader installed on the train to gather the train's real-time data, such as speed, location, and direction.

2. **Authentication**:
   - Upon connection to the server, the train sends its credentials (train name and hashed password) for authentication.
   - If authenticated successfully, the client starts the data transmission loop.

3. **Data Packet Generation**:
   - The train gathers information such as:
     - Train ID (based on RFID)
     - Current speed
     - Permissible speed (determined randomly for demonstration)
     - Timestamp
   - This data is serialized into a JSON packet and sent to the server.

4. **Receiving Server Instructions**:
   - The client receives a response from the server, which includes the updated speed, direction, and any control messages (e.g., **STOP** or **SLOW DOWN**).
   - The client decodes the response and acts on it (printing the instructions or adjusting speed for simulation purposes).

5. **Looping Data Transmission**:
   - The client continues to periodically send packets to the server and receives updated instructions.
   - This loop runs continuously, simulating real-time train communication and decision-making.

6. **Timeout Handling**:
   - The client includes timeout handling to ensure that it retries the connection if the server doesn't respond in a timely manner.

## Setup Instructions

### Prerequisites

- **Python 3.x** installed on all machines (server and trains).
- A system with **RFID readers** installed on the trains.
- RFID tags placed along the length of the railway track.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/train-collision-avoidance.git
   cd train-collision-avoidance
   ```

2. **Install Dependencies** (if any):
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server

1. Navigate to the server directory and run the server:
   ```bash
   python server.py
   ```

2. The server will start listening for connections from the trains (clients).

### Running the Train (Client)

1. Each train acts as a client and connects to the server. Run the following command on the train:
   ```bash
   python train_client.py
   ```

2. The train will continuously read RFID data, generate packets, and communicate with the server.

### Communication Protocol

- **Authentication**: Each train authenticates with the server by sending its ID and hashed password.
- **Data Exchange**: Trains send structured data packets containing:
  - Train ID (`TID`)
  - Current speed
  - Permissible speed
  - Distance from RFID tag
  - Timestamp

- **Packet Format**:
  ```json
  {
      "TID": "R001",
      "SPEED": 100,
      "PERMISSIBLE SPEED": 90,
      "TSTAMP": "2023-09-12 14:33:12.123456"
  }
  ```

## Example Scenario

- **Train A** sends its current speed, distance from the RFID tag, and direction to the server.
- **Train B** sends its current information to the server as well.
- The server checks if the two trains are on a collision course by comparing the distance and direction of both trains.
- If the trains are too close, the server sends a message to both trains to **STOP** or **SLOW DOWN**.
- The trains will act on this information to avoid a collision.

## Future Enhancements

- **Real-time GPS Integration**: Combine GPS data with RFID for more accurate train positioning.
- **Automated Braking System**: Integrate with the train's control system to automatically apply brakes if necessary.
- **GUI Dashboard**: Implement a visual dashboard for railway management to monitor train movement in real-time.


