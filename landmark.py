import os
import time
import cv2 as cv
import pandas as pd
from save_csv import save

class Main:
    def __init__(self, imagePath, w_name='image',image_name=None, iteration=False):
        self.iteration = iteration
        self.image_name = image_name
        self.imagePath = imagePath 
        self.windowName = w_name
        self.font = cv.FONT_HERSHEY_SIMPLEX
        self.line_type = cv.LINE_AA
        self.count = 0
        self.color = (255, 255, 255)
        self.co_ordinate = []

        cv.namedWindow(self.windowName)
        # Create a track bar for the point
        cv.createTrackbar('colorP', self.windowName, 0, 3, self.trackbar)

    
    # Callback function for trackbar that select the color 
    def trackbar(self, x):
        print(x)
        if x == 0:
            self.color = (100, 0, 0)
        elif x == 1:
            self.color = (255, 0, 0)
        elif x == 2:
            self.color = (0, 255, 0)
        elif x == 3:
            self.color = (0, 0, 255)
        else:
            self.color = (255, 255, 255)

    def run(self):
        while True:
            #Reading the image
            self.image = cv.imread(self.imagePath, 1)

            #Resizing the image if it's not (512, 512)
            if self.image.shape[0] != 200 and self.image.shape[1] !=200:
                self.image = cv.resize(self.image, (200, 200))

            print('Shape: {}'.format(self.image.shape))

            # Showing image
            cv.imshow(self.windowName, self.image)

            #Mouse call back
            self.mouseCallback()
            
            #Waiting for response
            response = self.waitkey()
            if response:
                break


    def mouseCallback(self):
        cv.setMouseCallback(self.windowName, self.onclick)
        
    def onclick(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            print('Left Button: {}, {}'.format(x, y))

            #Saving the coordinate in temporory list
            self.co_ordinate.append((x, y))
            print(f'Co-ordinates: {self.co_ordinate}')

            # Show the point in image 
            self.image = cv.circle(self.image, (x, y), 2, self.color, -1)

            # Showing the images
            self.showImage(self.image)
                      
    def waitkey(self):
        key = cv.waitKey(0)
        if key == 27:
            quit()
        elif key == ord('r'):
            self.reset()
        else:
            # This will save co-ordinates in csv
            if self.co_ordinate:
                save(self.image_name, self.co_ordinate, True if self.iteration == 0 else False)
            cv.destroyAllWindows()
            return True

            

    def showImage(self, image):
        cv.imshow(self.windowName, image)

    def reset(self):
        self.co_ordinate.clear()
        print('Finished Reset!')



if __name__ == "__main__":
    # imagesPath = input('ImageDir: ')
    # savePath = input('SaveDir: ')
    # print(os.listdir('../Scale/images'))

    print("""
        Instruction: 'r' for reset.
                     Any key for next.
                     Esc for exit.
    """)
    time.sleep(2)
    for i, image in enumerate(os.listdir('Upload_image_here')):
        ext = ['jpg', 'jpeg', 'png']
        file_split = image.split('.')
        if len(file_split) == 2:
            if file_split[1] in ext:
                print('Image: {}'.format(image))
                Main(os.path.join(os.getcwd(), f'Upload_image_here/{image}'), iteration = i, image_name = image).run()
