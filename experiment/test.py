#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: test.py
# Author: Qian Ge <geqian1001@gmail.com>

import os
import platform
import numpy as np
import skimage.transform

import sys
sys.path.append('../')
import loader
import configs.parsecfg as parscfg
import src.bbox.bboxgt as bboxgt
import src.utils.viz as viz
import src.utils.image as image

if __name__ == "__main__":
    pathconfig = parscfg.parse_cfg('configs/path.cfg')
    pretrained_path = pathconfig['coco_pretrained_npy_path']
    data_dir = pathconfig['test_image_path']
    im_name = pathconfig['test_image_name']

    netconfig = parscfg.parse_cfg('configs/coco80.cfg')
    im_rescale = netconfig['rescale']
    n_channel = netconfig['n_channel']
    bsize = netconfig['bsize']
    obj_score_thr = netconfig['obj_score_thr']
    nms_iou_thr = netconfig['nms_iou_thr']
    n_class = netconfig['n_class']
    anchors = netconfig['anchors']

    image_data, _ = loader.load_VOC(batch_size=bsize)

    batch_data = image_data.next_batch_dict()

    im_shape = batch_data['image'][0].shape[:2]
    rescale_shape = 416
    stride_list = [32, 16, 8]
    # print(batch_data['label'][0])
    # gt_anchor, gt_label, gt_dict, gt_mask = bboxgt.get_target_anchor(
    #     batch_data['label'][0], batch_data['shape'][0], rescale_shape, stride_list, anchors, n_class)

    gt_bbox_para = np.array([bbox[1:] for bbox in batch_data['label'][0]])
    gt_bbox_label = [bbox[0] for bbox in batch_data['label'][0]]

    # o_im = image.rescale_image(batch_data['image'][0]*255, batch_data['shape'][0])
    # viz.draw_bounding_box(o_im, gt_bbox_para, label_list=None, box_type='xyxy')

    # rescale_im = image.rescale_image(batch_data['image'][0]*255, rescale_shape)
    # viz.draw_bounding_box(rescale_im, gt_anchor, label_list=None, box_type='xyxy')

    # print(gt_dict)
    # print('-------')
    target = bboxgt.TargetAnchor([416, 320], stride_list, anchors, n_class)
    # gt = target.get_target_anchor(batch_data['label'], batch_data['shape'], rescale_shape, True)
    gt = target.get_yolo_target_anchor(batch_data['label'], batch_data['shape'], rescale_shape, True)
    # print(np.array_equal(gt_mask, gt_mask_2))

    # print(gt_mask.shape)
    print(gt.shape)
    # print(target_anchor_batch[0],)
    # rescale_im = image.rescale_image(batch_data['image'][0]*255, rescale_shape)
    # o_im = image.rescale_image(batch_data['image'][0]*255, batch_data['shape'][0])
    # viz.draw_bounding_box(o_im, gt_bbox_para, label_list=None, box_type='xyxy')
    # viz.draw_bounding_box(rescale_im, target_anchor_batch[0], label_list=None, box_type='xyxy')

    # for g1, g2 in zip(gt_mask, gt[0]):
    #     print(g1.shape, g2.shape)
    #     for gg1, gg2 in zip(g1, g2):
    #         print(gg1.shape, gg2.shape)
    #         print((gg1 == gg2).all())

        