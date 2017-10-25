#!/usr/bin/env python
# -*- coding:utf-8 -*-
import argparse
import json
import os
import sys
from time import sleep

import cv2
import matplotlib.pyplot as plt
import numpy as np
import rospy
import scipy.io as sio
import zmq
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

sys.path.append('/home/ros/code/py-faster-rcnn/tools')

import _init_paths
import caffe
from fast_rcnn.config import cfg
from fast_rcnn.nms_wrapper import nms
from fast_rcnn.test import im_detect
from utils.timer import Timer


CLASSES = {'voc': ('__background__',
                   'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse',
                   'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor'),
           'self': ('__background__',
                    'bottle', 'hedgehog', 'polarbear', 'squirrel', 'dolphin', 'lion', 'box', 'brush', 'cabbage', 'eggplant')}


def get_net():
    '''初始化图像识别模块'''

    cfg.TEST.HAS_RPN = True  # Use RPN for proposals
    # args = parse_args()
    args = {'caffemodel': '/home/ros/code/py-faster-rcnn.bak/data/faster_rcnn_models/zf_voc.caffemodel',
            'classes': 'voc',
            'cpu_mode': False,
            'gpu_id': 0,
            'prototxt': '/home/ros/code/py-faster-rcnn.bak/data/faster_rcnn_models/zf_voc.pt'}
    print args

    Classes = CLASSES[args['classes']]
    prototxt = args['prototxt']
    caffemodel = args['caffemodel']
    if not os.path.isfile(caffemodel):
        raise IOError(('{:s} not found.\nDid you run ./data/script/'
                       'fetch_faster_rcnn_models.sh?').format(caffemodel))

    if args['cpu_mode']:
        caffe.set_mode_cpu()
    else:
        caffe.set_mode_gpu()
        caffe.set_device(args['gpu_id'])
        cfg.GPU_ID = args['gpu_id']
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)
    return net, Classes


def recognize(net, Classes, im):
    '''图像识别函数'''
    # im_path = "/tmp/camera.jpg"
    # image = cv2.imread(im_path)
    image = im
    object_list = demo(net, image, Classes)
    if len(object_list):
        res_list = json.dumps(object_list)
        return res_list


def vis_detections(im, class_name, dets, thresh=0.5):
    """Draw detected bounding boxes."""
    list1 = []
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return []
    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]
        list1.append([class_name, int(bbox[0]), int(
            bbox[1]), int(bbox[2]), int(bbox[3])])
    return list1


def demo(net, image, Classes):
    """Detect object classes in an image using pre-computed object proposals."""
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(net, image)
    timer.toc()
    # print ('Detection took {:.3f}s for '
    #      '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    CONF_THRESH = 0.8
    NMS_THRESH = 0.3
    object_list = []
    for cls_ind, cls in enumerate(Classes[1:]):  # CLASSES1
        cls_ind += 1  # because we skipped background
        cls_boxes = boxes[:, 4 * cls_ind:4 * (cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        list2 = vis_detections(image, cls, dets, thresh=CONF_THRESH)
        if len(list2):
            object_list.append(list2)
    return object_list


def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Faster R-CNN demo')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU device id to use [0]',
                        default=0, type=int)
    parser.add_argument('--cpu', dest='cpu_mode',
                        help='Use CPU mode (overrides --gpu)',
                        action='store_true')

    parser.add_argument('--classes', dest='classes',
                        choices=CLASSES.keys(), default='voc')
    parser.add_argument('--caffemodel', dest='caffemodel',
                        default='/home/ros/code/py-faster-rcnn.bak/data/faster_rcnn_models/zf_voc.caffemodel')
    parser.add_argument('--prototxt', dest='prototxt',
                        default='/home/ros/code/py-faster-rcnn.bak/data/faster_rcnn_models/zf_voc.pt')

    args = parser.parse_args()

    return args
