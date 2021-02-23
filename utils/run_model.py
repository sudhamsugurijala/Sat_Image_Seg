# Constant paths for saving inputs, weights
from PIL import ImageChops
from unet.loss_metrics import *
from utils.unet_baseline_model import retMask
from utils.pixel_wise_model import getPixelMask

IMG_PATH = "C:/Users/G Sudhamsu/Desktop/PROJECT DOC/app/Sat_Image_Seg/static"
OUTPUT_PATH = IMG_PATH

BUILDING_WEIGHTS = "C:/Users/G Sudhamsu/Desktop/PROJECT DOC/app/Sat_Image_Seg/weights/buildings/model_sample.h5"
ROAD_WEIGHTS = ""
GREEN_WEIGHTS = ""
WATER_WEIGHTS = ""


def splitImageAndTest(img, weights_path):
	"""Splits input image into 256x256 tiles, gets masks and returns output mask"""
	Y = np.zeros((img.shape[0], img.shape[1], img.shape[2]), np.uint8)
	for i in range(0, img.shape[0], 256):
		for j in range(0, img.shape[1], 256):
			Y[i:i+256, j:j+256] = retMask(img[i:i+256, j:j+256], weights_path)

	return Y


def colourMaskAndSave(opt):
	"""Gets mask and applies class colour"""
	if opt == 1: colour = [255, 0, 0] # RED
	if opt == 2: return 0 #colour = [0, 0, 0]   # BLACK
	if opt == 3: colour = [0, 255, 0] # GREEN
	if opt == 4: colour = [0, 0, 255] # BLUE

	file_path = os.path.join(OUTPUT_PATH, "{}_mask.png".format(opt))
	if not os.path.exists(file_path):
		return "No mask found to colour!"

	image = plt.imread(file_path)
	image_copy = image.copy() #image is read only, therefore copy
	
	black_pixels_mask = np.all(image == [0, 0, 0], axis=-1)
	non_black_pixels_mask = np.any(image != [0, 0, 0], axis=-1) 
	
	image_copy[black_pixels_mask] = [255, 255, 255]
	image_copy[non_black_pixels_mask] = colour

	plt.imsave(os.path.join(OUTPUT_PATH, '{}_color.png'.format(opt)), image_copy)


def segmentMapsAndSave(opt):
	"""
	Load input and get option (class) to segment
	option 1 - Buildings
	option 2 - Roads
	option 3 - Greenery
	option 4 - Water
	"""
	# check if input image is available
	file_path = os.path.join(IMG_PATH, "input.jpg")
	if not os.path.exists(file_path):
		# -1 is image not found or error in input shape
		return "Image Not found!"
	
	img = Image.open(file_path, 'r')
	img = np.array(img)
	if(img.shape[0]%256 != 0 or img.shape[1]%256 != 0 or img.shape[2] != 3):
		return "Image size invalid"

	# Segmentation
	# Buildings
	if opt == 1:
		Y = splitImageAndTest(img, BUILDING_WEIGHTS)

	# Roads
	if opt == 2:
		return 0
		#Y = splitImageAndTest(img, ROAD_WEIGHTS)

	# Greenery
	if opt == 3:
		#Y = splitImageAndTest(img, GREEN_WEIGHTS)
		Y = getPixelMask(img, opt)

	# Water
	if opt == 4:
		#Y = splitImageAndTest(img, WATER_WEIGHTS)
		Y = getPixelMask(img, opt)

	if type(Y) == str:
		return Y
	
	Y = Image.fromarray(Y)
	Y.save(os.path.join(OUTPUT_PATH, '{}_mask.png'.format(opt)), 'PNG')
	return 0

"""
def mergeMapsAndSave():
	# Roads remaining
	# base will be water
	file_path = os.path.join(OUTPUT_PATH, '4_color.png')
	# index 0 is dummy, blue is not needed as it is base
	color = [[], [255, 0, 0], [0, 0, 0], [0, 255, 0]]
	Y = Image.open(file_path)

	for i in [3, 1]:
		X = Image.open(os.path.join(OUTPUT_PATH, '{}_mask.png'.format(i)))
		Y = ImageChops.multiply(X.convert('RGB'), Y.convert('RGB'))
		Y = np.array(Y)
		black_pixels_mask = np.all(Y == [0, 0, 0], axis=-1)
		Y[black_pixels_mask] = color[i]
		Y = Image.fromarray(Y)

	Y.save(os.path.join(OUTPUT_PATH, 'output.png'), 'PNG')
	return 0
"""


def getBaseMap():
	for i in range(1, 4+1):
		Y = segmentMapsAndSave(i)

		if type(Y) == str:
			return Y

		Y = colourMaskAndSave(i)

		if type(Y) == str:
			return Y
	
	#mergeMapsAndSave()
	return 0