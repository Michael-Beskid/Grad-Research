## This script is meant to be run on the ground control station to publish the images to the headless PIs via UDP
import math
import GCS_Functions as GCS

#Load Image From Image Generator
#with open('Projection.png', 'rb') as file:
#    data = file.read()
#print(len(data))

# NOTE: Need to cut image size in half for this to work at the moment... increase buffer or use different method than UDP

# THREAT FIELD PARAMETERS
img_height = 800
img_width = 1280
mu_x = 250
mu_y = 300
sigma_x = 150
sigma_y = 400
saturation = 0.8
value = 1.0
theta = math.pi/12
scale_factor = 0.8
invert = False


# Generate Gaussian threat field
# GCS.generate_image(800, 1280, 250, 400, 200, 400, 0.6, 0.9)   # Good distribution
# GCS.generate_image(800, 1280, 100, 100, 60, 180, 0.8, 1.0)      # Temp distribution for 1 projector
GCS.generate_image_with_rot(img_height, img_width, mu_x, mu_y, sigma_x, sigma_y, saturation, value, theta, scale_factor, invert)      # Temp distribution for 1 projector

# Split image and return 4 PNGs
Images = GCS.split_image('test_dist.png')

# Call encoding function to prepare image data for UDP transmission
UDP_Message = GCS.Encode_Image(Images)

# Function to send the message via udp
GCS.UDP_SEND(UDP_Message[0],UDP_Message[1],UDP_Message[2],UDP_Message[3])


