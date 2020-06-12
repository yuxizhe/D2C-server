
# D2C机器学习生成CRM表单 - 服务端部署

## 接口

> https://api.dappwind.com/ai/generate/form

method:  `POST`

body: `file`  要识别的表单图片

## 原理
前端代码自动生成-机器学习 模型训练
> https://blog.dappwind.com/2020/05/13/index.html

前端代码自动生成-Opencv提取后模型分类
> https://blog.dappwind.com/2020/05/14/index.html

前端代码自动生成-文字识别并关联元素
> https://blog.dappwind.com/2020/05/15/index.html

前端代码自动生成 之 根据识别出的内容生成前端代码
> https://blog.dappwind.com/2020/05/18/index.html


## 包安装
```bash
pip3 install flask
pip3 install opencv-python-headless
pip3 install tf-nightly
pip3 install keras
pip3 install pillow
pip3 install pytesseract
```

>pip 版本过低时无法安装 tf-nightly
```bash
python3 -m pip install --upgrade pip
```

## 文字识别库安装
ubuntu
```bash
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-chi-sim
```
mac
```
brew install tesseract
```
然后手动复制https://github.com/tesseract-ocr/tessdata/blob/master/chi_sim.traineddata
到 /usr/local/Cellar/tesseract/4.1.1/share/tessdata


## 启动命令

```bash
lsof -i tcp:5000 | grep LISTEN | awk '{print $2}' | xargs kill -9

nohup python3 -u app.py > app.log 2>&1 &
```