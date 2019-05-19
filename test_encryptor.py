import encryptor

e = encryptor.encryptor()

refid = e.encrypt('unknown.jpg')

e.decrypt(refid, 'unknown.jpg.enc')
