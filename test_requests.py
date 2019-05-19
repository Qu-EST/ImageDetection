import requests
import encryptor
import json

enc = encryptor.encryptor()

refid = enc.encrypt('unknown.jpg')


with open('unknown.jpg.enc', 'rb') as uki:
    img = bytearray(uki.read())


payload = {'refid':refid}

data = json.dumps(payload)


# #print(refid)

result = requests.post('http://127.0.0.1:5000/compare_image', data=img, headers={'Content-Type': 'application/octet-stream'})

#print(result)

result = requests.get('http://127.0.0.1:5000/compare_image',json=data, headers = {'content-type': 'application/json'})
print(result.text)
