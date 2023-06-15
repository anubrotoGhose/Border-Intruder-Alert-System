import cv2
from detection_and_tracking import *
import datetime
# import pygame

ob1 = DetectionAndTracking("https://192.168.130.40:8080/video",0)
# ob1.main()

ob2 = DetectionAndTracking("https://192.168.130.201:8080/video",1)
# ob2.main()

# ob3 = Detection("https:// /video")
# ob3.main()

# ob4 = Detection("https:// /video")
# ob4.main()

# Python program to illustrate the concept
# of threading
# importing the threading module
import threading
import multiprocessing


# def print_cube(num):
# 	# function to print cube of given num
# 	print("Cube: {}" .format(num * num * num))


# def print_square(num):
# 	# function to print square of given num
# 	print("Square: {}" .format(num * num))
# t1 = multiprocessing.Process(target=ob1.main(), args=())
# t2 = multiprocessing.Process(target=ob2.main(), args=())
t1 = threading.Thread(target=ob1.main(), args=())
t2 = threading.Thread(target=ob2.main(), args=())

if __name__ == "__main__":
	# creating thread
	

	# starting thread 1
	t1.start()
	# starting thread 2
	t2.start()

	# # wait until thread 1 is completely executed
	t1.join()
	# # wait until thread 2 is completely executed
	t2.join()

	

	# both threads completely executed
	print("Done!")
