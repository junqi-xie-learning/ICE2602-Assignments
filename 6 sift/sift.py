import numpy as np
import cv2
from itertools import product


def detectAndCompute(img):
    '''
    Find SIFT keypoints and descriptors in the image.

    Input: `img`: Input image
    Output: `kp`: Keypoints in the image
            `des`: SIFT descriptors of the keypoints
    '''
    kp = detect(img)
    des = compute(img, kp)
    return kp, des


def detect(img):
    '''
    Find the keypoints in the image. Using ``Good Features to Track'' to simplify calculations.

    Input: `img`: Input image
    Output: `kp`: Keypoints in the image
    '''
    corners = cv2.goodFeaturesToTrack(img, 500, 0.01, 10, blockSize=3, k=0.04)
    return list(map(lambda x: cv2.KeyPoint(x[0][0], x[0][1], 0), corners))


def compute(img, kp):
    '''
    Compute SIFT descriptors from keypoints in the image.

    Input: `img`: Input image
           `kp`: Keypoints in the image
    Output: `des`: SIFT descriptors corresponding to the keypoints
    '''
    grad = compute_gradient(img)
    orientation = assign_orientation(grad, kp, 2)
    return sift_descriptor(grad, kp, orientation)


def magnitude(g):
    return np.linalg.norm(g)


def angle(g):
    angle = round(np.angle(complex(g[0], g[1]), deg=True))
    if angle < 0:
        angle += 360
    return angle


def compute_gradient(img):
    '''
    Compute gradients of points in the image.

    Input: `img`: Input image
    Output: `grad`: Gradients of corresponding points in the image.
    '''
    img = img.astype('int')
    grad = np.zeros(img.shape + (2,))
    for i, j in product(range(1, img.shape[0] - 1), range(1, img.shape[1] - 1)):
        grad[i][j] = img[i + 1][j] - img[i - 1][j], img[i][j + 1] - img[i][j - 1]
    return grad


def assign_orientation(grad, kp, m):
    '''
    Orientation Assignment for keypoints in the image.

    Input: `grad`: Gradients of the input image
           `kp`: Keypoints in the image
           `m`: Width of the image window
    Output: `orientation`: Orientation Assignments of the keypoints
    '''
    orientation = { }
    for p in kp:
        x, y = map(int, p.pt)
        grad_hist = [0] * 36
        for i, j in product(range(x - m, x + m + 1), range(y - m, y + m + 1)):
            if 0 < i < grad.shape[0] - 1 and 0 < j < grad.shape[1] - 1:
                grad_hist[angle(grad[i][j]) // 10] += magnitude(grad[i][j])
        orientation[p] = grad_hist.index(max(grad_hist)) * 10
    return orientation


def bilinear_interpolation(grad, p):
    '''
    Compute gradient of the desired point.
    Bilinear interpolation is used for points whose coordinates aren't integers.

    Input: `grad`: Gradients of the input image
           `p`: Keypoint to be calculated
    Output: `interpolation`: Gradient of the desired point
    '''
    x, y = map(int, p.pt)
    dx1, dx2 = p.pt[0] - x, x + 1 - p.pt[0]
    dy1, dy2 = p.pt[1] - y, y + 1 - p.pt[1]

    weight = [[dx2 * dy2, dx1 * dy2], [dx2 * dy1, dx1 * dy1]]
    interpolation = np.array([0] * 2, dtype='float32')
    for i, j in product(range(2), range(2)):
        if 0 < i + x < grad.shape[0] - 1 and 0 < j + y < grad.shape[1] - 1:
            interpolation += grad[i + x][j + y] * weight[i][j]
    return interpolation


def sift_descriptor(grad, kp, orientation):
    '''
    Compute SIFT descriptors from gradients of the keypoints.

    Input: `grad`: Gradients of the input image
           `kp`: Keypoint to be calculated
           `orientation`: Orientation assigned to the keypoints
    Output: `des`: Matrix containing the SIFT descriptors
    '''
    des = []
    for p in kp:
        x, y = map(int, p.pt)
        orient = orientation[p]
        cosine = np.cos(np.radians(orient))
        sine = np.sin(np.radians(orient))

        des0 = []
        for a, b in product(range(-2, 2), range(-2, 2)):
            grad_hist = [0] * 8
            for i, j in product(range(a * 4, (a + 1) * 4), range(b * 4, (b + 1) * 4)):
                pos_i = x + cosine * i - sine * j
                pos_j = y + sine * i + cosine * j

                g = bilinear_interpolation(grad, cv2.KeyPoint(pos_i, pos_j, 0))
                a = angle(g) - orient
                if a < 0:
                    a += 360
                grad_hist[a // 45] += magnitude(g)
            des0.extend(grad_hist)
        des.append(des0)
    return np.array(des, dtype='float32')
