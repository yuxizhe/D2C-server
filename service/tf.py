import tensorflow as tf
import json
from tensorflow import keras
import numpy as np
from keras.preprocessing.image import ImageDataGenerator

from service.cv import cv_get_block

print(tf.__version__)

html_model = tf.keras.models.load_model('./model/1589869679/')
# create a data generator
datagen = ImageDataGenerator(rescale=(1/255))


def tfServer(path):
    # 从图片CV获取元素
    #images,positionAndText ,img = cv_get_block('/content/pic/crm/1.png')
    images, positionAndText, img = cv_get_block(path)
    # 矩形元素 通过ImageDataGenerator 图像进一步处理
    # 需要注意的是，通过flow输出的数据是乱序的，并不会严格安装输入的顺序，所以对应关系要存储在label中
    input_data = datagen.flow(images, positionAndText)
    image_batch, boxes_batch = next(input_data)
    # 预测元素
    predicted_batch = html_model.predict(image_batch)

    # 结果归一
    predicted_id = np.argmax(predicted_batch, axis=-1)

    class_name = np.array(['Select', 'Button', 'Input'])
    # 结果对应上名字
    predicted_name = class_name[predicted_id]

    # print(predicted_name)
    # print(boxes_batch)
    # 图示结果
    #result_show(image_batch, predicted_name)
    #result_show_in_image(img, boxes_batch, predicted_name)

    result_list = []
    for index in range(len(boxes_batch)):
        item = np.append(boxes_batch[index], predicted_name[index])
        # 翻译命名
        # item = np.append(item, translate(boxes_batch[index][2]))
        result_list.append(item)

    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return json.JSONEncoder.default(self, obj)

    json_result = json.dumps(result_list, cls=NumpyEncoder)
    print(json_result)
    return json_result

# print(tfServer('./images/1.png'))