#! /usr/bin/env python3
# coding = utf-8


import cv2
import numpy as np
from imc_modules.get_biggest_contour import get_biggest_contour
MASK_RED = (0,0,255)
MASK_GREEN = (0,255,0)
MASK_BLUE = (255,0,0)


def camera_setup(capture):
    

    cv2.namedWindow("Capture", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("Masked image", cv2.WINDOW_AUTOSIZE)

    def nothing(x):
        pass

    cv2.createTrackbar('H_max', 'Masked image', 0, 255, nothing)
    cv2.createTrackbar('H_min', 'Masked image', 0, 255, nothing)
    cv2.createTrackbar('S_max', 'Masked image', 0, 255, nothing)
    cv2.createTrackbar('S_min', 'Masked image', 0, 255, nothing)
    cv2.createTrackbar('V_max', 'Masked image', 0, 255, nothing)
    cv2.createTrackbar('V_min', 'Masked image', 0, 255, nothing)
   

    cv2.setTrackbarPos('H_max', 'Masked image', 255)
    cv2.setTrackbarPos('S_max', 'Masked image', 255)
    cv2.setTrackbarPos('V_max', 'Masked image', 255)



    while True:
        ret, image = capture.read()
        if ret == False:
            continue
        src_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_hsv = np.array([cv2.getTrackbarPos('H_min', 'Masked image'),cv2.getTrackbarPos('S_min', 'Masked image'),cv2.getTrackbarPos('V_min', 'Masked image')])
        upper_hsv = np.array([cv2.getTrackbarPos('H_max', 'Masked image'),cv2.getTrackbarPos('S_max', 'Masked image'),cv2.getTrackbarPos('V_max', 'Masked image')])

        blur = cv2.GaussianBlur(src_hsv, (5,5), 3)
        #blur = cv2.blur(src_hsv, (5,5))
        #blur = cv2.medianBlur(src_hsv, 5)
        src_mask = cv2.inRange(blur, lower_hsv, upper_hsv)
        masked_image = cv2.bitwise_and(src1 = image, src2 = image, mask = src_mask)

        src_mask_not = cv2.bitwise_not(src = src_mask)
        colored_image = np.zeros((masked_image.shape[0],masked_image.shape[1],3), dtype=np.uint8)
        colored_image[:] = MASK_GREEN
        colored_mask = cv2.bitwise_or(src1 = masked_image, src2 = colored_image, mask = src_mask_not)
        masked_image = masked_image + colored_mask

        cv2.imshow("Capture", image)
        cv2.imshow("Masked image", masked_image)

        if cv2.waitKey(delay=50) >= 0:
            cv2.imwrite("./images/setup_mask_image.jpg", masked_image)
            initial_biggest_contour, image_gauss_blur = get_biggest_contour(lower_hsv, upper_hsv, image)

            break
    
    
    del blur
    del masked_image
    del src_mask
    del src_hsv
    cv2.destroyAllWindows()
    return lower_hsv, upper_hsv, initial_biggest_contour 




if __name__ == "__main__":
    img_mask()


