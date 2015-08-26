import cv2

def SliceImg(img, x1, y1, x2, y2):
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    if x1==x2 or y1==y2:
        print 'Two points should not be on a line.'
        return None
    if len(img) == 0:
        print 'Image is empty.'
        return None
    if x1<0 or y1<0 or x2>=len(img[0]) or y2>=len(img):
        print 'The region can not be projected on this image.'
        return None
        
    img = img[min(y1,y2) : max(y1,y2)]
    import numpy as np
    img_tmp = np.zeros(shape=(len(img), max(x1,x2) - min(x1,x2), len(img[0][0])), dtype=np.uint8)
    for i in range(len(img)):
        img_tmp[i] = img[i][min(x1,x2) : max(x1,x2)]
    return img_tmp


img = cv2.imread('/Users/ying/1.jpg')
img_sliced = SliceImg(img, 100, 100, 300, 250)
if not img_sliced == None:
    cv2.imshow('img', img_sliced)
    cv2.waitKey(0)




