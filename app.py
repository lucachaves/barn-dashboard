from os import getenv, path
from flask import Flask, render_template, send_file
from dotenv import load_dotenv
from barn.image_ftp_collector import ImageFTPCollector

app = Flask(__name__)

APP_ROOT = path.join(path.dirname(__file__), '..')
dotenv_path = path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

ftp_host = getenv('FTP_HOST')
ftp_user = getenv('FTP_USER')
ftp_password = getenv('FTP_PASSWORD')

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/barn/lastimage')
def last_image():
  collector = ImageFTPCollector(ftp_host, ftp_user, ftp_password, '5C033BCPAGBC9CE')
  img = collector.get_last_jpeg()
  return send_file(img['figure'], mimetype='image/jpeg', as_attachment=True, attachment_filename='%s.jpg' % img['time'])

if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0')