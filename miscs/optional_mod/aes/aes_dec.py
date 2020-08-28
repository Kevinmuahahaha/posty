from Crypto.Cipher import AES
# tool::get post-id --> default postid_nonce stored in file
# user::get key
# tool::get content(text)



# takes encrypted data + key + nonce
# returns binary data
def aes_dec(content_binary, key_file_path, nonce_file_path):
    f_key = open(key_file_path,"rb")
    key_b = f_key.readline()
    f_key.close()

    f_nonce = open(nonce_file_path,"rb")
    nonce = f_nonce.readline()
    f_nonce.close()
    

    crypted_text=content_binary

    cipher = AES.new(key_b,AES.MODE_EAX,nonce=nonce)

    plain_text = cipher.decrypt(crypted_text)
    try:
        #cipher.verify(tag)
        return plain_text
    except ValueError:
        return "[-] Corrupted Data."
