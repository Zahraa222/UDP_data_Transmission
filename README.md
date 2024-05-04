# UDP Image Transmission

This project demonstrates the process of transmitting an image file from a client to a server using the User Datagram Protocol (UDP) in Python. The client fragments an image into smaller packets, sends them over UDP, and the server reassembles the packets back into the original image file.

## Features

- **Client Script (`client.py`)**: Sends image data in packets, handles timeouts, and resends packets if acknowledgments are not received in time.
- **Server Script (`server.py`)**: Receives packets, sends acknowledgments, and reconstructs the image file.
- **Dynamic Timeout**: The client adjusts its timeout dynamically based on the average delay of received acknowledgments.
- **Error Handling**: Both client and server include basic error handling to deal with common network issues such as packet loss.


##Understanding The Code

- **Client**
  - Fragments the image into manageable packets
  - Sends each packet sequentially, waiting for acknoledgement before sending the next
  - Adjusts timeout conditions
- **Server**
  - Listens for incoming packets and stores them in order of retreival based on sequence numbers.
  - Sends out an acknowledgement message to the client
  - Handles duplicate packets and simple network timeouts
  - reassembles image once all packets are received
