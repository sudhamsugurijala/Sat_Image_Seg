import cv2
import numpy as np

def getPixelMask(img, opt):
	""" 
	Get pixel wise mask of opt class
	input = img (np array), opt
	opt = 3 Greenery
	opt = 4 Water
	"""

	if opt == 3:
		lower_limit = (15, 50, 0)
		upper_limit = (75, 255, 150)

	if opt == 4:
		lower_limit = (76, 100, 10)
		upper_limit = (120, 255, 60)

	hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
	h, s, v = cv2.split(hsv_img)
	mask = cv2.inRange(hsv_img, lower_limit, upper_limit)
	white_layer = np.zeros((img.shape[0], img.shape[1], img.shape[2]), np.uint8)
	white_layer[:] = (255, 255, 255)
	mask = cv2.bitwise_and(white_layer, white_layer, mask=mask)
	return mask