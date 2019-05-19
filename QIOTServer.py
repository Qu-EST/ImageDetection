from flask import Flask, request
import face_recognition as fr
import glob
import encryptor
import json


# constants
IMAGE_PATH ='images/*.jpg'      # image folder

# read all the images in the image folder
files = glob.glob(IMAGE_PATH)

encp = encryptor.encryptor()



# load all the known images to a library

known_image_enc = {}

for each_file in files:
    image = fr.load_image_file(each_file)
    image_enc = fr.face_encodings(image)[0]
    known_image_enc[each_file] = image_enc



def compare(unknown_image):
    pass

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Welcome to the Quantum IOT Server!'




@app.route('/compare_image', methods=['POST', 'GET'] )
def compare_image():

    if(request.method=='POST'):
        image1 = request.get_data()
        with open('unknown_server.jpeg.enc', 'wb+') as uk:
            uk.write(image1)
        return 'got data'
    else:
        refid = request.get_json()
        refid_dict = json.loads(refid)
        print(type(refid_dict['refid']))
        encp.decrypt(refid_dict['refid'], 'unknown_server.jpeg.enc')
        uk = fr.load_image_file('decrypted_unknown_server.jpeg')
        uk = fr.face_encodings(uk)[0]
        for key, value in known_image_enc.items():
            if(fr.compare_faces([value], uk)):
                return key[7:-4]                       
        return 'unknown user'


if __name__ == '__main__':
    app.run(debug=True)
