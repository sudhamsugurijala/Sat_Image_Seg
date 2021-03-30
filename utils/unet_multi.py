from unet.loss_metrics import *

def retMap(img, path):
	model = load_model(path, custom_objects={"mean_iou":mean_iou})
	X_pred = np.array([img])

	Y_pred = model.predict(X_pred)

	print(Y_pred[0].shape)

	test = np.argmax(Y_pred[0], axis=2)
	test = np.expand_dims(test, axis=-1)
	np.unique(test)

	mask = np.zeros((256, 256, 3), dtype=np.uint8)
	for i in range(256):
		for j in range(256):
			if test[i][j] == 0:
				mask[i][j] = [255, 255, 255]
			elif test[i][j] == 1: # BUILDING
				mask[i][j] = [255, 255, 255]
			elif test[i][j] == 2: # Green
				mask[i][j] = [0, 255, 0]
			elif test[i][j] == 3: # Water
				mask[i][j] = [0, 0, 255]

	return mask