import cv2
from tracker import *
import datetime
import pygame
# Create tracker object

class DetectionAndTracking:
    def __init__(self,address,n):
        self.tracker = EuclideanDistTracker()
        self.address = address
        self.cap = cv2.VideoCapture(n)
        self.cap.open(address)
        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

        # Create background subtractor object
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2()

        #initialize pygame mixer
        pygame.init()
        self.alarm_sound = pygame.mixer.Sound("C:\\Users\\anubr\\Documents\\Inter Fall Semester 22-23\\IOT Project\\Code\\alarm.wav")
        self.alarm_channel = pygame.mixer.Channel(1)

        # Object detection from Stable camera
    

        # Set threshold for motion detection
        self.threshold = 10
        self.alarm_status = False

        # Set motion threshold
        self.motion_threshold = 2
        self.min_area = 500

        # Set time threshold (seconds)
        self.time_threshold = 2
    
    

    
    

    def disarm_alarm(self,x):
        global alarm_status
        # self.alarm_channel.stop()
        alarm_status = False
        print("Alarm Disarmed")


    def alarm_control(self,contours):
        global alarm_status
        # initialize variables to keep track of motion
        motion = 0
        total_area = 0
        for contour in contours:
            if cv2.contourArea(contour) > self.min_area:
                (x, y, w, h) = cv2.boundingRect(contour)
                total_area += w*h
                motion += 1
        if motion > self.motion_threshold and total_area > self.min_area:
            if not alarm_status:
                self.alarm_channel.play(self.alarm_sound)
                alarm_status = True
                print("Motion detected, alarm ON!")
        else:
            # self.alarm_channel.stop()
            alarm_status = False
            print("No motion detected, alarm OFF")
        return alarm_status
    
    def main(self):
        cv2.namedWindow("Alarm")
        cv2.createTrackbar("Disarm", "Alarm", 0, 1, self.disarm_alarm)
        last_motion_time = datetime.datetime.now()

        while True:
            ret, frame = self.cap.read()
            height, width, _ = frame.shape

            # check if 'q' is pressed
            if cv2.waitKey(1) and (0xFF == ord('q') or 0xFF == ord('Q')):
                break


            # Extract Region of interest
            # roi = frame[340: 720,500: 800]
            roi = frame[0:int(height),0:int(width)]
            # 1. Object Detection

            # Apply background subtraction to frame
            foreground_mask = self.background_subtractor.apply(frame)

            # threshold the mask to identify motion regions
            thresholded_mask = cv2.threshold(foreground_mask, self.threshold, 255, cv2.THRESH_BINARY)[1]
            
            mask = self.object_detector.apply(frame)
            _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            detections = []

            alarm_status = self.alarm_control(contours)
            if alarm_status:
                last_motion_time = datetime.datetime.now()
            else:
                # check if alarm has been on for more than time_threshold seconds
                if (datetime.datetime.now() - last_motion_time).seconds > self.time_threshold:
                    self.alarm_channel.stop()
                    alarm_status = False
                    print("Alarm OFF")


            for cnt in contours:
                # Calculate area and remove small elements
                area = cv2.contourArea(cnt)
                if area > 100:
                    #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                    x, y, w, h = cv2.boundingRect(cnt)
                    

                    detections.append([x, y, w, h])

            # 2. Object Tracking
            boxes_ids = self.tracker.update(detections)
            for box_id in boxes_ids:
                x, y, w, h, id = box_id
                cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

            
            # show alarm status on the frame
            if alarm_status:
                cv2.putText(frame, "Alarm ON!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "Alarm OFF", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


            # cv2.imshow("roi", roi)
            cv2.imshow("Frame", frame)
            cv2.imshow("Mask", mask)
            # width = 320
            # height = 320
            # cv2.resizeWindow(frame, width, height)

            # image = cv2.resize(frame, (200, 100))
            # cv2.imshow("image", image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            
            key = cv2.waitKey(30)
            if key == 27:
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
