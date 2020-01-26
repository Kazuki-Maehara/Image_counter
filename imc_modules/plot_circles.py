#! /usr/bin/env python3
# coding = utf8

import cv2
CIRCLE_RADIUS = 15
CIRCLE_GREEN = (0,255,0)
CIRCLE_RED = (0,0,255)
CIRCLE_THICKNESS = 3

def plot_circles(ins_results, ins_points, image):
    #plot circles; filled = green, blank = red
    for m in range(12):
        for n in range(6):
            if ins_results[m][n] == True:
                image = cv2.circle(image, tuple(ins_points[m][n]), CIRCLE_RADIUS, CIRCLE_GREEN, CIRCLE_THICKNESS)
            else:
                image = cv2.circle(image, tuple(ins_points[m][n]), CIRCLE_RADIUS, CIRCLE_RED, CIRCLE_THICKNESS)
    
    return image
