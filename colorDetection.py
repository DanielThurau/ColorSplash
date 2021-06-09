#!/usr/bin/python

from numpy.random import f
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import getopt
import ast
import cv2
from collections import Counter
from scipy.spatial import cKDTree
from skimage.color import rgb2lab, deltaE_cie76
import os
import json
import sys


IMAGE_DIRECTORY = 'images'

class Args:
    def __init__(self):
        input_file = None
        hex_color = None
        distance = None

def get_args(argv):
    args = Args()
    try:
        opts, arginball= getopt.getopt(argv,"hi:",["input_file=", "hex=", "distance="])
    except getopt.GetoptError:
        print('processImages.py -i <input_file> --hex <hex code> --distance <distance>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('processImages.py -i <input_file> --hex <hex code> --distance <distance>')
            sys.exit()
        elif opt in ("-i", "--input_file"):
            if not arg:
                raise RuntimeError("Inputfile cannot be an empty string")
            args.input_file = arg
        elif opt in ("--hex"):
            if not arg:
                raise RuntimeError("Hex code cannot be an empty string")
            args.hex_color = arg
        elif opt in ("--distance"):
            if not arg:
                raise RuntimeError("Distance cannot be an empty string")
            args.distance = arg
    
    return args

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return list(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

def deseralize_dict(file):
    with open(file) as f:
        data = f.read()
    return json.loads(data)

def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def get_rgb_keys(image_dict):
    rgbs = []
    for key in image_dict.keys():
        rgb = [float(x) for x in  ast.literal_eval(key)]
        rgbs.append(rgb)
    return np.array(rgbs)

if __name__ == "__main__":
    args = get_args(sys.argv[1:])

    image_dict = deseralize_dict(args.input_file)
    matching_color = hex_to_rgb(args.hex_color)
    distance = args.distance


    pts = get_rgb_keys(image_dict)

    T = cKDTree(pts)
    rgbs = T.data[T.query_ball_point(matching_color, r=distance)]
    image_files = set()
    for rgb in rgbs:
        for deez_nuts in image_dict[str(rgb.tolist())]:
            image_files.add(deez_nuts)
    print(image_files)

    images = []
    for file in image_files:
        images.append(get_image(os.path.join(IMAGE_DIRECTORY, file)))

    plt.figure(figsize=(20, 10))
    for i in range(len(images)):
        plt.subplot(1, len(images), i+1)
        plt.imshow(images[i])

    plt.show()