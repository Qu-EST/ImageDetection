import encryptor

e = encryptor.encryptor()

refid, key = e.encrypt_file('unknown.jpg')

key = e.decrypt_file(refid, 'unknown.jpg.enc')

enc_data = e.encrypt_data( 'how', key)

data = e.decrypt_data(enc_data, key)

print(data)
