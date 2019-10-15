from os import path, getenv
from flask import Flask, render_template, send_file, jsonify, request
from dotenv import load_dotenv
from barn.image_ftp_collector import ImageFTPCollector
from barn.scene_recognition import SceneRecognition
from barn.instance_segmentation import InstanceSegmentation
from barn.barn_sensors import BarnSensors

app = Flask(__name__)
ftp = None
scene_recognition = None
barn_sensors = None
instance_seg = None

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
  result = scene_recognition.prediction(raw_image)
  return jsonify(result)

@app.route('/barn/instancesegmentation')
def instance_segmentation():
  raw_image_path = request.args.get('ftp')
  raw_image = ftp.get_jpeg(raw_image_path)
  raw_image = instanceSeg.predict(raw_image)
  return send_file(raw_image, mimetype='image/jpeg')

@app.route('/barn/sensorrequest')
def sensor_request():
 result = barn_sensors.get_data('A81758FFFE03580A')
 return result

@app.after_request
def set_response_headers(response):
  response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
  response.headers['Pragma'] = 'no-cache'
  response.headers['Expires'] = '0'
  return response

if __name__ == '__main__':
  load_dotfile_env()
  ftp = ImageFTPCollector(getenv('FTP_HOST'), getenv('FTP_USER'), getenv('FTP_PASSWORD'), '5C033BCPAGBC9CE')
  scene_recognition = SceneRecognition('barn/models/scene_recognition_model.h5')
  instance_seg = InstanceSegmentation(weight_path='barn/models/mask_rcnn_coco.h5')
  barn_sensors = BarnSensors(getenv('AZURE_STORAGE_ACCOUNT'), getenv('AZURE_ACCESS_KEY'), getenv('AZURE_TABLE_NAME'), getenv('AZURE_API_VERSION'))
  app.run(debug=True,host='0.0.0.0')