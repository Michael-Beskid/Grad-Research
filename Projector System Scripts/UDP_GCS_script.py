## This script is meant to be run on the ground control station to publish the images to the headless PIs via UDP
import GCS_Functions as GCS

#Load Image From Image Generator
#with open('Projection.png', 'rb') as file:
#    data = file.read()
#print(len(data))

# Call function to split projection image and return 4 PNGs
Images = GCS.split_image('projection.png')

# Call encoding function to prepare image data for UDP transmission
UDP_Message = GCS.Encode_Image(Images)

# Function to send the message via udp
GCS.UDP_SEND(UDP_Message[0],UDP_Message[1],UDP_Message[2],UDP_Message[3])


