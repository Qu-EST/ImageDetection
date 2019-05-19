from Crypto.Cipher import AES
import os
import pandas as pd
from pandas import DataFrame

KEY_COUNT =43

class encryptor(object):
    def __init__(self):
        self.keys = pd.read_csv('keys_binary.csv', names=['refid', 'keys'], index_col=0, dtype={1:'str'})
        
        
    
    def bitstring_to_bytes(self, s):
        return int(s, 2).to_bytes((len(s)+7) // 8, byteorder='big')
    
    def get_random_key(self):
        '''get a random set of keys from the key pool'''
        sample_keys = self.keys.sample(KEY_COUNT)
        refid = sample_keys.index.values.tolist()
        keys = ''
        for row in sample_keys.iterrows():
            keys += row[1]
        return refid, keys[0][:128]

    def find_key(self, refid):
        pass
    
    def encrypt(self, filename):
        refid, key = self.get_random_key()
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
        return refid
    
    def decrypt(self, refid,  filename):
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
    
