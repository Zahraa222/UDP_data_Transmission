import socket
import traceback
import time


#look into time library and its resolution


HOST = '0.0.0.0'    # listening
PORT = 1234         # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 1024  # Buffer size
PAUSE_PACKET_NUMBER = 10
PAUSE_TIME = 6
PACKET_COUNT = 0


# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Socket was created")
sock.bind((HOST, PORT))

print(f"Server listening on {HOST}:{PORT}")
received_packets = {}

seen_packets = set()

try:
    while True:
        # Receive packet
        data, address = sock.recvfrom(BUFFER_SIZE + 4)  # plus 4 for the packet number
        

        if data.startswith(b'EOF'):
            # All packets received, assemble the image
            image_data = b''.join(received_packets[number] for number in sorted(received_packets))
            with open('received_image.jpg', 'wb') as img_file:
                img_file.write(image_data)
            print("Image successfully received and reassembled. Ready to open.")
            break
        
        if PACKET_COUNT == PAUSE_PACKET_NUMBER:
            print("Pausing packet processing to simulate server timeout...")
            time.sleep(PAUSE_TIME)
            print("Resuming packet processing...")

        
        # Extract packet number
        packet_number = int(data[:4])

        if packet_number in seen_packets:
            print(f"Duplicate packet {packet_number} received, ignoring")
            continue #skip processing this packet

        seen_packets.add(packet_number) #mark this packet as seen
        received_packets[packet_number] = data[4:]
        PACKET_COUNT += 1

        
        # Display received packet message
        print(f"Packet {packet_number} received from {address}")

        # Send back receipt acknowledgment
        sock.sendto(f'{packet_number:04d}'.encode(), address)
        print(f"Acknowledgment sent for packet {packet_number}")


except Exception as e:
    print("An error occurred:")
    traceback.print_exc()

finally:
    # Close the socket
    sock.close()
