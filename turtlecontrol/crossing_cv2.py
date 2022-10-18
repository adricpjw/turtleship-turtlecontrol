import numpy as np
import cv2

TOLERANCE = 10
class CrossingDetection:
    def __init__(self, parent):
        self.parent = parent

    def detectPedCrossing(self):
        cap = cv2.VideoCapture('resource/rumin_resized_rotated.mp4')
        while cap.isOpened():
            ret, frame = cap.read()
            edges = self.generateCanny(frame,cap)
            mask = self.generatePolyMask(frame, edges)
            lines_img = self.generateHoughLines(frame, mask)
            cv2.imshow('Final Image with dotted Lines detected', lines_img)
            cv2.imshow('Polymask', mask)
            cv2.imshow('Original', frame)
            if (cv2.waitKey(1) == ord('q') or self.parent.stop):
                break
        cap.release()
        cv2.destroyAllWindows()
    
    def generateCanny(self,frame,cap):
            width = int(cap.get(3))
            height = int(cap.get(4))
            imgGray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            kernel_size = 5
            blur = cv2.GaussianBlur(imgGray, (kernel_size, kernel_size), 0)
            low_t = 200
            high_t = 250
            return cv2.Canny(blur, low_t, high_t)

    def generatePolyMask(self, frame, imgbw):
            vertices = np.array([[(0, frame.shape[0]), (0, frame.shape[0] - 150), (150, 230), (490, 230), (frame.shape[1], frame.shape[0]- 150), (frame.shape[1], frame.shape[0])]], dtype=np.int32)
            mask = np.zeros_like(imgbw)
            cv2.fillPoly(mask, vertices, 255)
            masked_edges = cv2.bitwise_and(imgbw, mask)
            return masked_edges

    def generateHoughLines(self, frame, mask):
            img_cp = np.zeros(frame.shape)
            imgLines= cv2.HoughLinesP(mask,2,np.pi/180,threshold=55, minLineLength= 8, maxLineGap=20)
            try:
                for i in range(len(imgLines)):
                    for x1,y1,x2,y2 in imgLines[i]:
                        cv2.line(img_cp,(x1,y1),(x2,y2),(0,255,0),2)
            except:
                pass
            return img_cp






