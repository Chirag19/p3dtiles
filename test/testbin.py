#!/usr/bin/python3
#-*-coding:utf-8-*-

__author__ = "chenxh"

"""
练习使用二进制的读写和格式
"""

import os, sys, struct
import pickle, json
from p3dtiles.FileUtils.FileHelper import FileHelper
import numpy, pandas

filepath = r"C:\Users\C\Desktop\output\0\0.b3dm"

def writetest():
    with open(filepath, 'wb') as binfile:
        a = "hello"
        b = "world!"
        c = 2
        d = 45.123
        byte = struct.pack('5s6sif', bytes(a.encode('utf-8')), bytes(b.encode('utf-8')), c, d)
        binfile.write(byte)

def readtest():
    with open(filepath, 'rb') as binfile:
        byte = binfile.read()
        a, b, c, d = struct.unpack('5s6sif', byte) # 必须满匹配
        print(str(a, 'utf-8'), str(b, 'utf-8'), c, d)

def readdemob3dm():
    # abs_path = os.path.abspath(filepath)
    from p3dtiles.TileFormat.B3dm import B3dm
    b3dm = B3dm(r"D:\MyCodes\p3dtiles\test\testData\tile.b3dm")
    b3dm_dict = b3dm.toDict()
    FileHelper.save2jsonfile(r"D:\MyCodes\p3dtiles\test\testData\tile.b3dm.json", b3dm_dict, False)

def readdemopnts():
    from p3dtiles.TileFormat.Pnts import Pnts
    pnts = Pnts(r"C:\Users\C\Desktop\11.pnts")
    pass

def readdemoi3dm():
    pass

if __name__ == '__main__':
    readdemopnts()