import requests
import datetime
import hmac
import hashlib
import base64

def sensorRequest():
    storageAccount = "barnmachinelearnistorage"
    accesskey = "5g0xfVRfXWWZvw5lQf7QLGg3eyBcyCaOrEi9gEU8G1mPssKpknRlWQRxqOuOv6C3qSFHEsRPJWGj+i3bjWRtWA=="
    tableName = "DecodedPayload"
    api_version = '2017-04-17'
    request_time = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    string_to_sign = request_time + '\n' +'/'+storageAccount+'/'+tableName


    signed_string = base64.b64encode(hmac.new(base64.b64decode(accesskey), msg=string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()).decode()
    #print(signed_string, string_to_sign)
    headers = {
        'x-ms-date' : request_time,
        'Authorization' : ('SharedKeyLite ' + storageAccount + ':' + signed_string),
        'x-ms-version' : api_version,
        'Accept' : 'application/json;odata=nometadata'
    }

    url = ('https://' + storageAccount + '.table.core.windows.net/'+tableName+"?$filter=Timestamp ge datetime'2019-10-10T13:07:10.073Z' and PartitionKey eq 'A81758FFFE03580A'")
    #print(url)
    r = requests.get(url, headers = headers)
    #print(r.status_code)
    #print('\n\n'+r.text)
    return r
