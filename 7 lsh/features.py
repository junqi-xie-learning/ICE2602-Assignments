import numpy as np

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


def extract(img):
    '''
    Extract feature from the image.

    Input: `img`: Input image
    Output: `feature`: Feature vector of the image
    '''
    H, W, _ = img.shape
    tl, tr, bl, br = img[:H // 2, :W // 2, :], img[H // 2 + 1:, :W // 2, :], \
        img[:H // 2, W // 2:, :], img[H // 2 + 1:, W // 2:, :]
    vector = color_histogram(tl) + color_histogram(tr) + \
        color_histogram(bl) + color_histogram(br)
    for i in range(len(vector)):
        if (vector[i] < 0.32):
            vector[i] = 0
        elif (0.32 <= vector[i] < 0.35):
            vector[i] = 1
        else:
            vector[i] = 2
    return np.array(vector)