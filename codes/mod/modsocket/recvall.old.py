# why do I keep this file?
# For your reference.
# This recvall() has not output, but it works.
#

import sys
def recvall( from_socket, expected_msg_bytes ):
    #single_chunk_size = 1024
    fragments = []
    record = 0
    while True:
        chunk = from_socket.recv(expected_msg_bytes)
        if not chunk:
            break
        fragments.append( chunk )
        tmp_arr = b''.join(fragments)
        record += len(chunk)
        if record >= expected_msg_bytes:
            break
    arr = b''.join(fragments)
    return bytes(arr)


#   bytearray impelmentation
#def recvall( from_socket, expected_msg_bytes ):
#    #returns bytes, instead of bytearray
#    arr = bytearray( expected_msg_bytes )
#    pos = 0
#    chunck_size = 1024
#    while pos < expected_msg_bytes:
#        #data = from_socket.recv(chunck_size)
#        #data_len = len(data)
#        #arr[pos:pos+data_len] = data
#        data = from_socket.recv(chunck_size)
#        arr[pos:pos+chunck_size] = data
#        pos += chunck_size
#        #pos += data_len
#        #print("Getting: " + str(data_len) + " Bytes. Total: " + str(pos) + " Need: " + str(expected_msg_bytes), flush=True)
#        print("Getting: " + str(len(data)) + " Bytes. Total: " + str(pos) + " Need: " + str(expected_msg_bytes), flush=True)
#    print("DONE")
#    return bytes(arr)



#def recvall( from_socket, expected_msg_bytes ):
#    #returns bytes, instead of bytearray
#    arr = bytearray( expected_msg_bytes )
#    pos = 0
#    chunck_size = 1024
#    while pos < expected_msg_bytes:
#        if len(arr) == expected_msg_bytes:
#            break
#        data = from_socket.recv(chunck_size)
#        data_len = len(data)
#        arr[pos:pos+data_len] = data
#        pos += data_len
#        print("Getting: " + str(data_len) + " Bytes. pos: " + str(pos) + " Need: " + str(expected_msg_bytes) + "  Total: " + str(len(arr)), flush=True)
#    return bytes(arr)
