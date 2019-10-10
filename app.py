from os import getenv, path
from flask import Flask, render_template, send_file, jsonify, request
from dotenv import load_dotenv
from barn.image_ftp_collector import ImageFTPCollector
from barn.scene_recognition import SceneRecognition
from keras.models import load_model

app = Flask(__name__)
model = None

APP_ROOT = path.join(path.dirname(__file__), '..')
dotenv_path = path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

ftp_host = getenv('FTP_HOST')
ftp_user = getenv('FTP_USER')
ftp_password = getenv('FTP_PASSWORD')

def load_prediction_model():
  global model
  model = load_model('barn/models/scene_recognition_model.h5')
  model._make_predict_function()

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/barn/lastimage/info')
def last_image_info():
  collector = ImageFTPCollector(ftp_host, ftp_user, ftp_password, '5C033BCPAGBC9CE')
  img = collector.get_last_jpeg_info()
  return jsonify(img)

@app.route('/barn/lastimage')
def last_image_file():
  raw_image_path = request.args.get('ftp')
  collector = ImageFTPCollector(ftp_host, ftp_user, ftp_password, '5C033BCPAGBC9CE')
  raw_image = collector.get_jpeg(raw_image_path)
  return send_file(raw_image, mimetype='image/jpeg')

@app.route('/barn/scenerecognition')
def scene_recognition():
  raw_image_path = request.args.get('ftp')
  collector = ImageFTPCollector(ftp_host, ftp_user, ftp_password, '5C033BCPAGBC9CE')
  raw_image = collector.get_jpeg(raw_image_path)
  sr = SceneRecognition(model)
  result = sr.recognition(raw_image)
  return jsonify(result)

@app.after_request
def set_response_headers(response):
  response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
  response.headers['Pragma'] = 'no-cache'
  response.headers['Expires'] = '0'
  return response

if __name__ == '__main__':
  load_prediction_model()
  app.run(debug=True,host='0.0.0.0')