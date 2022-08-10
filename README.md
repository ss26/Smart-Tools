## Smart-Tools
# DATA COLLECTION:
The data is collected with tools found in the data collection folder. These include arduino code for collecting the data. Python code to set up the data transfer with pyserial and a plotting tool to visualize the data.

# DATA PRE-PROCESSING:
Once the data is collected and stored into separate csv files, it is pre-processed with the python code included in the Pre-Processing folder. The pre-processed data can be found on the the team's google drive

# MODEL DESIGN AND TRAINING:
The model is designed, created and trained using google colab and the tensorflow and keras library. Running the complete google colab will create a "model_quantized.tflite" file. This tflite file is then converted into hexadecimal format for deployment onto arduino.

# ARDUINO DEPLOYMENT:
The "Arduino Deployment" folder contains the arduino files necessary to deploy the model onto the device

 
