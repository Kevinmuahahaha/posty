from Crypto.Cipher import AES
import os
# tool::get content
# tool::save key   to local -- post id.key
# tool::save nonce to local -- post id.nonce
# tool::output crypted text (or pass to method)

# takes binary data, id
# save nonce, key to local storage (id.suffix)
# returns encrypted text
def aes_enc( content_binary, post_id ):
    key_b = os.urandom(16)

    cipher = AES.new(key_b, AES.MODE_EAX)
    nonce = cipher.nonce #another part of the key

    crypted_text, tag = cipher.encrypt_and_digest(content_binary)

    nonce_record = open(str(post_id) + ".nonce","wb")
    nonce_record.write(nonce)
    nonce_record.close()

    key_record = open(str(post_id) + ".key","wb")
    key_record.write(key_b)
    key_record.close()

    return crypted_text
