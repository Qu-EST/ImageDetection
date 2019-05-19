import encryptor

e = encryptor.encryptor()

refid, key = e.encrypt_file('Lac.jpg')

key = e.decrypt_file(refid, 'Lac.jpg.enc')

enc_data = e.encrypt_data( 'how', key)

data = e.decrypt_data(enc_data, key)

print(data)
