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
  id = db.Column(db.Integer, primary_key=True)
  path = db.Column(db.String(255), unique=True, nullable=False)
  camera = db.Column(db.String(255), unique=False, nullable=False)
  datetime = db.Column(db.DateTime, unique=False, nullable=False)

class ImageSchema(ma.ModelSchema):
  class Meta:
    model = Image
    # fields = ('id', 'path', 'camera', 'datetime')

class Recognition(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  normal_situation = db.Column(db.Float, unique=False, nullable=False)
  aggression_frontal = db.Column(db.Float, unique=False, nullable=False) 
  aggression_lateral = db.Column(db.Float, unique=False, nullable=False) 
  aggression_vertical = db.Column(db.Float, unique=False, nullable=False) 
  aggression_overtaking = db.Column(db.Float, unique=False, nullable=False) 
  curiosity = db.Column(db.Float, unique=False, nullable=False) 
  queuing_fewer = db.Column(db.Float, unique=False, nullable=False) 
  queuing_crowded = db.Column(db.Float, unique=False, nullable=False) 
  drinking_water = db.Column(db.Float, unique=False, nullable=False) 
  low_visibility = db.Column(db.Float, unique=False, nullable=False)
  image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
  image = db.relationship("Image", backref="recognition")

class RecognitionSchema(ma.ModelSchema):
  class Meta:
    model = Recognition
  image = ma.Nested(ImageSchema)

class Segmentation(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  is_milking = db.Column(db.Boolean, nullable=False)
  distance_array = db.Column(db.String(255), nullable=False)
  n_cows = db.Column(db.Integer, nullable=False)
  n_humans = db.Column(db.Integer, nullable=False)
  image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
  image = db.relationship("Image", backref="segmentation")

class SegmentationSchema(ma.ModelSchema):
  class Meta:
    model = Segmentation
  image = ma.Nested(ImageSchema)

# class Distance(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   distance = db.Column(db.Integer, nullable=False)

db.create_all()
db.session.commit()

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/barn/images/last/info')
def get_last_image_info():
  info = ftp.get_last_jpeg_info()
  image = Image.query.filter_by(path=info['path']).first()
  if image is None:
    image = Image(path=info['path'], camera=info['camera'], datetime=info['datetime'])
    db.session.add(image)
    db.session.commit()
  image_schema = ImageSchema(many=False)
  result = image_schema.dump(image)
  return jsonify(result)

@app.route('/barn/images/info')
def get_images_info():
  images = Image.query.all()
  image_schema = ImageSchema(many=True)
  result = image_schema.dump(images)
  return jsonify(result)

@app.route('/barn/images/<id>')
def get_images_file(id):
  image = Image.query.get(id)
  raw_image = ftp.get_jpeg(image.path)
  return send_file(raw_image, mimetype='image/jpeg')

@app.route('/barn/scenerecognition')
def get_images_scene_recognition():
  count = Recognition.query.count()
  offset = count - 10 if count - 10 >= 0 else 0
  recognitions = Recognition.query.offset(offset).limit(10).all()
  recognition_schema = RecognitionSchema(many=True)
  result = recognition_schema.dump(recognitions)
  return jsonify(result)

@app.route('/barn/scenerecognition/<id>')
def get_images_scene_recognition_specific(id):
  image = Image.query.get(id)
  recognition = Recognition.query.filter_by(image_id=image.id).first()
  if recognition is None:
    raw_image = ftp.get_jpeg(image.path)
    result = scene_recognition.prediction(raw_image)
    recognition = Recognition(normal_situation=result['normal_situation'], aggression_frontal=result['aggression_frontal'], aggression_lateral=result['aggression_lateral'], aggression_vertical=result['aggression_vertical'], aggression_overtaking=result['aggression_overtaking'], curiosity=result['curiosity'], queuing_fewer=result['queuing_fewer'], queuing_crowded=result['queuing_crowded'], drinking_water=result['drinking_water'], low_visibility=result['low_visibility'], image=image)
    db.session.add(recognition)
    db.session.commit()
  recognition_schema = RecognitionSchema(many=False)
  result = recognition_schema.dump(recognition)
  return jsonify(result)

@app.route('/barn/instancesegmentation')
def get_instance_segmentation():
  count = Segmenation.query.count()
  offset = count - 10 if count - 10 >= 0 else 0
  segmentations = Segmenation.query.offset(offset).limit(10).all()
  segmentation_schema = SegmenationSchema(many=True)
  result = segmentation_schema.dump(segmentations)
  return jsonify(result)

@app.route('/barn/instancesegmentation/<id>/image')
def get_image_instance_segmentation(id):
  image = Image.query.get(id)
  raw_image = ftp.get_jpeg(image.path)
  result = instance_segmentation.predict(raw_image)
  segmentation = Segmentation.query.filter_by(image_id=image.id).first()
  if segmentation is None:
    print(f"########## {result[1]['distance_array']}", file=sys.stdout)
    segmentation = Segmentation(is_milking=result[1]['is_milking'], distance_array=str(result[1]['distance_array']), n_cows=result[1]['n_cows'], n_humans=result[1]['n_humans'], image=image)
    db.session.add(segmentation)
    db.session.commit()
  return send_file(result[0], mimetype='image/jpeg')

@app.route('/barn/instancesegmentation/<id>/features')
def get_features_instance_segmentation(id):
  image = Image.query.get(id)
  segmentation = Segmentation.query.filter_by(image_id=image.id).first()
  segmentation_schema = SegmentationSchema(many=False)
  result = segmentation_schema.dump(segmentation)
  return jsonify(result)

@app.route('/barn/sensors/<id>')
def get_sensor_request(id):
 result = barn_sensors.get_data(id)
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
  # instance_segmentation = InstanceSegmentation(weight_path='barn/prediction_models/mask_rcnn_coco.h5')
  
  # Barn Sensors
  barn_sensors = BarnSensors(getenv('AZURE_STORAGE_ACCOUNT'), getenv('AZURE_ACCESS_KEY'), getenv('AZURE_TABLE_NAME'), getenv('AZURE_API_VERSION'))

  app.run(debug=True, host='0.0.0.0')