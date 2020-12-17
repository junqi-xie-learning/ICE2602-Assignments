import numpy as np
from itertools import product

def color_histogram(img):
    '''
    Compute the components of the color histogram of the image.

    Input: `img`: Input image
    Output: `data`: Components of the histogram
    '''
    data = [0] * 3
    for i in range(3):
        data[i] = np.sum(img[:, :, i])
    return list(map(lambda x: x / sum(data), data))


def grayscale_histogram(img):
    '''
    Compute the components of the grayscale histogram of the image.

    Input: `img`: Input image
    Output: `data`: Components of the histogram
    '''
    data = [0] * 256
    for i in img.flatten():
        data[i] += 1
    return list(map(lambda x: x / sum(data), data))


def gradient_histogram(img):
    '''
    Compute the components of the gradient histogram of the image.

    Input: `img`: Input image
    Output: `data`: Components of the histogram
    '''
    img = img.astype('int')
    data = [0] * 361

    H, W = img.shape
    for i, j in product(range(1, H - 1), range(1, W - 1)):
        grad = np.array([img[i + 1][j] - img[i - 1][j], img[i][j + 1] - img[i][j - 1]])
        data[int(np.linalg.norm(grad))] += 1
    return list(map(lambda x: x / sum(data), data))