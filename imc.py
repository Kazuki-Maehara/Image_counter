#! /usr/bin/env python3
# coding = utf-8

import cv2
import time
import sys,os
from imc_modules.camera_setup import camera_setup 
from imc_modules.get_biggest_contour import get_biggest_contour
from imc_modules.get_ins_points import get_ins_points
from imc_modules.inspect_image import inspect_image
from imc_modules.plot_circles import plot_circles
from imc_modules.add_csv import add_csv

#Camera's parameters
CAM_DEVNO = 2
CAM_FPS = 5 
CAM_WIDTH = 1280
CAM_HEIGHT = 720
CAM_EXPOSURE = str(100)


#directorys of saving data
IMAGE_DIRECTORY = './images/circled.jpg'
CSV_DIRECTORY = './csv/'
CONTSIZE_THRESH = 300


def setup():

    #get a image by USB camera
    capture = cv2.VideoCapture(CAM_DEVNO)
    if capture.isOpened() is False:
        raise("IO Error")

    os.system('v4l2-ctl -d /dev/video2 -c exposure_auto=1')
    os.system('v4l2-ctl -d /dev/video2 -c white_balance_temperature_auto=0')
    os.system('v4l2-ctl -d /dev/video2 -c exposure_absolute=' + CAM_EXPOSURE)

    capture.set(cv2.CAP_PROP_FPS, CAM_FPS)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
    return capture

#def indicator():



def main(capture):

    #set and initialize arguments
    C_FLAG = True
    filled_count = 0
    blank_count = 0
    con_counter = 1
    elapsed_time = 0.

    #set up the USB camera, get HSV range
    lower_hsv, upper_hsv, INI_BIG_CONTOUR = camera_setup(capture) 

    while True:
        
        #get while-cycle start time
        start_time = time.time()

        #get a image from video capture
        ret, image = capture.read()
        if ret is False:
            print('capture read error')
            continue
        
        #get a most biggest contour; e.g. container 
        biggest_contour, image_gauss_blur = get_biggest_contour(lower_hsv, upper_hsv, image)
        

        #get a inspection points
        ins_points = get_ins_points(biggest_contour) 
        
        
        if (ins_points[:,:,0].max() > CAM_WIDTH) or (ins_points[:,:,0].min() < 0) or (ins_points[:,:,1].max() > CAM_HEIGHT) or (ins_points[:,:,1].min() < 0):
            continue

        #inspect a blurred image
        ins_results, filled_count, blank_count = inspect_image(ins_points, image_gauss_blur)

        #plot circles on a image
        image =  plot_circles(ins_results, ins_points, image)
       


        #set C_FLAG True when a container is changed
        if (C_FLAG is True) & (biggest_contour.size > (INI_BIG_CONTOUR.size - CONTSIZE_THRESH)) & (biggest_contour.size < (INI_BIG_CONTOUR.size + CONTSIZE_THRESH)) & (filled_count < 72):
            C_FLAG = False
            print('\nStart counting')

        elif (C_FLAG is False) & (filled_count == 72):
           
            #write counts in a buffer
            sys.stdout.write('\r\033[Kfilled = ' + str(filled_count))
            sys.stdout.write(', blank = ' + str(blank_count))
            #write progress-bar in a buffer
            bar_len = int(30 * filled_count / 72)
            sys.stdout.write('   [' + '=' * bar_len +
                            ('>' if bar_len < 30 else '') +
                            ' ' * (30 - bar_len) +
                            '] %.1f%%' % ((filled_count / 72) * 100.))
            sys.stdout.write('   e-time = ' + str(int(elapsed_time*1000)) + ' ms')
            sys.stdout.write('   con-value = ' + str(biggest_contour.size))
            #flush a buffer
            sys.stdout.flush()

            #write a original image
            cv2.imwrite(IMAGE_DIRECTORY, image)
            print('\nThe image was written : ' + IMAGE_DIRECTORY)
            #add to csv file
            add_csv(CSV_DIRECTORY, con_counter)
            print('Data was written ; ' + CSV_DIRECTORY)
            con_counter = con_counter + 1
            print('The container should be changed')
            C_FLAG = True

        elif (C_FLAG is False) & (filled_count < 72):
            #write counts in a buffer
            sys.stdout.write('\r\033[Kfilled = ' + str(filled_count))
            sys.stdout.write(', blank = ' + str(blank_count))
            #write progress-bar in a buffer
            bar_len = int(30 * filled_count / 72)
            sys.stdout.write('   [' + '=' * bar_len +
                            ('>' if bar_len < 30 else '') +
                            ' ' * (30 - bar_len) +
                            '] %.1f%%' % ((filled_count / 72) * 100.))
            sys.stdout.write('   e-time = ' + str(int(elapsed_time*1000)) + ' ms')
            sys.stdout.write('   con-value = ' + str(biggest_contour.size))
            #flush a buffer
            sys.stdout.flush()
        


        #show the window of capture image
        cv2.namedWindow('Capture', cv2.WINDOW_NORMAL)
        cv2.imshow('Capture', image)
        


        #get while-cycle elapsed time
        elapsed_time = time.time() - start_time
        if elapsed_time >= (1/CAM_FPS): 
            print('\nError : Cycle-time is too long to run this program')
            print('Closing the program...\n')
            break


        if cv2.waitKey(delay=(int(1000/CAM_FPS)-int(elapsed_time * 1000))) >= 0:
            break


        #for test program, error
        #raise NameError('program is done')

    print('\n\n\nClosing the program...')
    print('Good bye..........\n\n\n')
    capture.release()
    cv2.destroyAllWindows()





if __name__ == '__main__':
    capture = setup()
    main(capture)

