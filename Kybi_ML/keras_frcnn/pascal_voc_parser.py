#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import cv2
import xml.etree.ElementTree as ET
import numpy as np


def get_data(input_path, mode):
    all_imgs = []
    classes_count = {}
    class_mapping = {}
    visualise = False

    # data_paths = [os.path.join(input_path,s) for s in ['VOC2007', 'VOC2012']]

    data_path = input_path
    print ('Parsing annotation files')
    annot_path = os.path.join(data_path, 'annotations')
    annot_val_path=os.path.join(data_path,'annotations')
    imgs_path = os.path.join(data_path, 'JPEGImages')
    imgs_val_path=os.path.join(data_path,'JPEGImages')
    imgsets_path_trainval = os.path.join(data_path, 'train_safetipin.txt')
    print (imgsets_path_trainval)
    imgsets_path_test = os.path.join(data_path, 'test_safetipin.txt')
    print (imgsets_path_test)
    trainval_files = []
    test_files = []
    try:
        with open(imgsets_path_trainval) as f:
            for line in f:
                (filename, ext) = os.path.splitext(line)

                # print (line)
                # print (filename)

                annot_file = filename + '.xml'
                annotfile = os.path.join(annot_path, annot_file)

                # print (annot_file)

                trainval_files.append(annotfile)
    except Exception as e:
        print (e)
    try:
        with open(imgsets_path_test) as f:
            for line in f:
                (filename, ext) = os.path.splitext(line)
                annot_file = filename + '.xml'
                annotfile = os.path.join(annot_val_path, annot_file)
                test_files.append(annotfile)
    except Exception as e:
        print (e)
    if mode == 'train':
        annots = trainval_files
        path=imgs_path
    else:
        annots = test_files
        path=imgs_val_path
    idx = 0
    #print (annots)
    for annot in annots:
        try:
            idx += 1
            print (annot)
            et = ET.parse(annot)
            element = et.getroot()

            element_objs = element.findall('object')
            element_filename = element.find('filename').text
            element_width = int(element.find('size').find('width').text)
            element_height = int(element.find('size').find('height'
                                 ).text)

            if len(element_objs) > 0:
                annotation_data = {
                    'filepath': os.path.join(path,
                            element_filename),
                    'width': element_width,
                    'height': element_height,
                    'bboxes': [],
                    }

                #if element_filename in trainval_files:
                if mode=='train':
                     annotation_data['imageset'] = 'trainval'
                #elif element_filename in test_files:
                else:
                     annotation_data['imageset'] = 'test'
                #else:
                   # annotation_data['imageset'] = 'trainval'

            for element_obj in element_objs:
                class_name = element_obj.find('name').text
                if class_name not in classes_count:
                    classes_count[class_name] = 1
                else:
                    classes_count[class_name] += 1

                if class_name not in class_mapping:
                    class_mapping[class_name] = len(class_mapping)
                obj_bbox = element_obj.find('bndbox')
                x1 = int(round(float(obj_bbox.find('xmin').text)))
                y1 = int(round(float(obj_bbox.find('ymin').text)))
                x2 = int(round(float(obj_bbox.find('xmax').text)))
                y2 = int(round(float(obj_bbox.find('ymax').text)))
                #difficulty = int(element_obj.find('difficult').text) \
                #    == 1
                annotation_data['bboxes'].append({
                    'class': class_name,
                    'x1': x1,
                    'x2': x2,
                    'y1': y1,
                    'y2': y2,
                    'difficult':1,
                    })
            all_imgs.append(annotation_data)

            if visualise:
                img = cv2.imread(annotation_data['filepath'])
                for bbox in annotation_data['bboxes']:
                    cv2.rectangle(img, (bbox['x1'], bbox['y1']),
                                  (bbox['x2'], bbox['y2']), (0, 0, 255))
                cv2.imshow('img', img)
                cv2.waitKey(0)
        except Exception as e:

            print (e)
            print (annot)
            continue

        # print(f'{class_mapping}')

    return (all_imgs, classes_count, class_mapping)


if __name__ == '__main__':
    img,count,mapping=get_data('', 'train')
    print (count)
    print (mapping)
    #print(img)
