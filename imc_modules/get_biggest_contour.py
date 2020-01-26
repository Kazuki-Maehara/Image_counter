#! /usr/bin/env python3
# coding = utf-8


import cv2
import numpy as np




def get_biggest_contour(lower_hsv, upper_hsv, image):
    
    #effect gaussian blur to a BGR image
    image_gauss_blur = cv2.GaussianBlur(image, (5,5), 3)

    #convert blurred BGR image to hsv
    image_hsv = cv2.cvtColor(image_gauss_blur, cv2.COLOR_BGR2HSV)

    #make the mask image by the range
    a_mask = cv2.inRange(image_hsv, lower_hsv, upper_hsv)

    #make a conjunction image by the mask
    masked_image = cv2.bitwise_and(image, image, mask = a_mask)
    
    #convert masked image to gray scale
    masked_image_gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)

    #binalization of image
    ret, thresh = cv2.threshold(masked_image_gray, 0 ,255, cv2.THRESH_BINARY)
    
    #find contours
    imgEdge, contours, hierarchu = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #find a most biggest contours
    greater_size = contours[0].size
    greater_index = 0
    for n in range(1, len(contours)):
        if greater_size < contours[n].size:
            greater_size = contours[n].size
            greater_index = n

    return contours[greater_index], image_gauss_blur
    





if __name__ == "__main__":
    get_biggest_contour()


