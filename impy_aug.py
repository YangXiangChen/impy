import sys
sys.path.append('/home/ivs/Downloads/impy')
import argparse
import json
import xml.etree.ElementTree as ET

from ObjectDetectionDataset import *

def parse_args():
 desc = ('This is a script to random crop the dataset and annotation.')
 parser = argparse.ArgumentParser(description=desc)
 parser.add_argument('--databaseName', dest='databaseName', help='the name of database')
 parser.add_argument('--image_path', dest='image_path', help='the directory contain images')
 parser.add_argument('--annotation_path', dest='annotation_path', help='the directory contain annotaions')
 parser.add_argument('--cropped_size', dest='cropped_size', nargs='+', default=["300", "300"], help='the size of cropping (default: 300 300 [width height])')
 parser.add_argument('--output_path', dest='output_path', help='the directory of output files')
 args = parser.parse_args()
 return args

def xml2json(tree):
 json_content = {}
 json_content['filename'] = tree.findtext('path').replace('./','')
 json_content['width'] = float(tree.find('size').findtext('width'))
 json_content['height'] = float(tree.find('size').findtext('height'))
 json_content['class'] = "image"
 json_content['annotations'] = []
 
 for obj in tree.findall('object'):
  json_content['annotations'].append({"class": obj.findtext('name'),
                                      "type": "rect",
                                      "x": float(obj.find('bndbox').findtext('xmin')),
                                      "y": float(obj.find('bndbox').findtext('ymin')),
                                      "width": float(obj.find('bndbox').findtext('xmax')) - float(obj.find('bndbox').findtext('xmin')),
                                      "height": float(obj.find('bndbox').findtext('ymax')) - float(obj.find('bndbox').findtext('ymin'))})
                                      
 return json_content
 
 #filename = tree.findtext('path').replace('./','')
 #width = tree.find('size').findtext('width')
 #height = tree.find('size').findtext('height')
 
 return filename, width, height, annotations

def main():
 # parameter initialization
 args = parse_args()
 images_path = args.image_path
 annotations_path = args.annotation_path
 dbName = args.databaseName
 
 if not os.path.exists(args.output_path):
  os.mkdir(args.output_path)
  
 images_output_path = os.path.join(args.output_path,'image_'+args.cropped_size[0]+'x'+args.cropped_size[1])
 if not os.path.exists(images_output_path):
  os.mkdir(images_output_path)
 
 annotations_output_path = os.path.join(args.output_path,'anno_'+args.cropped_size[0]+'x'+args.cropped_size[1])
 if not os.path.exists(annotations_output_path):
  os.mkdir(annotations_output_path)
 
 # declare data augmentation object
 imda = ObjectDetectionDataset(imagesDirectory = images_path, annotationsDirectory = annotations_path, databaseName = dbName)
 
 # implement data augmentation
 imda.reduceDatasetByRois(offset = [int(args.cropped_size[0]), int(args.cropped_size[1])], outputImageDirectory = images_output_path, outputAnnotationDirectory = annotations_output_path)
 
 # create json file
 print('Creating json file...')
 json_content = []
 with open(os.path.join(args.output_path,'output.json'), 'w') as jsonout:
  with open(os.path.join(args.output_path,'output.txt'), 'w') as fout:
   for root, dirs, files in os.walk(images_output_path):
    for image_name in files:
     xml_path = os.path.join(annotations_output_path, image_name[:-3] + 'xml')
     fout.write("{} {}\n".format(os.path.join(annotations_output_path, image_name), xml_path))
     print(xml_path)
    
     tree = ET.parse(xml_path)
     json_content.append(xml2json(tree))
  json.dump(json_content, jsonout, indent = 4)
  print('Create json file done.')
    
if __name__ == "__main__":
 main()
