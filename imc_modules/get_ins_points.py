#! /usr/bin/env python3
# coding = utf-8

import cv2
import numpy as np

def get_ins_points(biggest_contour):

    #set outer rectangle
    outer_rect = cv2.minAreaRect(biggest_contour)
    
    #set inner rectangle
    inner_rect = (outer_rect[0], (outer_rect[1][0]*0.72069, outer_rect[1][1]*0.76781), outer_rect[2])
    #set inspection box
    ins_box = cv2.boxPoints(inner_rect)
    
    #calculate inspection points
    ins_points = np.zeros((12,6,2))
    dist21 = ins_box[2] - ins_box[1]
    dist01 = ins_box[0] - ins_box[1]
   
    if np.linalg.norm(dist21) >= np.linalg.norm(dist01): 
        ins_points[0,0] = ins_box[1]
        ins_points[11,0] = ins_box[0]
        ins_points[0,5] = ins_box[2]
        step_column = (ins_box[2]-ins_box[1])/5
        step_row = (ins_box[0]-ins_box[1])/11

    else:
        ins_points[0,0] = ins_box[2]
        ins_points[11,0] = ins_box[1]
        ins_points[0,5] = ins_box[3]
        step_column = (ins_box[3]-ins_box[2])/5
        step_row = (ins_box[1]-ins_box[2])/11
        

    for m in range(12):
        ins_points[m,0] = ins_points[0,0] + (m * step_row)
        for n in range(6):
            ins_points[m,n] = ins_points[m,0] + (n * step_column)
    
    #truncates to integer about ins_points
    ins_points = ins_points.astype(int)

    return ins_points





if __name__ == '__main__':
    get_ins_points()

