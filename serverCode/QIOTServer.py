from flask import Flask, request
import face_recognition as fr
import glob
import encryptor
import json

app = Flask(__name__)

# constants
IMAGE_PATH ='../images/*.jpg'      # image folder
# read all the images in the image folder
files = glob.glob(IMAGE_PATH)
encp = encryptor.encryptor()
# load all the known images to a library
known_image_enc = {}
for each_file in files:
    image = fr.load_image_file(each_file)
    if(fr.face_encodings(image)):
        image_enc = fr.face_encodings(image)[0]
        known_image_enc[each_file] = image_enc

def compare(unknown_image):
    pass


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
        print(refid_dict['key'])
        startPosition =refid_dict['key']
        encp.decrypt_file(startPosition, 'unknown_server.jpeg.enc')
        uk = fr.load_image_file('decrypted_unknown_server.jpeg')
        if fr.face_encodings(uk):
            uk = fr.face_encodings(uk,num_jitters=100)[0]
            for key, value in known_image_enc.items():
                if(fr.compare_faces([value], uk, tolerance=0.5)):
                    name = key.split('/')
                    #to check if we have keys is of structure like: ../images/SomeName.jpg
                    if len(name)==3:
                        fileName = name[2]
                        return fileName
        return 'unknown user'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)

