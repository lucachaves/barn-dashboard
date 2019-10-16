from barn.barn_sensors import BarnSensors
from barn.image_ftp_collector import ImageFTPCollector
from barn.instance_segmentation import InstanceSegmentation
from barn.scene_recognition import SceneRecognition
from dotenv import load_dotenv
from flask import Flask, render_template, send_file, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from os import path, getenv
import sys

load_dotenv()

app = Flask(__name__)
ftp = None
scene_recognition = None
instance_segmentation = None
barn_sensors = None

# Database Connection
database_uri = 'mysql://%s:%s@%s:%s/%s' % (getenv('MYSQL_USER'), getenv('MYSQL_PASSWORD'), getenv('MYSQL_HOST'), getenv('MYSQL_PORT'), getenv('MYSQL_DATABASE'))
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print(app.config['SQLALCHEMY_DATABASE_URI'], file=sys.stdout)
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Image(db.Model):
  __tablename__ = 'images'
  id = db.Column(db.Integer, primary_key=True)
  path = db.Column(db.String(80), unique=True, nullable=False)
  camera = db.Column(db.String(80), unique=False, nullable=False)
  datetime = db.Column(db.String(80), unique=True, nullable=False)

  def __init__(self, path, camera, datetime):
        self.path = path
        self.camera = camera
        self.datetime = datetime

class ImageSchema(ma.Schema):
  class Meta:
    fields = ('path', 'camera', 'datetime')

db.create_all()
db.session.commit()

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/barn/lastimage/info')
def last_image_info():
  img_info = ftp.get_last_jpeg_info()
  image = Image(path=img_info['path'], camera=img_info['camera'], datetime=img_info['datetime'])
  db.session.add(image)
  db.session.commit()
  return jsonify(img_info)

@app.route('/barn/lastimage')
def last_image_file():
  raw_image_path = request.args.get('ftp')
  raw_image = ftp.get_jpeg(raw_image_path)
  return send_file(raw_image, mimetype='image/jpeg')

@app.route('/barn/scenerecognition')
def scene_recognition_image():
  raw_image_path = request.args.get('ftp')
  raw_image = ftp.get_jpeg(raw_image_path)
  result = scene_recognition.prediction(raw_image)
  return jsonify(result)

@app.route('/barn/instancesegmentation')
def instance_segmentation_image():
  raw_image_path = request.args.get('ftp')
  raw_image = ftp.get_jpeg(raw_image_path)
  result = instance_segmentation.predict(raw_image)
  return send_file(result[0], mimetype='image/jpeg')

@app.route('/barn/images')
def test():
  images = Image.query.all()
  image_schema = ImageSchema(many=True)
  result = image_schema.dump(images)
  return jsonify(result)

@app.route('/barn/sensorrequest')
def sensor_request():
 result = barn_sensors.get_data('A81758FFFE03580D')
 return result

@app.after_request
def set_response_headers(response):
  response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
  response.headers['Pragma'] = 'no-cache'
  response.headers['Expires'] = '0'
  return response

if __name__ == '__main__':
  # FTP Connection
  ftp = ImageFTPCollector(getenv('FTP_HOST'), getenv('FTP_USER'), getenv('FTP_PASSWORD'), '5C033BCPAGBC9CE')
  print(f"ftp:{getenv('FTP_HOST')}", file=sys.stdout)
  
  # Scene Recognition
  scene_recognition = SceneRecognition('barn/prediction_models/scene_recognition_model.h5')
  
  # Instance Segmentation
  instance_segmentation = InstanceSegmentation(weight_path='barn/prediction_models/mask_rcnn_coco.h5')
  
  # Barn Sensors
  barn_sensors = BarnSensors(getenv('AZURE_STORAGE_ACCOUNT'), getenv('AZURE_ACCESS_KEY'), getenv('AZURE_TABLE_NAME'), getenv('AZURE_API_VERSION'))

  app.run(debug=True, host='0.0.0.0')