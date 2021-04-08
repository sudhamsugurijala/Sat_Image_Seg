==================================================================================
Project Description
==================================================================================

The project will generate the base map from a satellite image for four classes of 
objects - Buildings, Roads, Greenery and Water Bodies. First, the system will take 
an input satellite image (RGB, JPG format) of pixel resolution 30 - 50cm, individually
segment the four classes using the trained U-Net weights, colour the segmentation outputs
from the U-Nets and finally combine the coloured outputs to obtain the base map

Input - Satellite image whose size is a multiple of 256 pixels (Minimum height and
	width is 256 pixels)
Output- Base Map of corresponding input satellite image with 4 classes of objects (
	Buildings (Red Colour), Roads (Black Colour), Greenery (Green Colour) and 
	Water Bodies (Blue Colour))


==================================================================================
Project Requirements
==================================================================================

1. tensorflow-gpu
2. keras
3. matplotlib
4. numpy
5. Pillow
6. opencv-contrib-python
7. tqdm
8. scipy
9. scikit-learn
10. scikit-image
11. flask


==================================================================================
Project Directory Structure
==================================================================================

-Sat_Image_Seg
|- static
   |- css
   |- labels
|- templates
|- unet
|- utils
|- weights
   |- buildings
   |- landcover
   |- roads
|- app.py
|- README.txt
|- requirements.txt


DESCRIPTION -

1. Sat_Image_Seg is the root folder of this project
2. static folder is for css (folder) and other images (labels folder) which do not
   change (static)
3. templates folder is for the HTML files
4. unet folder has python files for U-Net architecture definition
5. utils folder has implementation files and functions for preprocessing input 
   image, using U-Nets to predict classes in input satellite images and providing 
   colour to the segmentation predictions and combining to give the Base Map.
6. weights folder stores weights of individual model (one folder for each class 
   respectively)
7. app.py is the main flask app python file
8. README.txt is the user guide for this project
9. requirements.txt has requirements of this project, and they can be installed 
   with "pip install -r requirements.txt" command.



==================================================================================
List of Files Used
==================================================================================

1. 
File Name: 	upload.html (HTML File)

Input: 		Satellite Image from User

Output: 	Gives prompt to user if input field is empty.

Description: 	HTML page to get input image from user and call the flask server 
		when submit button is clicked.



2. 
File Name: 	complete.html (HTML File)

Input: 		Base Map from Flask server

Output: 	Displays Base Map to user.

Description: 	HTML page to render the base map returned by the flask server.



3. 
File Name: 	loss metrics.py (Python File)

Input: 		Not Applicable

Output: 	Not Applicable

Description: 	Defines Loss functions and metrics to be used by segmentation models.



4.
File Name: 	unet base binary.py (Python File)

Input: 		Path to model, option

Output: 	Returns segmentation output for buildings or roads class depending on option.

Description: 	Contains testing code for binary segmentation models. Returns segmentation 
		output to main application file (run model.py) depending on option (1 for buildings 
		and 2 for roads class)



5. 
File Name: 	unet multi.py (Python File)

Input: 		Path to model

Output: 	Returns segmentation output for greenery and water bodies class.

Description: 	Contains testing code for multi-class segmentation model (Greenery and water bodies class).
		Returns segmentation output to main application file (run model.py).



6.
File Name: 	app.py (Python File)

Input: 		Input image from upload.html

Output: 	Renders complete.html page with base map.

Description: 	Flask application file that stores the input image provided by user and calls the main 
		application file (run model.py). Retrieves base map from storage after getting control 
		from run model.py and Renders complete.html if no error is returned.



7.
File Name: 	run model.py (Python File)

Input: 		Not applicable

Output: 	Stores segmentation masks, base map in storage.

Description: 	The main application file. Retrieves input image from storage, checks validity of input image, 
		splits image to 256x256 tiles and tests them with segmentation models, adds colour to segmentation 
		outputs and combines all colour outputs to get the base map. Stores all output images and returns 
		control to app.py.



==================================================================================
Steps for Running the Project
==================================================================================

1. Open terminal / Command Prompt
2. Change working directory to root of this project (cd command)
3. Install Python, followed by Flask
3. Install all requirements from requirements.txt
4. run app.py
5. Open the URL displayed in the command prompt in a browser once the server has started.
6. Give an input in the web interface (Choose a satellite image)
7. Wait for the server to generate the base map
8. The final screen will show the base map generated by the system in the web interface.
