import requests
import datetime
import time
import hmac
import hashlib
import base64
import json 

class BarnSensors:
  def __init__(self, storage_account, access_key, table_name, api_version):
    self.storage_account = storage_account
    self.access_key = access_key
    self.table_name = table_name
    self.api_version = api_version

  def get_data(self, sensor_id):
    temperature = []
    humidity = []
    motion = []
    timestamp = []
    response_text = self.request(sensor_id)
    datas = json.loads(response_text)
    for data in datas['value'][-10:]:
      temperature.append(data['temperature'])
      humidity.append(data['humidity'])
      motion.append(data['motion'])
      time_str = data['Timestamp']
      result = datetime.datetime.strptime(time_str.split('.')[0], '%Y-%m-%dT%H:%M:%S')
      offset = datetime.datetime.now() - datetime.datetime.utcnow()
      result = result + offset
      timestamp.append(result.strftime("%m/%d %H:%M"))
    return {
      'temperature': temperature,
      'humidity': humidity,
      'motion': motion,
      'timestamp': timestamp
    }

  def request(self, sensor_id):
    # TODO last 10 datas
    start='2019-10-10T13:07:10.073Z'
    request_time = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    string_to_sign = f'{request_time}\n/{self.storage_account}/{self.table_name}'
    signed_string = base64.b64encode(hmac.new(base64.b64decode(self.access_key), msg=string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()).decode()
    headers = {
        'x-ms-date' : request_time,
        'Authorization' : f'SharedKeyLite {self.storage_account}:{signed_string}',
        'x-ms-version' : self.api_version,
        'Accept' : 'application/json;odata=nometadata'
    }
    filter = f'Timestamp ge datetime\'{start}\' and PartitionKey eq \'{sensor_id}\''
    url = f'https://{self.storage_account}.table.core.windows.net/{self.table_name}?$filter={filter}'
    response = requests.get(url, headers = headers)
    return response.text
