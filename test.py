from barn.scene_recognition import SceneRecognition
from barn.image_ftp_collector import ImageFTPCollector
from keras.models import load_model
from io import BytesIO
from PIL import Image
from os import getenv, path
from dotenv import load_dotenv

def create_test_image():
  file = BytesIO()
  # image = Image.new('RGB', size=(50, 50), color=(155, 0, 0))
  image = Image.open('temp/raw_image.jpg')
  image.save(file, 'JPEG')
  file.name = 'raw_image.jpg'
  file.seek(0)
  return file

raw_image = create_test_image()
model = load_model('barn/models/scene_recognition_model.h5')
sr = SceneRecognition(model)
result = sr.recognition(raw_image)
print(result)
