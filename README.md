# Hand-writing recognition
## Background
## Install

1. click on code -> Download ZIP
2. unzip the zip file to the path you expect

## Usage
### 1. Generate a new model

To generate a new model, please first open the file "modelgenerated.py"<br/>
Click on run and after a few second a summary of whole structure of current will be shown on you screen and saved in the “saved_model” folder (Customizable)<br/>
**Carefully modify the parameters of the CNN layers and save path**

### 2. Training & Testing the model

For training & testing a model, please open "main.py"<br/>
There are already two trained models available “saved_model_28” and "saved_model_64" in folder "saved_model". For testing these models, please annotate the training part in the file to avoid retrained the model **This might decrease the accuracy and increase time cost!**<br/>
For testing new model, please set the path to where your model saved and then begin.<br/>

### 3. Use the Writing pad

To use the Writing pad, please run file "MainWidget.py"<br/>
Click on "Start recognition" when you finish writing a letter, the result will be shown on the screen and the current letter you write will be saved in “test.png”<br/>

## Maintainers
> Liu Yuanchen email: sgyliu78@liverpool.ac.uk<br/>
> Wu Guanjie<br/>
> Qiu Jiachun<br/>
> Luo Xinbo
For any questions please send a email to us or post
##
