# -*- coding: utf-8 -*

from flask import Flask, jsonify, request
from service.tf import tfServer

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['png', 'PNG', 'jpg', 'jpeg'])

@app.route('/')
def root():
    return 'D2C后台服务'

@app.route('/json')
def test():
    t = {'a':1}
    return jsonify(t)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
  if request.files:
    file = request.files['file']
    if file and allowed_file(file.filename):
      file.save('images/'+file.filename)
      result = tfServer('images/'+file.filename)
      return jsonify({'success': 'true', 'data': result})
  return jsonify({'success': 'false', 'message': '请传文件file'})

if __name__ == '__main__':
    # app.debug = True
    app.run(port=5000)