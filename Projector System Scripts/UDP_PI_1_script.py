import socket
import base64
import matplotlib.pyplot as plt
import io

UDP_IP = "192.168.1.10"
UDP_PORT = 16690

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    
    encoded_message, addr = sock.recvfrom(30000)  # buffer size is 1024 bytes
    Projection = base64.b64decode(encoded_message)
    
    image_stream = io.BytesIO(Projection)

    # Open the image using Matplotlib
    image = plt.imread(image_stream)

    # Display the image
    plt.imshow(image)
    plt.axis('off')
    plt.show()