#!/usr/bin/env python
# -*- coding:utf-8 -*-

from struct import *
import json
import numpy as np
import math


def get_point(point, points):
    '''获取与给定点最相近的一个点'''
    for p in points:
        if p['rotation'] == point['rotation']:
            return p
        if p['rotation'] > point['rotation']:
            return None


def get_points(point, points1, points2):
    '''获取构成三角面的三个点'''
    result1 = get_point(point, points1)
    result2 = get_point(point, points2)
    if result1 is None or result2 is None:
        return None
    return [point, result1, result2]


with open('data', 'rb') as f:
    data = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    results = []
    indexs = [15, 13, 11, 9, 7, 5, 3, 1, 14, 12, 10, 8, 6, 4, 2, 0]
    for i in range(0, 13468):
        (x, y, z) = unpack("fff", f.read(12))
        f.seek(8, 1)
        ring = unpack("I", f.read(4))
        f.seek(8, 1)
        rotation = round(math.atan2(y, x), 2)
        data[ring[0]].append({'x': x, 'y': y, 'z': z, 'rotation': rotation})
        # print (x, y, z), str(ring), str(rotation)
    for i in range(0, len(indexs)):
        index = indexs[i]
        data[index] = sorted(data[index], key=lambda point: point['rotation'])
        if i > 0:
            for j in range(0, len(data[index - 1])):
                result = get_points(
                    data[index - 1][j], data[index - 1][j + 1:], data[index])
                if result is None:
                    continue
                results.append(result)
                print result

    with open('point.json', 'w') as wj:
        json.dump(results, wj)
