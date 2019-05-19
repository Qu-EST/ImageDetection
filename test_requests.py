import requests
import encryptor
import csv
import json

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s)+7) // 8, byteorder='big')

def readCSVfile(startPosition):
    with open('keys_binary.csv') as csvfile:
        readCSVfile = csv.reader(csvfile, delimiter=',')
        temporaryIndex = 0
        temporaryString = ''
        for row in readCSVfile:
            if(temporaryIndex >= startPosition and temporaryIndex-startPosition >= 0 and temporaryIndex-startPosition < 43):
                temporaryString = temporaryString+row[1]
            temporaryIndex+=1
            # print(row[0])
            # print(row[1])

        key = temporaryString[0:128]
    return bitstring_to_bytes(key)

enc = encryptor.encryptor()
r = requests.get(url="http://quest.phy.stevens.edu:5050/main?lower=1&higher=422&amount=1")
startPosition = r.json()['finalrandomarray'][0]
key = readCSVfile(startPosition)
enc.encrypt_file(key,'Lac.jpg')
with open('Lac.jpg.enc', 'rb') as uki:
    img = bytearray(uki.read())
payload = {'key':startPosition}
data = json.dumps(payload)
result = requests.post('http://127.0.0.1:5000/compare_image', data=img, headers={'Content-Type': 'application/octet-stream'})
result = requests.get('http://127.0.0.1:5000/compare_image',json=data, headers = {'content-type': 'application/json'})
print(result.text)
