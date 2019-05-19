import requests
import face_recognition as fr
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


with open('unknown.jpg', 'rb') as uki:
    
    img = bytearray(uki.read())


# with open('unk_cpy.jpg', 'wb+') as uki:
#     uki.write(img)


#print(img)
    
# unknown_image = fr.load_image_file('unknown.jpg')

# #plt.imshow(img)

payload = {'refid':'jeeva', 'image':img}



result = requests.post('http://127.0.0.1:5000/compare_image', data=img, headers={'Content-Type': 'application/octet-stream'})

print(result)

result = requests.get('http://127.0.0.1:5000/compare_image')

print(result.text)
