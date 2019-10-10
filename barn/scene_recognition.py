from keras.models import load_model
import numpy as np
import cv2

class SceneRecognition:

  def __init__(self, model, img_height=256, img_width=256):
    self.img_width = img_width
    self.img_height = img_height
    self.model = load_model(model)
    self.model._make_predict_function()

  def loadFrame(self, frame):
    file_bytes = np.asarray(bytearray(frame.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
    frame = cv2.resize(image, (self.img_height, self.img_width), interpolation=cv2.INTER_CUBIC)
    return frame

  def preProcessFrame(self, frame):
    frame = cv2.flip(frame, 0)
    brightness = 20
    contrast = -20
    frame = np.int16(frame) * (contrast/127+1) - contrast + brightness
    frame = np.clip(frame, 0, 255)
    frame = np.uint8(frame)
    return frame

  def prediction(self, raw_image):
    raw_image = self.loadFrame(raw_image)
    raw_image = self.preProcessFrame(raw_image)
    raw_image = raw_image.reshape(1, self.img_height, self.img_width, 1)
    label_names = [
      'Normal situation', 
      'Aggression frontal', 
      'Aggression lateral', 
      'Aggression vertical', 
      'Aggression overtaking', 
      'Curiosity', 
      'Queuing fewer', 
      'Queuing crowded', 
      'Drinking water', 
      'Low visibility'
    ]
    predictions = self.model.predict(raw_image)
    return {
      'labels': label_names,
      'predictions': predictions[0].tolist()
    }
