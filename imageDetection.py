import csv
import os
import requests
from Crypto.Cipher import AES
import face_recognition
def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s)+7) // 8, byteorder='big')
def encrypt(key, filename):
    chunk_size = 64*1024
    output_file = filename+".enc"
    IV = b'EncryptionOf16By'
    file_size = str(os.path.getsize(filename)).zfill(16)
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    with open(filename, 'rb') as inputfile:
        with open(output_file, 'wb') as outf:
            outf.write((file_size.encode('utf-8')))
            outf.write(IV)
            while True:
                chunk = inputfile.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                   chunk += ' '.encode('utf-8')*(16 - len(chunk)%16)
                outf.write(encryptor.encrypt(chunk))

def decrypt(key, filename):
        chunk_size = 64*1024
        output_file = "decrypted"+filename[:-4]
        with open(filename, 'rb') as inf:
            filesize = int(inf.read(16))
            IV = inf.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, IV)
            with open(output_file, 'wb') as outf:
                while True:
                    chunk = inf.read(chunk_size)
                    if len(chunk)==0:
                        break
                    outf.write(decryptor.decrypt(chunk))
                outf.truncate(filesize)
def compare():
    picture_of_me = face_recognition.load_image_file("image.jpeg")
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
    unknown_picture = face_recognition.load_image_file("image.jpeg")
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
    results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)
    if results[0] == True:
        print("It's a picture of me!")
    else:
        print("It's not a picture of me!")

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
#over here we are hitting url with the range lower = 1 and higher = depends upon the size of the csv file so we will make higher = (csv's length - 16) because we want 16 bits length which becomes our 
# so here it will be higher= 467-44 = 423
r = requests.get(url="http://quest.phy.stevens.edu:5050/main?lower=1&higher=422&amount=1")
startPosition = r.json()['finalrandomarray'][0]
key = readCSVfile(startPosition)
# input_file = open("download.jpeg")
# input_data = input_file.read()
# input_file.close()
# decrypt(key,"download.jpeg.enc")
compare()

# encryption_suite = AES.new(key, AES.MODE_CBC, 'EncryptionOf16By')
# cipher_text = encryption_suite.encrypt(input_data)

decryption_suite = AES.new(key, AES.MODE_CBC, 'EncryptionOf16By')
#print("Decrypted key is", decryption_suite.decrypt(cipher_text))