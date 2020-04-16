import os

class FileHelper:
    def __init__(self):
        pass

    @staticmethod
    def filesize(path:str, fmt:str = 'B'):
        """ 获取文件大小，默认单位是Bytes

        Args:

            path: 文件全路径

            fmt: 字符串，默认是B，即Bytes。可传入'KB'或'MB'

        """
        if os.path.isfile(path) == False:
            raise Exception("伙计, path不是指向一个文件啊")

        size = os.path.getsize(path)
        if (fmt == 'B'):
            return size 
        elif (fmt == 'KB'):
            return size / 1024.0
        elif (fmt == 'MB'):
            return size / (1024.0 * 1024.0)
        else:
            return size
            

    @staticmethod
    def bin2str(bin:bytes):
        """ 二进制字符串数据（b'xx'）转换为UTF-8编码的字符串
        """
        return str(bin, 'utf-8')

    @staticmethod
    def hasVal(obj, val):
        """判断是否有属性，如果有返回属性值，如果没有返回None
        """
        if type(obj) == dict:
            if val in obj:
                return obj[val]
            else:
                return None
        else:
            if hasattr(obj, val):
                return obj[val]
            else:
                return None

    @staticmethod
    def save2jsonfile(path:str, dict_data:dict, minified:bool = True):
        """ 字典存为json的快捷方法
        """
        if os.path.isfile(path) == False:
            raise Exception("伙计, path不是指向一个文件啊")

        with open(path, 'w') as file_handle:
            import json
            if minified:
                file_handle.write(json.dumps(dict_data))
            else:
                file_handle.write(json.dumps(dict_data, indent = 4))