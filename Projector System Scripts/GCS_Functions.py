import socket
import base64
import io
from PIL import Image
import colorsys
import math
import numpy as np


class Point: 
    def __init__(self, x, y): 
        self.x = x
        self.y = y


def generate_image(height, width, mu_x, mu_y, sigma_x, sigma_y, saturation, value):

    filename = "test_dist.png"

    pixelArray = [[0 for i in range(width)] for j in range(height)]
    for x in range(height):
        for y in range(width):
            pixelArray[x][y] = hue2rgb(xyFunction(x, y, mu_x, mu_y, sigma_x, sigma_y), saturation, value)

    img = Image.fromarray(np.array(pixelArray), mode="RGB")
    img.save(filename)


def generate_image_with_rot(height, width, mu_x, mu_y, sigma_x, sigma_y, saturation, value, theta, scale_factor, invert):

    filename = "test_dist.png"

    pixelArray = [[0 for i in range(width)] for j in range(height)]
    for x in range(height):
        for y in range(width):
            newPoint = calc_rot_point(x, y, mu_x, mu_y, theta)
            pixelArray[x][y] = hue2rgb(xyFunction(newPoint.x, newPoint.y, mu_x, mu_y, sigma_x, sigma_y), saturation, value, scale_factor, invert)

    img = Image.fromarray(np.array(pixelArray), mode="RGB")
    img.save(filename)


def calc_rot_point(x,y, mu_x, mu_y, theta):

    # Translate mean to origin
    newX = x - mu_x
    newY = y - mu_y

    # Perform rotation
    newX = newX * math.cos(theta) - newY * math.sin(theta)
    newY = newX * math.sin(theta) + newY * math.cos(theta)

    # Translate mean back to original position
    newX = newX + mu_x
    newY = newY + mu_y

    return Point(newX, newY)


def xyFunction(x, y, mu_x, mu_y, sigma_x, sigma_y):
    A = 2 * math.pi * (sigma_x ** 2) * (sigma_y ** 2)
    B = (x - mu_x) ** 2
    C = 2 * (sigma_x ** 2)
    D = (y - mu_y) ** 2
    F = 2 * (sigma_y ** 2)
    return math.exp(-((B/C) + (D/F)))


def hue2rgb(hue, saturation, value, scale_factor, invert):
    if invert:
        hue = scale_factor - hue*scale_factor
    else:
        hue = hue*scale_factor
    return tuple(np.uint8(component * 255) for component in colorsys.hsv_to_rgb(hue, saturation, value))


def split_image(image_path):

    # Open the original image
    original_image = Image.open(image_path)

    # Get the dimensions of the original image
    width, height = original_image.size

    # Calculate the size of each cut image (1280x800)
    cut_width, cut_height = width/2, height/2

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
        UDP_IP_1 = "192.168.1.11"
        UDP_PORT = 16690
        print(f"UDP target IP: {UDP_IP_1}"),
        print (f"UDP target port: {UDP_PORT}"),
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        sock.sendto(Encoded_Image_1, (UDP_IP_1, UDP_PORT))
        print("Message1 Sent")
        
        #Send to second PI
        UDP_IP_2 = "192.168.1.12"
        print(f"UDP target IP: {UDP_IP_2}"),
        print (f"UDP target port: {UDP_PORT}"),
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        sock.sendto(Encoded_Image_2, (UDP_IP_2, UDP_PORT))
        print("Message2 Sent")
        
        #Send to third PI
        UDP_IP_3 = "192.168.1.13"
        print(f"UDP target IP: {UDP_IP_3}"),
        print (f"UDP target port: {UDP_PORT}"),
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        sock.sendto(Encoded_Image_3, (UDP_IP_3, UDP_PORT))
        print("Message3 Sent")
        
        #Send to fourth PI
        UDP_IP_4 = "192.168.1.14"
        print(f"UDP target IP: {UDP_IP_4}"),
        print (f"UDP target port: {UDP_PORT}"),
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        sock.sendto(Encoded_Image_4, (UDP_IP_4, UDP_PORT))
        print("Message4 Sent")
        
