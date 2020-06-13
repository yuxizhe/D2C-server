import cv2
import numpy as np
import os
import glob
import pytesseract
import re

# 获取图片内矩形函数

def cv_get_block(location):
    img = cv2.imread(location)
    # img resize to 700
    img = cv2.resize(
        img, (700, int(700/img.shape[1]*img.shape[0])), interpolation=cv2.INTER_AREA)

    # 转为灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 边缘检测
    binary = cv2.Canny(gray, 50, 100)

    # 检测轮廓
    # RETR_EXTERNAL  表示只检测最外层轮廓
    contours, hier = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 裁剪出的图片
    croppedImage = []
    # 位置信息和文案信息
    positionAndText = []

    for c in contours:  # 遍历轮廓
        rect = cv2.minAreaRect(c)  # 生成最小外接矩形

        # 计算最小面积矩形的坐标
        # 这个返回坐标点顺序是随机的
        box = cv2.boxPoints(rect)
        box = np.int0(box)  # 将坐标规范化为整数

        h = int(abs(box[3, 1] - box[1, 1]))
        w = int(abs(box[3, 0] - box[1, 0]))
        y = min(box[2][1], box[0][1])
        x = min(box[2][0], box[0][0])

        # 去除太小太大 的矩形，只保留合适的
        if (h > 500 or w > 600):
            continue
        if (h < 20 or w < 60):
            continue

        # print(h,w)
        # print(box)
        # 取出图片
        # image[y:y+h, x:x+w]
        cropped = img[y-5:y+h+5, x-5:x+w+5]

        # 识别矩形中的文字
        inner_text, before_text = element_ocr(cropped, img, x, y, w, h)

        # 传出
        positionAndText.append([box, inner_text, before_text])

        # 格式化为正方形
        cropped = resize_image(cropped)
        croppedImage.append(cropped)
        # 绘制矩形
        cv2.drawContours(img, [box], 0, (255, 0, 255), 1)

    # 输出 array 而不是list
    # 'Input data in `NumpyArrayIterator` should have rank 4. You passed an array with shape', (224, 224, 3))
    # 因为 ImageDataGenerator.flow 输入为 NumpyArray
    return np.array(croppedImage), np.array(positionAndText), img


min_side = 224
# 图像归一为 224 224


def resize_image(img):
    size = img.shape
    h, w = size[0], size[1]
    # 长边缩放为min_side
    scale = max(w, h) / float(min_side)
    new_w, new_h = int(w/scale), int(h/scale)
    resize_img = cv2.resize(img, (new_w, new_h))
    # 填充至min_side * min_side
    if new_w % 2 != 0 and new_h % 2 == 0:
        top, bottom, left, right = (
            min_side-new_h)/2, (min_side-new_h)/2, (min_side-new_w)/2 + 1, (min_side-new_w)/2
    elif new_h % 2 != 0 and new_w % 2 == 0:
        top, bottom, left, right = (
            min_side-new_h)/2 + 1, (min_side-new_h)/2, (min_side-new_w)/2, (min_side-new_w)/2
    elif new_h % 2 == 0 and new_w % 2 == 0:
        top, bottom, left, right = (
            min_side-new_h)/2, (min_side-new_h)/2, (min_side-new_w)/2, (min_side-new_w)/2
    else:
        top, bottom, left, right = (
            min_side-new_h)/2 + 1, (min_side-new_h)/2, (min_side-new_w)/2 + 1, (min_side-new_w)/2
    pad_img = cv2.copyMakeBorder(resize_img, int(top), int(bottom), int(left), int(
        right), cv2.BORDER_CONSTANT, value=[255, 255, 255])  # 从图像边界向上,下,左,右扩的像素数目
    # print pad_img.shape
    #cv2.imwrite("after-" + os.path.basename(filename), pad_img)
    return pad_img

# 文字过滤
def string_filter(text):
    new_text = re.sub('[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "", text)
    return new_text

# 识别元素内及元素前的文字
def element_ocr(cropped, img, x, y, w, h):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    # 识别矩形中的文字
    inner_text = string_filter(pytesseract.image_to_string(cropped, lang='chi_sim'))
    print('元素内文字:  ' + inner_text)

    # 识别矩形前的文字 往前200
    textAreaBefore = img[y:y+h, max(0, x-200):x]
    # cv2_imshow(textAreaBefore)
    # 识别前序文字
    before_text = string_filter(pytesseract.image_to_string(textAreaBefore, lang='chi_sim'))
    print('元素前区域文字：  '+before_text)

    return inner_text, before_text

# print(cv_get_block('./images/1.png'))
