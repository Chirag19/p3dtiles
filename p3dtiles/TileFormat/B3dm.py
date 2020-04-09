#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

import struct, json
from .. FileUtils.FileHelper import FileHelper
from . TileBodyTable.FeatureTable import FeatureTable
from . TileBodyTable.BatchTable import BatchTable

class B3dm:
    '''
    3dtiles瓦片数据文件的一种：批量模型类型，即*.b3dm文件
    '''
    def __init__(self, b3dm_file):
        byte = None
        import _io
        if isinstance(b3dm_file, _io.BufferedReader):
            byte = b3dm_file.read()
        else:
            with open(b3dm_file, 'rb') as file_handle:
                byte = file_handle.read()
        # 读文件头部
        self.b3dmHeader = B3dmHeader(byte[0:28])
        # 读数据体
        self.b3dmBody = B3dmBody(self.b3dmHeader, byte[28:self.b3dmHeader.byteLength])

    def toDict(self):
        return {
            "B3dm.Header" : self.b3dmHeader.toDict(),
            "B3dm.Body" : self.b3dmBody.toDict()
        }

class B3dmHeader:
    '''
    b3dm瓦片的文件头信息, 可使用b3dm的前28字节构造
    '''
    def __init__(self, buffer_data):
        fmt = '4s6I' # b3dm死格式，官方规范没更改请勿改动
        self.header = struct.unpack(fmt, buffer_data)
        # 7个数据
        self.magic = 'b3dm' # 常量，'b3dm'
        self.version = self.header[1] # 版本，目前是1
        self.byteLength = self.header[2] # 整个b3dm文件大小包括header和body
        self.featureTableJSONByteLength = self.header[3] # featureTable JSON的大小
        self.featureTableBinaryByteLength = self.header[4] # featureTable 二进制的大小
        self.batchTableJSONByteLength = self.header[5] # batchTable JSON的大小，0为不存在 
        self.batchTableBinaryByteLength = self.header[6] # batchTable 二进制大小，若上面是0这个也是0

    def toDict(self):
        return {
            "magic": self.magic,
            "version": self.version,
            "byteLength": self.byteLength,
            "featureTableJSONByteLength": self.featureTableJSONByteLength,
            "featureTableBinaryByteLength": self.featureTableBinaryByteLength,
            "batchTableJSONByteLength": self.batchTableJSONByteLength,
            "batchTableBinaryByteLength": self.batchTableBinaryByteLength
        }

    def toString(self):
        header_dict = self.toDict()
        header_jsonstr = json.dumps(header_dict)
        return header_jsonstr

class B3dmBody:
    '''
    body = featuretable + [batchtable] + glb
        featuretable = jsonheader + [binbody]
        [batchtable] = [jsonheader] + [binbody]
    '''
    def __init__(self, header, buffer_data):
        _buffer = buffer_data
        self.feature_table = FeatureTable(_buffer, header)
        if header.batchTableJSONByteLength == 0:
            self.batch_table = BatchTable.DEFAULT # 默认给个空的batchtable
            return
        else:
            self.batch_table = BatchTable(_buffer, header, self.feature_table.ftJSON.JSON["BATCH_LENGTH"])

    def toDict(self):
        '''
        以字典形式，返回B3dmBody
        '''
        bt = self.batch_table
        if isinstance(self.batch_table, dict) == False:
            bt = self.batch_table.toDict()
        return {
            "B3dm.Body.FeatureTable": self.feature_table.toDict(),
            "B3dm.Body.BatchTable": bt
        }

    def toString(self):
        '''
        以字典的字符串形式，返回B3dmBody
        '''
        body_dict = self.toDict()
        return json.dumps(body_dict)
