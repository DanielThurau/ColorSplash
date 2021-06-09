#!/usr/bin/python

import sys
import getopt
import os
import cv2
import json
from sklearn.cluster import KMeans
from collections import Counter


IMAGE_DIRECTORY = 'images'

def get_args(argv):
   output_file = ''
   try:
      opts, args = getopt.getopt(argv,"ho:",["output_file="])
   except getopt.GetoptError:
      print('processImages.py -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('processImages.py -o <outputfile>')
         sys.exit()
      elif opt in ("-o", "--output_file"):
         if not arg:
            raise RuntimeError("Outputfile cannot be an empty string")
         output_file = arg
   return output_file

def serialize_dict(kv_pair, file):
    with open(file, 'w') as f:
        f.write(json.dumps(kv_pair))

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def get_colors(image, number_of_colors):
    
   modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
   modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
   
   clf = KMeans(n_clusters = number_of_colors)
   labels = clf.fit_predict(modified_image)
   
   counts = Counter(labels)
   # sort to ensure correct color percentage
   counts = dict(sorted(counts.items()))
   
   center_colors = clf.cluster_centers_
   # We get ordered colors by iterating through the keys
   ordered_colors = [center_colors[i] for i in counts.keys()]
   hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
   rgb_colors = [ordered_colors[i] for i in counts.keys()]
   
   return rgb_colors

def print_ds_stats(ds):
   keys = len(ds)
   sum = 0

   for key, value in ds.items():
      sum += len(value)
   avg = sum / keys

   print("Data structure stats:")
   print("Number of keys: " + str(keys))
   print("Average number of images per RGB: " + str(avg))

def process_images(image_directory, number_of_colors, degree_of_rounding=3):
   image_dict = {}
   for file in os.listdir(image_directory):
      if not file.startswith('.'):
         print("Processing file: " + file)
         image = get_image(os.path.join(image_directory, file))
         colors = get_colors(image, number_of_colors)
         for color in colors:
               color_list = color.tolist()
               for i in range(len(color_list)):
                  color_list[i] = round(color_list[i], degree_of_rounding)
               color_tuple = str(color_list)

               if color_tuple not in image_dict:
                  image_dict[color_tuple] = []
               image_dict[color_tuple].append(file)
   return image_dict


if __name__ == "__main__":
   data_store = get_args(sys.argv[1:])
   if not data_store:
      raise RuntimeError("You must provide an output_file")

   rgb_to_file_ds = process_images(IMAGE_DIRECTORY, 3, 0)
   print("")
   print_ds_stats(rgb_to_file_ds)
   serialize_dict(rgb_to_file_ds, data_store)


      
