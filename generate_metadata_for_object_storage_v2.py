#!/usr/bin/env python


import os
import subprocess
import time
from time import sleep
import io

from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "<INSERT PATH TO CREDS HERE>"

# This file will make a swiftcall against the swiftstack container
# pull the object names from the container and put them in a list
# Take that list and fill in the URL portion of the request.json template

# setting variables (lists)
object_name_list = []
opened_file_content = []
diff_in_objects = []

def run_swift_list_command_to_get_objects():
	p = subprocess.check_output(['swift', 'list', 'images']).splitlines()
	for i in p:
		object_name_list.append(i)
	return object_name_list


def get_container_object_names_and_generate_uri_and_command_to_run():

	# returns all the object names from the test_images container
	run_swift_list_command_to_get_objects()

	# if the list of objects file doesn't exist, create it, write the objects to it, close it, loop through all the objeects in the container and put into list, generate swift command from objects in list, run metadata function against Google vision API and return metadata parsed into args for command, join the commmand together and run the command
	if not os.path.exists("./object_tracking_file.txt"):

		create_object_tracking_file = open("object_tracking_file.txt", "w+")
		
		for item in object_name_list:
			create_object_tracking_file.write("%s\n" % item)
		create_object_tracking_file.close()


		print "File did not exist to we created a new one! This is the initial run so no objects will be forgotten this time around!!\n"


		for i in object_name_list:
			uri = "https://<YOUR BUCKET DOMAIN HERE>/images/%s" % (i)
			command = "swift post images %s" % (i)
			
			# gets the metadata back from the URI into a list to be added to command, creates a string from the two parts of the commands and runs it against SwiftStack API
			get_google_vision_data_and_return_metadata_args = detect_web_uri(uri)
			get_metadata_from_object_RUN = get_metadata_from_object(get_google_vision_data_and_return_metadata_args)

			# creating new command to run against the cluster
			new_command = "swift post images ", i, get_metadata_from_object_RUN
			new_command_string = ''.join(new_command)
			print new_command_string, "\n"
			subprocess.check_output([new_command_string], shell=True)

	else:
		print "object file exists so we'll compare it for you!"
		with open("object_tracking_file.txt") as opened_object_file_to_list:
			opened_file_content = opened_object_file_to_list.readlines()
		opened_file_content = [x.strip() for x in opened_file_content] 

		print "These are the current objects in the list file: ", opened_file_content


		for i in object_name_list:
			if i not in opened_file_content:
				with open ("object_tracking_file.txt", "a") as tester:
					tester.write(i)
					tester.write("\n")

				uri = "https://https://<YOUR BUCKET DOMAIN HERE>/images/%s" % (i)
				command = "swift post images %s" % (i)
				diff_in_objects.append(i)
				
				# gets the metadata back from the URI into a list to be added to command, creates a string from the two parts of the commands and runs it against SwiftStack API
				get_google_vision_data_and_return_metadata_args = detect_web_uri(uri)
				get_metadata_from_object_RUN = get_metadata_from_object(get_google_vision_data_and_return_metadata_args)

				# creating new command to run against the cluster
				new_command = "swift post images ", i, get_metadata_from_object_RUN
				new_command_string = ''.join(new_command)
				print new_command_string, "\n"
				subprocess.check_output([new_command_string], shell=True)
				tester.close()
		if diff_in_objects:
			print "\nHere are the new objects that have been added to your container and ran against the Google vision API:\t", diff_in_objects


# This runs the URI against the Google Vision API and returns the list of descriptive elemenents that we will attach to the image metadata
def detect_web_uri(uri):
    """Detects web annotations in the file located in Google Cloud Storage."""
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.web_detection(image=image)
    annotations = response.web_detection
    list_of_metadata_for_object = []

    if annotations.web_entities:
        for entity in annotations.web_entities:
        	list_of_metadata_for_object.append('{}'.format(entity.description))

    return list_of_metadata_for_object


# goes through the list of returned metadata from Google Vision API and parses them into command args 
def get_metadata_from_object (list_of_metadata_for_object):
    counter = 0
    command_plus_metadata = ""
    for value in list_of_metadata_for_object:
    	pop = value.replace(" ","_").replace("'","")
    	hello = " -m mldata%d:%s " % (counter, pop)

    	command_plus_metadata+=hello
    	counter+=1

    return command_plus_metadata
	

# Run the program
if __name__ == "__main__":
	get_container_object_names_and_generate_uri_and_command_to_run()


	
