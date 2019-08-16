# 获取文件夹中的文件路径
import os


def getFilePathList(dirPath, partOfFileName=''):
    allFileName_list = list(os.walk(dirPath))[0][2]
    fileName_list = [k for k in allFileName_list if partOfFileName in k]
    filePath_list = [os.path.join(dirPath, k) for k in fileName_list]
    return filePath_list


# 生成新的xml文件
import xml.etree.ElementTree as ET


def generateNewXmlFile(old_xmlFilePath, new_xmlFilePath, new_size):
    new_width, new_height = new_size
    with open(old_xmlFilePath) as file:
        fileContent = file.read()
    root = ET.XML(fileContent)
    # 获得图片宽度变化倍数，并改变xml文件中width节点的值
    width = root.find('size').find('width')
    old_width = int(width.text)
    try:
        width_times = new_width / old_width

        width.text = str(new_width)
        # 获得图片高度变化倍数，并改变xml文件中height节点的值
        height = root.find('size').find('height')
        old_height = int(height.text)
        height_times = new_height / old_height
        height.text = str(new_height)
        # 获取标记物体的列表，修改其中xmin,ymin,xmax,ymax这4个节点的值
        object_list = root.findall('object')
        for object_item in object_list:
            bndbox = object_item.find('bndbox')
            xmin = bndbox.find('xmin')
            xminValue = int(xmin.text)
            xmin.text = str(int(xminValue * width_times))
            ymin = bndbox.find('ymin')
            yminValue = int(ymin.text)
            ymin.text = str(int(yminValue * height_times))
            xmax = bndbox.find('xmax')
            xmaxValue = int(xmax.text)
            xmax.text = str(int(xmaxValue * width_times))
            ymax = bndbox.find('ymax')
            ymaxValue = int(ymax.text)
            ymax.text = str(int(ymaxValue * height_times))
        tree = ET.ElementTree(root)
        tree.write(new_xmlFilePath)
    except Exception as e:
        print("错误："+old_xmlFilePath)


# 修改文件夹中的若干xml文件
def batch_modify_xml(old_dirPath, new_dirPath, new_size):
    xmlFilePath_list = getFilePathList(old_dirPath, '.xml')
    for xmlFilePath in xmlFilePath_list:
        xmlFileName = os.path.split(xmlFilePath)[1]
        new_xmlFilePath = os.path.join(new_dirPath, xmlFileName)
        generateNewXmlFile(xmlFilePath, new_xmlFilePath, new_size)


# 生成新的jpg文件
from PIL import Image


def generateNewJpgFile(old_jpgFilePath, new_jpgFilePath, new_size):
    old_image = Image.open(old_jpgFilePath)
    new_image = old_image.resize(new_size, Image.ANTIALIAS)
    try:
        new_image.save(new_jpgFilePath)
    except Exception as e:
        captcha=new_image.convert('RGB')
        captcha.save(new_jpgFilePath)




# 修改文件夹中的若干jpg文件
def batch_modify_jpg(old_dirPath, new_dirPath, new_size):
    if not os.path.isdir(new_dirPath):
        os.makedirs(new_dirPath)
    xmlFilePath_list = getFilePathList(old_dirPath, '.xml')
    for xmlFilePath in xmlFilePath_list:
        old_jpgFilePath = xmlFilePath[:-4] + '.jpg'
        jpgFileName = os.path.split(old_jpgFilePath)[1]
        new_jpgFilePath = os.path.join(new_dirPath, jpgFileName)
        generateNewJpgFile(old_jpgFilePath, new_jpgFilePath, new_size)


if __name__ == '__main__':
    old_dirPath = '/Users/zx/Desktop/game/train/'
    new_width = 416
    new_height = 416
    new_size = (new_width, new_height)
    new_dirPath = 'ximages_%sx%s' % (str(new_width), str(new_height))
    batch_modify_jpg(old_dirPath, new_dirPath, new_size)
    batch_modify_xml(old_dirPath, new_dirPath, new_size)