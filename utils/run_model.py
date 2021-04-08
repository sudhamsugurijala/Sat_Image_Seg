# Constant paths for saving inputs, weights
from PIL import ImageChops
import concurrent.futures
from unet.loss_metrics import *
from utils.unet_base_binary import retMask
from utils.unet_multi import retMap
#from utils.pixel_wise_model import getPixelMask

IMG_PATH = "./static"
OUTPUT_PATH = IMG_PATH

# Every model is named model.h5 for simplicity
BUILDING_WEIGHTS = "./weights/buildings/model.h5"
ROAD_WEIGHTS = "./weights/roads/model.h5"
LANDCOVER_WEIGHTS="./weights/landcover/model.h5"


def splitImageAndTest(img, weights_path):
	"""Splits input image into 256x256 tiles, gets masks and returns output mask"""
	Y = np.zeros((img.shape[0], img.shape[1], img.shape[2]), np.uint8)
	for i in range(0, img.shape[0], 256):
		for j in range(0, img.shape[1], 256):
			## Threading
			with concurrent.futures.ThreadPoolExecutor() as thread:
				thread_out = thread.submit(retMask, img[i:i+256, j:j+256], weights_path)
				Y[i:i+256, j:j+256] = thread_out.result() #retMask(img[i:i+256, j:j+256], weights_path)
			## Threading

	return Y


def splitImageAndMap(img, weights_path):
	"""Special function for multiclass landcover classification"""
	Y = np.zeros((img.shape[0], img.shape[1], img.shape[2]), np.uint8)
	for i in range(0, img.shape[0], 256):
		for j in range(0, img.shape[1], 256):
			## Threading
			with concurrent.futures.ThreadPoolExecutor() as thread:
				thread_out = thread.submit(retMap, img[i:i+256, j:j+256], weights_path)
				Y[i:i+256, j:j+256] = thread_out.result() #retMask(img[i:i+256, j:j+256], weights_path)
			## Threading
			#Y[i:i+256, j:j+256] = retMap(img[i:i+256, j:j+256], weights_path)

	return Y	


def colourMaskAndSave(opt):
	"""Gets mask and applies class colour"""
	if opt == 1: colour = [255, 0, 0] # RED
	if opt == 2: colour = [0, 0, 0]   # BLACK

	file_path = os.path.join(OUTPUT_PATH, "{}_mask.png".format(opt))
	if not os.path.exists(file_path):
		return "No mask found to colour!"

	image = plt.imread(file_path)
	image_copy = image.copy() #image is read only, therefore copy
	
	black_pixels_mask = np.all(image == [0, 0, 0], axis=-1)
	non_black_pixels_mask = np.any(image != [0, 0, 0], axis=-1) 
	
	image_copy[black_pixels_mask] = [255, 255, 255]
	image_copy[non_black_pixels_mask] = colour

	image_copy = Image.fromarray(image_copy.astype('uint8'), 'RGB')
	image_copy.save(os.path.join(OUTPUT_PATH, '{}_color.png'.format(opt)))


def segmentMapsAndSave(opt):
	"""
	Load input and get option (class) to segment
	option 1 - Buildings
	option 2 - Roads
	option 3 - Greenery, Water (Landcover)
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
		Y = splitImageAndTest(img, ROAD_WEIGHTS)

	if type(Y) == str:
		return Y
	
	Y = Image.fromarray(Y)
	Y.save(os.path.join(OUTPUT_PATH, '{}_mask.png'.format(opt)), 'PNG')
	return 0


def mergeMapsAndSave(token):
	# Roads remaining
	# base will be water
	file_path = os.path.join(OUTPUT_PATH, '3_color.png')
	# index 0 is dummy, blue is not needed as it is base
	color = [[], [255, 0, 0], [0, 0, 0]]
	Y = Image.open(file_path)

	for i in [1, 2]:
		X = Image.open(os.path.join(OUTPUT_PATH, '{}_mask.png'.format(i)))
		X = np.array(X)
		black_pixels_mask = np.all(X == [0, 0, 0], axis=-1)
		non_black_pixels_mask = np.any(X != [0, 0, 0], axis=-1)
		# invert color to multiply
		X[black_pixels_mask] = [255, 255, 255]
		X[non_black_pixels_mask] = [0, 0, 0]
		X = Image.fromarray(X)

		Y = ImageChops.multiply(X.convert('RGB'), Y.convert('RGB'))
		Y = np.array(Y)
		black_pixels_mask = np.all(Y == [0, 0, 0], axis=-1)
		Y[black_pixels_mask] = color[i]
		Y = Image.fromarray(Y)

	Y.save(os.path.join(OUTPUT_PATH, 'map_{}.png'.format(token)))
	validation = Image.open(os.path.join(IMG_PATH, "input.jpg"))

	Y = Y.convert('RGBA')
	validation = validation.convert('RGBA')

	validation = Image.blend(validation, Y, 0.5)
	validation.save(os.path.join(IMG_PATH, "validation.png"), "PNG")
	return 0


def generateLandcoverMap():
	file_path = os.path.join(IMG_PATH, "input.jpg")
	if not os.path.exists(file_path):
		# -1 is image not found or error in input shape
		return "Image Not found!"
	
	img = Image.open(file_path, 'r')
	img = np.array(img)
	if(img.shape[0]%256 != 0 or img.shape[1]%256 != 0 or img.shape[2] != 3):
		return "Image size invalid"

	Y = splitImageAndMap(img, LANDCOVER_WEIGHTS)
	Y = Image.fromarray(Y)
	Y.save(os.path.join(OUTPUT_PATH, '3_color.png'), 'PNG')

	return 0


def getBaseMap(token):

	# separately run multiclass model first
	Y = generateLandcoverMap()
	if type(Y) == str:
		return Y

	# Binary model for buildings(1) and Roads(2)
	for i in range(1, 2+1):
		Y = segmentMapsAndSave(i)
		if type(Y) == str:
			return Y

		Y = colourMaskAndSave(i)
		if type(Y) == str:
			return Y
	
	mergeMapsAndSave(token)
	return 0