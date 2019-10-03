from ftplib import FTP
import time
import sys
import os
from io import BytesIO

class ImageFTPCollector:  

  def __init__(self, ftp_host, ftp_user, ftp_password, camera):
    self.camera = camera
    self.connect(ftp_host, ftp_user, ftp_password)

  def connect(self, host, username, password):
    ftp = FTP(host)
    ftp.login(username, password)
    self.ftp = ftp

  def get_last_folder(self, dirname):
    files = []
    self.ftp.dir(dirname, files.append)
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
    self.ftp.dir(dirname, files.append)
    for file in files:
      tokens = file.split()
      filename = tokens[3]
      if filename.endswith('.jpg'):
        last_jpg = filename
    return f'{dirname}/{last_jpg}'

  def get_timestamp_file(self, dirname):
    files = []
    self.ftp.dir(dirname, files.append)
    tokens = files[0].split()
    time_str = ' '.join(tokens[0:2])
    timestamp = time.strptime(time_str, '%m-%d-%y %I:%M%p')
    return time.mktime(timestamp)

  def get_last_jpeg(self):
    path = self.get_last_jpeg_path()
    time = self.get_timestamp_file(path)
    figure = BytesIO()
    self.ftp.retrbinary(f'RETR {path}', figure.write)
    figure.seek(0)
    return {
      'time': time,
      'figure': figure
    }
