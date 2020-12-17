import numpy as np
import cv2

sift = cv2.SIFT_create()
def sift_feature(img):
    '''
    Compute the components of the SIFT feature of the image

    Input: `img`: Input image
    Output: `data`: Components of the SIFT feature
    '''
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    kp, des = sift.detectAndCompute(img_gray, None)
    data = [0] * 128
    for i in range(128):
        data[i] = sum(des[:, i])
    return list(map(lambda x: x / sum(data), data))


def extract(img):
    '''
    Extract feature from the image.

    Input: `img`: Input image
    Output: `feature`: Feature vector of the image
    '''
    vector = sift_feature(img)
    for i in range(len(vector)):
        if (vector[i] < 0.005):
            vector[i] = 0
        elif (0.005 <= vector[i] < 0.008):
            vector[i] = 1
        else:
            vector[i] = 2
    return np.array(vector)