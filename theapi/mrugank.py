import cv2
import numpy as np
import sys
import requests

def main():
    cam = cv2.VideoCapture(0)
    #cam = cv2.VideoCapture("http://192.168.43.1:8080/video")
    pixel_count = 10
    pixel_intensity = 10
    window = 'Original'
    filename = 'Original.avi'
    filename_b = 'Blue.avi'
    filename_g = 'Green.avi'
    filename_r = 'Red.avi'
    codec = cv2.VideoWriter_fourcc('X','V','I','D')
    '''framerate = 24
    resolution = (640,480)
    video_orginal = cv2.VideoWriter(filename, codec, framerate, resolution)
    video_blue = cv2.VideoWriter(filename_b, codec, framerate, resolution)
    video_green = cv2.VideoWriter(filename_g, codec, framerate, resolution)
    video_red = cv2.VideoWriter(filename_r, codec, framerate, resolution)'''
    '''if cam.isOpened():
        ret, frame = cam.read()
        print(ret)
    else:
        ret = False
        #print(ret)
        #break'''
    while True:
        ret, frame = cam.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #tracking of blue color
        low = np.array([100, 50, 50])
        high = np.array([140, 255, 255])

        #tracking of green color
        low_green = np.array([40, 50, 50])
        high_green = np.array([80, 255, 255])

        #tracking of red color
        low_red = np.array([140, 150, 0])
        high_red = np.array([180, 255, 255])

        #binary matrix
        image_mask = cv2.inRange(hsv, low, high)
        image_mask_green = cv2.inRange(hsv, low_green, high_green)
        image_mask_red = cv2.inRange(hsv, low_red, high_red)

        #display image_mask
        #cv2.imshow('image mask', image_mask)

        #output after and operation
        output_blue = cv2.bitwise_and(frame, frame, mask = image_mask)
        output_green = cv2.bitwise_and(frame, frame, mask = image_mask_green)
        output_red = cv2.bitwise_and(frame, frame, mask = image_mask_red)
        output_blue = cv2.resize(output_blue, (100,100))
        output_green = cv2.resize(output_green, (100,100))
        output_red = cv2.resize(output_red, (100,100))
        #print('output_green', output_green)
        #print('output_red', output_red)

        #display the output
        #cv2.imshow('Output_blue', output_blue)
        #cv2.imshow('Output_green', output_green)
        #cv2.imshow('Output_red', output_red)
        #cv2.imshow('Output_green', output_green)
        cv2.imshow(window, frame)
        counter = 0
        for i in range(100):
            left = output_red[i][49]
            right = output_green[i][49]
            if left[2] > pixel_intensity:
                #continue
                counter += 1
                if left[2] > pixel_intensity and counter > pixel_count:
                    counter = 0
                    #print('red',left[2])
                    print('entered')
                    r = requests.get(url = 'http://127.0.0.1:8000/bot-api/', params = {"direction":"left"})
                    #print (left[2])
                    sys.stdout.flush()
                    #return False
                #print(counter)
                continue
            elif right[1] > pixel_intensity:
                #continue
                counter += 1
                if right[1] > pixel_intensity and counter > pixel_count:
                    counter = 0
                    #print('green',right[1])
                    print('entered')
                    r = requests.get(url = '127.0.0.1:8000/bot-api/', params = {"direction":"right"})
                    #print (right[1])
                    sys.stdout.flush()
                    #return True
                #print(counter)
                continue

        #save videos
        '''video_orginal.write(frame)
        video_blue.write(output_blue)
        video_green.write(output_green)
        video_red.write(output_red)'''

        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()
    cam.release()

if __name__ == '__main__':
    main()
