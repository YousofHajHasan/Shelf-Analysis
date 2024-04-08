# Shelf Analysis with YOLOV8 and user friendly interface

## Description
This project utilizes YOLOv8 object detection on custom data for shelf analysis, along with a simple and user-friendly interface for shelf management.


## Project's Output Sample

<p align="center">
   <img src="https://github.com/YousofHajHasan/Shelf-Analysis/assets/161046637/a305c0cf-1d27-4f5c-8d19-af6a01579473" alt="Sample" width="600"/>
</p>

## Installation Notes
An environment with a GPU can provide significantly faster processing.

Don't forget to run pip install requirements.txt file

I've added a sample video to try the model on ***- it's inside the Test Video Folder -***

## Data Description

The dataset used is SKU110K, which provides 11,762 images with more than 1.7 million annotated bounding boxes captured in densely packed scenarios. It includes 8,233 images for training, 588 for validation, and 2,941 for testing. There are around 1,733,678 instances in total. The images of various scales, viewing angles, lighting conditions, and noise levels are collected from thousands of supermarket stores. All the images are resized to a resolution of one megapixel. 
Because we want to train the model locally, we reduced the data size to 1/3 for training purposes.

## Execution Stages

1. **The script allows users to select an image or video file.**

2. **For shelf detection, it prompts the user to enter the number of shelves in the image/video.**

3. **It then uses mouse clicks to define the rectangular regions of each shelf.**

4. **The YOLO model is loaded for object detection.**

5. **Objects are detected within the image/video frame.**

6. **If an object is located within a defined shelf region, a bounding box is drawn around the object, and a counter is incremented for that shelf.**

7. **The frame with bounding boxes and shelf counts is displayed.**

