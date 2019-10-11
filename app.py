from os import path, getenv
from flask import Flask, render_template, send_file, jsonify, request
from dotenv import load_dotenv
from barn.image_ftp_collector import ImageFTPCollector
from barn.scene_recognition import SceneRecognition
#from barn.azure_sensors import sensorRequest

app = Flask(__name__)
ftp = None
sceneRecognition = None

def load_dotfile_env():
  APP_ROOT = path.join(path.dirname(__file__), '..')
  dotenv_path = path.join(APP_ROOT, '.env')
  load_dotenv(dotenv_path)

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/barn/lastimage/info')
def last_image_info():
  img = ftp.get_last_jpeg_info()
  return jsonify(img)

@app.route('/barn/lastimage')
def last_image_file():
  raw_image_path = request.args.get('ftp')
  raw_image = ftp.get_jpeg(raw_image_path)
  return send_file(raw_image, mimetype='image/jpeg')

@app.route('/barn/scenerecognition')
def scene_recognition():
  raw_image_path = request.args.get('ftp')
  raw_image = ftp.get_jpeg(raw_image_path)
  result = sceneRecognition.prediction(raw_image)
  return jsonify(result)

#@app.route('/barn/sensorrequest')
#def sensor_request():
#  result = sensorRequest()
#  return jsonify(result)

@app.after_request
def set_response_headers(response):
  response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
  response.headers['Pragma'] = 'no-cache'
  response.headers['Expires'] = '0'
  return response

if __name__ == '__main__':
  load_dotfile_env()
  ftp = ImageFTPCollector(getenv('FTP_HOST'), getenv('FTP_USER'), getenv('FTP_PASSWORD'), '5C033BCPAGBC9CE')
  sceneRecognition = SceneRecognition('barn/models/scene_recognition_model.h5')
  app.run(debug=True,host='0.0.0.0')