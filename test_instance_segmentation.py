from barn.instance_segmentation import InstanceSegmentation
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
instanceSeg = InstanceSegmentation(weight_path='barn/models/mask_rcnn_coco.h5')
result = instanceSeg.predict(raw_image)
print(result)

#import matplotlib as plt
#plt.pyplot.savefig('foo.png')
