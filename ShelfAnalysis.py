import cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from ultralytics import YOLO
import re

# Variables for Mouse callbacks and Rectangles
drawing = False
top_left = None
bottom_right = None
rectangle_coordinates = None
click_count = 0

def draw_rectangle(event, x, y, flags, param):
    global drawing, top_left, bottom_right, click_count, rectangle_coordinates, original_img, img, i

    if event == cv2.EVENT_LBUTTONDOWN:
        click_count += 1

        if click_count == 1:
            top_left = (x, y)

        elif click_count == 2:
            bottom_right = (x, y)
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
            cv2.rectangle(img, (
            (int((top_left[0] + bottom_right[0]) / 2) - 10), int((top_left[1] + bottom_right[1]) / 2) - 10),
                          (int((top_left[0] + bottom_right[0]) / 2) + 20, int((top_left[1] + bottom_right[1]) / 2) + 20),
                          (0, 0, 0), -1)
            cv2.putText(img, text=f"{i+1}", org=(int((top_left[0]+bottom_right[0])/2 - 5), int((top_left[1]+bottom_right[1])/2 + 15)),
                        fontFace=3, fontScale=1, thickness=1, color=(0, 0, 255))
            cv2.imshow('image', img)
            rectangle_coordinates = (top_left, bottom_right)

        elif click_count == 3:
            img = original_img.copy() # Reset on the third click
            top_left = (x, y)
            click_count = 1

def call_draw_rectangle():
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('image', int(width * 0.5), int(height * 0.5))
    cv2.setMouseCallback('image', draw_rectangle)
    while True:
        cv2.imshow('image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def Topleft_Bottomright_Fix(Box):
    # we need to make sure that the box have the top left and bottom right coordinates was choosen correctly
    if Box[0][0] > Box[1][0]:
        Box = list(map(list, Box))  # Convert tuple to list
        Box[0][0], Box[1][0] = Box[1][0], Box[0][0] # Swap the x coordinates
        Box = tuple(map(tuple, Box))  # Convert list back to tuple
        
    if Box[0][1] > Box[1][1]:
        Box = list(map(list, Box))  # Since we can't change the tuple, we convert it to a list
        Box[0][1], Box[1][1] = Box[1][1], Box[0][1] # Swap the y coordinates    
        Box = tuple(map(tuple, Box))  # Convert list back to tuple
    
    return Box
        

def is_inside(outerBox, innerBox):
    inside = (
            outerBox[0][0] <= innerBox[0][0] <= outerBox[1][0] and
            outerBox[0][1] <= innerBox[0][1] <= outerBox[1][1] and
            outerBox[0][0] <= innerBox[1][0] <= outerBox[1][0] and
            outerBox[0][1] <= innerBox[1][1] <= outerBox[1][1]
    )

    return inside


# Reading an image using file explorer
root = Tk()
root.withdraw()

filename = askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.mp4")])

while not filename:
    print("No file selected.")
    filename = askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.mp4")])


Video_flag = False
# Check if input is image or video
if re.search(r"\.(mp4)$", filename):
    Video_flag = True
    vid = cv2.VideoCapture(filename)
    nxt, Full_img = vid.read()
else:
    # Reading Image
    Full_img = cv2.imread(filename)

img = Full_img.copy()

Shelf_Num = int(input("Enter number of shelves: "))
rectangles = []

# Determining shelves coordinates
for i in range(Shelf_Num):
    original_img = img.copy()
    call_draw_rectangle()
    click_count = 0
    rectangles.append(rectangle_coordinates)
cv2.destroyAllWindows()

# Loading the model
model = YOLO("Models/Model.pt")

# to detect objects in a video
if Video_flag:
    while nxt:
        results = model(img, stream=True, conf=0.48, imgsz=(640, 640), iou=0.3)
        for result in results:
            counter_list = []
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                result_box = []
                result_box.append((x1, y1))
                result_box.append((x2, y2))
                for index in range(len(rectangles)):
                    counter_list.append(0)
                    rectangles[index] = Topleft_Bottomright_Fix(rectangles[index])
                    inside = is_inside(rectangles[index], result_box)
                    if inside:
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        counter_list[index] += 1
                        break
                if rectangles is None:
                    print("No shelves have been chosen")
                    break
            for index in range(len(rectangles)):
                cv2.rectangle(img, (
                    (int((rectangles[index][0][0] + rectangles[index][1][0]) / 2) - 25),
                    int((rectangles[index][0][1] + rectangles[index][1][1]) / 2) - 25),
                              (int((rectangles[index][0][0] + rectangles[index][1][0]) / 2) + 30,
                               int((rectangles[index][0][1] + rectangles[index][1][1]) / 2) + 30),
                              (0, 0, 0), -1)
                cv2.putText(img, text=f"{counter_list[index]}",
                            org=(int((rectangles[index][0][0] + rectangles[index][1][0]) / 2 - 5),
                                 int((rectangles[index][0][1] + rectangles[index][1][1]) / 2 + 15)),
                            fontFace=3, fontScale=1, thickness=2, color=(255, 255, 255))

        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.imshow("image", img)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        nxt, img = vid.read()

# To detect objects in an image
else:
    img = Full_img.copy()
    results = model(img, stream=True, conf=0.48, imgsz=(640, 640), iou=0.3)
    for result in results:
        counter_list = []
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            result_box = []
            result_box.append((x1, y1))
            result_box.append((x2, y2))
            for index in range(len(rectangles)):
                counter_list.append(0)
                rectangles[index] = Topleft_Bottomright_Fix(rectangles[index])
                inside = is_inside(rectangles[index], result_box)
                if inside:
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    counter_list[index] += 1
                    break
            if rectangles is None:
                print("No shelves have been chosen")
                break
        for index in range(len(rectangles)):
            cv2.rectangle(img, (
                (int((rectangles[index][0][0] + rectangles[index][1][0]) / 2) - 25),
                int((rectangles[index][0][1] + rectangles[index][1][1]) / 2) - 25),
                          (int((rectangles[index][0][0] + rectangles[index][1][0]) / 2) + 30,
                           int((rectangles[index][0][1] + rectangles[index][1][1]) / 2) + 30),
                          (0, 0, 0), -1)
            cv2.putText(img, text=f"{counter_list[index]}",
                        org=(int((rectangles[index][0][0] + rectangles[index][1][0]) / 2 - 15),
                             int((rectangles[index][0][1] + rectangles[index][1][1]) / 2 + 15)),
                        fontFace=3, fontScale=1, thickness=2, color=(255, 255, 255))

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow("image", img)
    cv2.waitKey(0)

vid.release()
cv2.destroyAllWindows()