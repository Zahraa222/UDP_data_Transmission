import socket
import time

HOST = '127.0.0.1'     # The server's IP address
PORT = 1234               # The port used by the server
BUFFER_SIZE = 1024        # Buffer size

delays = []
dynamic_timeout = 5

# Path to the image file
image_path = "C:\\Users\\test.jpg"
print(f"File name opened: {image_path}")

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Load the JPG image
with open(image_path, 'rb') as f:
    image_data = f.read()
    print("File data copied to buffer.")

# Fragment the JPG image into packets of BUFFER_SIZE bytes
packets = [image_data[i:i+BUFFER_SIZE] for i in range(0, len(image_data), BUFFER_SIZE)]
acknowledged_packets = [False] * len(packets) # tracks ack status of each packet

# Start the timer
start_time = time.time()

# Send each packet, waiting for an acknowledgment before sending the next
for packet_number, packet in enumerate(packets):
    while not acknowledged_packets[packet_number]:
        # Send the packet with a sequence number at the start
        sock.sendto(f'{packet_number:04d}'.encode() + packet, (HOST, PORT))
        send_time = time.time()  # Record the time when the packet is sent
        print(f"Packet {packet_number} sent.")  # Print message indicating packet is sent
        
        # Wait for acknowledgment
        while True:
            try:
                sock.settimeout(dynamic_timeout)  #timeout for waiting for ack
                data, _ = sock.recvfrom(BUFFER_SIZE)
                ack_num = int(data.decode())

                if ack_num == packet_number and not acknowledged_packets[ack_num]:
                    recv_time = time.time()  # Record the time when the acknowledgment is received
                    delay = recv_time - send_time  # Calculate the delay
                    delays.append(delay)

                    acknowledged_packets[ack_num] = True # mark packet as acknowledged
                    print(f"Acknowledgement received for packet {packet_number}, Delay: {delay:.9f} seconds")
                    break # Break out of the inner loop if acknowledgement is correct.

                elif ack_num == packet_number:
                    print(f"Duplicate ack received for packet {ack_num}")
                else:
                    print(f"Out of order ack received: {ack_num}")
            except socket.timeout:
                print(f"Timeout! Resending packet {packet_number}")
                break # Exit the inner loop and resend the current packet

            average_delay = sum(delays) / len(delays) if delays else 0
            dynamic_timeout = average_delay * 2  #double the average delay to accomodate disturbance
            sock.settimeout(dynamic_timeout)

# Send a final message indicating all packets have been sent
sock.sendto(b'EOF', (HOST, PORT))

# Stop the timer
end_time = time.time()

# Close the socket
sock.close()

# Calculate and print the total time taken
total_time = end_time - start_time
print(f"Image successfully sent in {total_time:.3f} seconds.")
