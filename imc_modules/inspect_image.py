#! /usr/bin/env python3
# coding = utf-8

import cv2
import numpy as np

SET_THRESHOLD = 60
TRIM_SIZE = 10

def inspect_image(ins_points, image_gauss_blur):
    
    #convert a gauss blurred image to gray scale
    gauss_gray = cv2.cvtColor(image_gauss_blur, cv2.COLOR_BGR2GRAY)




    #make a 12 * 6 list, all of its value is False
    ins_results = [[False for i in range(6)] for j in range (12)]

    #inspect each ins_points in thresh_ins
    for m in range(12):
        for n in range(6):
            if np.mean(gauss_gray[ins_points[m,n,1] - int(TRIM_SIZE / 2):ins_points[m,n,1] + int(TRIM_SIZE / 2),ins_points[m,n,0] - int(TRIM_SIZE / 2):ins_points[m,n,0] + int(TRIM_SIZE / 2)]) < SET_THRESHOLD:
                ins_results[m][n] = True
    

    #count up filled and blank cells
    filled_count = 0
    blank_count = 0
    for m in range(12):
        for n in range(6):
            if ins_results[m][n] == True:
                filled_count = filled_count + 1
            else:
                blank_count = blank_count + 1

    return ins_results, filled_count, blank_count

