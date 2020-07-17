import cv2

#read all file from dir
from os import listdir
from os.path import isfile, join

import xml.etree.ElementTree as ET

def concat_img (img_path, front_path, rear_path, left_path, right_path):
    front_img = cv2.imread(img_path + front_path + ".jpg")
    rear_img = cv2.imread(img_path + rear_path + ".jpg")
    left_img = cv2.imread(img_path + left_path + ".jpg")
    right_img = cv2.imread(img_path + right_path + ".jpg")
    
    front_rear = cv2.hconcat([front_img, rear_img])
    left_right = cv2.hconcat([left_img, right_img])
    concat_all = cv2.vconcat([front_rear, left_right])

    return concat_all

def concat_ant (ant_path, front_path, rear_path, left_path, right_path):
    front_tree = ET.parse(ant_path + front_path + ".xml")
    rear_tree = ET.parse(ant_path + rear_path + ".xml")
    left_tree = ET.parse(ant_path + left_path + ".xml")
    right_tree = ET.parse(ant_path + right_path + ".xml")
    
    front_root = front_tree.getroot()
    rear_root = rear_tree.getroot()
    left_root = left_tree.getroot()
    right_root = right_tree.getroot()
    
    size = front_root.find("size")
    offset_width = int(size.find("width").text)
    size.find("width").text = str(offset_width*2)
    offset_height = int(size.find("height").text)
    size.find("height").text = str(offset_height*2)

    
    # print(ET.tostring(front_root))

    for ob in rear_root.iter("object"):
        bndbox = ob.find("bndbox")
        bndbox.find("xmin").text = str(float(bndbox.find("xmin").text) + offset_width)
        bndbox.find("xmax").text = str(float(bndbox.find("xmax").text) + offset_width)
        front_root.append(ob)
    
    
    for ob in left_root.iter("object"):
        bndbox = ob.find("bndbox")
        bndbox.find("ymin").text = str(float(bndbox.find("ymin").text) + offset_height)
        bndbox.find("ymax").text = str(float(bndbox.find("ymax").text) + offset_height)
        front_root.append(ob)

    for ob in right_root.iter("object"):
        bndbox = ob.find("bndbox")
        bndbox.find("xmin").text = str(float(bndbox.find("xmin").text) + offset_width)
        bndbox.find("xmax").text = str(float(bndbox.find("xmax").text) + offset_width)
        bndbox.find("ymin").text = str(float(bndbox.find("ymin").text) + offset_height)
        bndbox.find("ymax").text = str(float(bndbox.find("ymax").text) + offset_height)
        front_root.append(ob)

    # print(ET.tostring(front_root))

db_path = "C:/Users/haminji/Documents/image_concat/GODTrain200618_SVM_case1_new/"
img_path = db_path + "newJPEGImages/"
ant_path = db_path + "newAnnotations/"

allfiles = [f.split(".jpg")[0] for f in listdir(img_path) if isfile(join(img_path, f))]

front_files = [f for f in allfiles if f.split("_")[6]=="front"]
rear_files = [f for f in allfiles if f.split("_")[6]=="rear"]
left_files = [f for f in allfiles if f.split("_")[6]=="left"]
right_files = [f for f in allfiles if f.split("_")[6]=="right"]

concat_imgs = []
concat_ants = []

check = 0
#for i in range(1):
for i in range(min(len(front_files), len(rear_files), len(left_files), len(right_files))):
    concat_imgs.append(concat_img(img_path, front_files[i], rear_files[i], left_files[i], right_files[i]))
    concat_ants.append(concat_ant(ant_path, front_files[i], rear_files[i], left_files[i], right_files[i]))

#have to save as file


# Output img with window name as 'image' 
cv2.imshow('image', concat_imgs[0])  
  
# Maintain output window utill 
# user presses a key 
cv2.waitKey(0)         
  
# Destroying present windows on screen 
cv2.destroyAllWindows()  


    