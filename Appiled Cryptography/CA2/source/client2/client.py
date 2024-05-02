import base64, time, datetime, ftplib, io, random, csv
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Signature import pkcs1_15 
from Crypto.Hash import SHA256
import OpenSSL
from six import u, b, binary_type, PY3
from base64 import b64decode
import socket
import os
from time import sleep

# These variables are to support the mock camera
my_pict = "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"

# System  variable of main program



def connect_server_send( file_name: str , file_data: bytes , username, password, server_name) -> bool:
    """This function send file_data using FTP and save it as file_name in the remote server. It will simulate intermittent transfer. 
    Args:
        file_name (str): file_name of file save in server as a String
        file_data (bytes): content of file as byte array
    Returns:
        bool: True if send, False otherwise
    """
    try:
        if random.randrange(1,10) > 8: raise Exception("Generated Random Network Error")   # create random failed transfer   
        ftp = ftplib.FTP()  # use init will use port 21 , hence use connect()
        ftp.connect( server_name , 2121) # use high port 2121 instead of 21
        ftp.login(user=username, passwd = password)
        ftp.storbinary('STOR ' + file_name, io.BytesIO( file_data ) )
        ftp.quit()
        return True
    except Exception as e:
        print(e, "while sending", file_name )
        return False


def get_picture() -> bytes:
    """This function simulate a motion activated camera unit.  It will return 0 byte if no motion is detected.
    Returns:
        bytes: a byte array of a photo or 0 byte no motion detected
    """    

    time.sleep(1) # simulate slow processor
    if random.randrange(1,10) > 8:  # simulate no motion detected
        return b''
    else:
        return b64decode(my_pict)

def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    #print(len(ciphertext), len(aesCipher.nonce), len(authTag))
    return (ciphertext, aesCipher.nonce, authTag)


def encrypt_image(img) -> bytes:
  digest=SHA256.new(img)

  key = open("private.pem", "rb").read()
  privkey = RSA.import_key(key)
  signature = pkcs1_15.new(privkey).sign(digest) #256

  secretKey = os.urandom(32)  # 256-bit random encryption key
  encryptedMsg = encrypt_AES_GCM(img, secretKey) # Enc Image + IV(16) + Auth Tag(16)

  key = open("server-cert.crt", "rb").read()
  pubkey = RSA.import_key(key)
  cipher = Cipher_PKCS1_v1_5.new(pubkey)

  enckey = cipher.encrypt(secretKey) # RSA encrypted session key(128)
  return (b''.join(encryptedMsg) + enckey + signature)

# server_name,camera_id,username,password
camera_id = str(input("Camera ID: ")) #"2"
server_name = str(input("Server IP: ")) #"127.0.0.1"
username = str(input("Username: ")) #"camera2"
password = str(input("Password: ")) #"32$-k3+chL:#rHF?"

if not os.path.isfile('server-cert.crt'):
  ClientSocket = socket.socket()
  host = '127.0.0.1'
  port = 7777
  try:
    ClientSocket.connect((host, port))
  except socket.error as e:
    print(str(e))

  while 1:
    try:
      ClientSocket.sendall("[REQ-CERT]".encode())
      PublicKey = ClientSocket.recv(10240)
      CAPublicKey = open("ca-cert.crt", "rb").read()
      ca_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, CAPublicKey)
      untrusted_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, PublicKey)
      store = OpenSSL.crypto.X509Store()
      store.add_cert(ca_cert)
      store_ctx = OpenSSL.crypto.X509StoreContext(store, untrusted_cert)
      store_ctx.verify_certificate()
      open('server-cert.crt','wb').write(PublicKey)
      # ClientSocket.close()
      break
    except OpenSSL.crypto.X509StoreContextError:
        sleep(60)


  new_key = RSA.generate(2048, e=65537)
  open('private.pem','wb').write(new_key.exportKey("PEM"))
  stor_req = b"[STOR-CERT] "+ bytes(f"{username} ", 'utf-8') + new_key.publickey().exportKey("PEM")
  ClientSocket.sendall(stor_req)
  ClientSocket.close()

while True: # Main function
    try:  
        my_image = get_picture()  # get picture
        if len(my_image) == 0:
            time.sleep(10) # sleep for 10 sec if there is no image
            print("Random no motion detected")
        else:
            enc_image = encrypt_image(my_image)
            f_name = str(camera_id) + "_" +  datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S.jpg" )
            if connect_server_send(f_name , enc_image, username, password, server_name): print(f_name , " sent" )
    except KeyboardInterrupt:  exit()  # gracefully exit if control-C detected