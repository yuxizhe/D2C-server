# -*- coding: utf-8 -*
from flask import Flask, jsonify, request
from service.tf import tfServer

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['png', 'PNG', 'jpg', 'jpeg'])

from elasticapm.contrib.flask import ElasticAPM
app.config['ELASTIC_APM'] = {
  # Set the required service name. Allowed characters:
  # a-z, A-Z, 0-9, -, _, and space
  'SERVICE_NAME': 'D2C-server',

  'SERVER_URL': 'https://g.dappwind.com/apm/',

  # Set the service environment
#   'ENVIRONMENT': 'debug',
}
# apm = ElasticAPM(app)

@app.route('/')
def root():
    return 'D2C后台服务'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/generate/form', methods=['POST'])
def generate_form():
    if request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save('images/'+file.filename)
            result = tfServer('images/'+file.filename)
            return jsonify({'success': 'true', 'data': result})
    return jsonify({'success': 'false', 'message': '请传文件-file'})


if __name__ == '__main__':
    # app.debug = True
    app.run(host="0.0.0.0", port=5000)
