
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import cv2
import PIL
from pathlib import Path

# File path of the folder which contains the 4 folders with the images
input_root_dir = "/Users/bhaveyjain/Documents/example/"

# File path of the folder where the resulting images should be placed
output_root_dir = "/Users/bhaveyjain/Documents/testing/"

# Lists which contain the file paths of each image
animal_images_path = Path(input_root_dir + "animal").glob("*.png")
furn_images_path = Path(input_root_dir + "furniture").glob("*.png")
outdoor_images_path = Path(input_root_dir + "outdoor").glob("*.jpg")
indoor_images_path = Path(input_root_dir + "indoor").glob("*.jpg")

# Transferring the file paths to strings
animal_strings = [str(p) for p in animal_images_path]
furn_strings = [str(p) for p in furn_images_path]
outdoor_strings = [str(p) for p in outdoor_images_path]
indoor_strings = [str(p) for p in indoor_images_path]

# Lists which will store the img objects
anim_img_list = []
furn_img_list = []
outdoor_img_list = []
indoor_img_list = []

# Dictionaries to be able to make output file names match the images they are made of
anim_dict = {}
furn_dict = {}
outdoor_dict = {}
indoor_dict = {}


# This function makes image objects from the image file path strings and populates the dictionary
def make_output_imglist(img_list, string_list, classification, dictionary):
    counter = 0
    if classification == "png":
        for i in string_list:
            img_list.append(Image.open(i))
            # splicing the string to only get the name and not the whole file path
            dictionary.update({counter: i[i.rfind('/') + 1: -4]})
            counter += 1
    else:
        for i in string_list:
            img_list.append(Image.open(i))
            # splicing the string to only get the name and not the whole file path
            dictionary.update({counter: i[i.rfind('/') + 1: -4]})
            counter += 1


# This function resizes the images that need to be resized
def resize_images(img_list):
    i = 0
    while i < len(img_list):
        origHeight, origWidth = img_list[i].size

        maxDim = max(origWidth, origHeight)
        if maxDim > 500:
            scale_ratio = 500 / maxDim
            newHeight = int(origHeight * scale_ratio)
            newWidth = int(origWidth * scale_ratio)
            newDim = (newHeight, newWidth)
            resized_img = img_list[i].resize(newDim)
            img_list[i] = resized_img
        i += 1


# This function produces the final images with the foreground and background and names the file as (prefix foreground
def final_images(foreground_one, foreground_two, background, foreground_dict1, foreground_dict2, background_dict, pf1,
                 pf2):
    i = 0
    while i < len(background):
        background_img = background[i]
        background_height, background_width = background_img.size
        foreground_height = 0
        foreground_width = 0
        # xoff and yoff represent the position that the top left corner needs to be at to make the img centered
        xoff = 0
        yoff = 0

        # if i < 5 select from the first foreground group else select from the second group
        if i < 5:
            foreground_img = foreground_one[i]
            foreground_height, foreground_width = foreground_img.size

            yoff = round((background_height - foreground_height) / 2)
            xoff = round((background_width - foreground_width) / 2)
            background_img.paste(foreground_img, (yoff, xoff))
            background_img.save(output_root_dir + pf1 + foreground_dict1.get(i) + " " + background_dict.get(i) + '.jpg')

        else:
            foreground_img = foreground_two[i]
            foreground_height, foreground_width = foreground_img.size

            yoff = round((background_height - foreground_height) / 2)
            xoff = round((background_width - foreground_width) / 2)
            background_img.paste(foreground_img, (yoff, xoff))
            background_img.save(output_root_dir + pf2 + foreground_dict2.get(i) + " " + background_dict.get(i) + '.jpg')
        i += 1


# initializing all of the img lists
make_output_imglist(anim_img_list, animal_strings, "png", anim_dict)
make_output_imglist(furn_img_list, furn_strings, "png", furn_dict)
make_output_imglist(outdoor_img_list, outdoor_strings, "jpg", outdoor_dict)
make_output_imglist(indoor_img_list, indoor_strings, "jpg", indoor_dict)

# resizing the animal and furniture lists
resize_images(anim_img_list)
resize_images(furn_img_list)

# running the functions to produce final images in desired folder
final_images(anim_img_list, furn_img_list, indoor_img_list, anim_dict, furn_dict, indoor_dict, "AI_", "FI_")
final_images(furn_img_list, anim_img_list, outdoor_img_list, furn_dict, anim_dict, outdoor_dict, "FO_", "AO_")
