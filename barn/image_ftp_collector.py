from ftplib import FTP
import time
import sys
import os
from io import BytesIO
import datetime

class ImageFTPCollector:  

  def __init__(self, host, user, password, camera):
    self.camera = camera
    self.host = host
    self.user = user
    self.password = password
    print(f'FTP {self.host}', file=sys.stdout)

  def connect(self):
    ftp = FTP(self.host)
    ftp.login(self.user, self.password)
    return ftp

  def get_last_folder(self, dirname):
    files = []
    ftp = self.connect()
    ftp.dir(dirname, files.append)
    ftp.close()
    for file in files:
      tokens = file.split()
      if tokens[2] == '<DIR>':
        name = tokens[3]
    return name

  def get_most_recent_path(self):
    camera_dirname = f'/Barn/{self.camera}'
    last_date = self.get_last_folder(camera_dirname)
    last_date_dir = f'/Barn/{self.camera}/{last_date}/001/jpg/'
    last_hour = self.get_last_folder(last_date_dir)
    last_hour_dirname = f'/Barn/{self.camera}/{last_date}/001/jpg/{last_hour}'
    last_minute = self.get_last_folder(last_hour_dirname)
    return f'/Barn/{self.camera}/{last_date}/001/jpg/{last_hour}/{last_minute}'

  def get_last_jpeg_path(self):
    last_jpg = None
    dirname = self.get_most_recent_path()
    files = []
    ftp = self.connect()
    ftp.dir(dirname, files.append)
    ftp.close()
    for file in files:
      tokens = file.split()
      filename = tokens[3]
      if filename.endswith('.jpg'):
        last_jpg = filename
    return f'{dirname}/{last_jpg}'

  def get_datetime_file(self, dirname):
    files = []
    ftp = self.connect()
    ftp.dir(dirname, files.append)
    ftp.close()
    tokens = files[0].split()
    time_str = ' '.join(tokens[0:2])
    result = datetime.datetime.strptime(time_str, '%m-%d-%y %I:%M%p')
    offset = datetime.datetime.now() - datetime.datetime.utcnow()
    result = result + offset
    return {
      'date': result.strftime("%m/%d/%Y"),
      'time': result.strftime("%H:%M"),
      'full': result.strftime("%m/%d/%Y %H:%M"),
      'timestamp': result.timestamp()
    }

  def get_jpeg(self, path):
    figure = BytesIO()
    ftp = self.connect()
    ftp.retrbinary(f'RETR {path}', figure.write)
    figure.seek(0)
    ftp.close()
    return figure

  def get_last_jpeg_info(self):
    path = self.get_last_jpeg_path()
    datetime = self.get_datetime_file(path)
    return {
      'camera': self.camera,
      'path': path,
      'datetime': datetime
    }
