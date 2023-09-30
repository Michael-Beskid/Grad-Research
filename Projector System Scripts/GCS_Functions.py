import socket
import base64
import io
from PIL import Image

def split_image(image_path):

    # Open the original image
    original_image = Image.open(image_path)

    # Get the dimensions of the original image
    width, height = original_image.size

    # Calculate the size of each cut image (1280x800)
    cut_width, cut_height = 1280, 800

    #Define empty binary images
    binary_images = []

    # Create four cut images
    for row in range(2):
        for col in range(2):
            # Calculate the region to crop for each cut image
            left = col * cut_width
            upper = row * cut_height
            right = left + cut_width
            lower = upper + cut_height

            # Crop the region and save as a new PNG
            split_image = original_image.crop((left, upper, right, lower))

            # Create a BytesIO object to store the binary data
            img_byte_array = io.BytesIO()

            # Save the cropped image to the BytesIO object
            split_image.save(img_byte_array, format='PNG')

            # Append the binary data to the list
            binary_images.append(img_byte_array.getvalue())

    return binary_images



# Function to encode in base64 format for UDP transmission
def Encode_Image(data):
    
    Encoded_Image_1 = base64.b64encode(data[0])
    Encoded_Image_2 = base64.b64encode(data[1])
    Encoded_Image_3 = base64.b64encode(data[2])
    Encoded_Image_4 = base64.b64encode(data[3])
    return(Encoded_Image_1,Encoded_Image_2,Encoded_Image_3,Encoded_Image_4)


#Function to send image to selected UDP port
def UDP_SEND(Encoded_Image_1,Encoded_Image_2,Encoded_Image_3,Encoded_Image_4):
    while True:
        #Send to first PI
        UDP_IP_1 = "192.168.1.80"
        UDP_PORT = 16690
        print(f"UDP target IP: {UDP_IP_1}"),
        print (f"UDP target port: {UDP_PORT}"),
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        sock.sendto(Encoded_Image_1, (UDP_IP_1, UDP_PORT))
        print("Message1 Sent")
        
        #Send to second PI
        UDP_IP_2 = "192.168.1.80"
        print(f"UDP target IP: {UDP_IP_2}"),
        print (f"UDP target port: {UDP_PORT}"),
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        sock.sendto(Encoded_Image_2, (UDP_IP_2, UDP_PORT))
        print("Message2 Sent")
        
        #Send to third PI
        UDP_IP_3 = "192.168.1.80"
        print(f"UDP target IP: {UDP_IP_3}"),
        print (f"UDP target port: {UDP_PORT}"),
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        sock.sendto(Encoded_Image_3, (UDP_IP_3, UDP_PORT))
        print("Message3 Sent")
        
        #Send to fourth PI
        UDP_IP_4 = "192.168.1.80"
        print(f"UDP target IP: {UDP_IP_4}"),
        print (f"UDP target port: {UDP_PORT}"),
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        sock.sendto(Encoded_Image_4, (UDP_IP_4, UDP_PORT))
        print("Message4 Sent")
        
