from mod.modsocket.recvall import recvall
from mod.modlog import debug, bad
from mod.data_operation import ls, touch, cat
import uuid
import sys
import socket
POST_ID_MAX_LENGTH=69 #bytes, encoded UUID string

def interaction_routine( client_sock ):
    task = client_sock.recv(128).decode()
    # 1st : get
    debug("Client Requesting Task: " + str(task))

    if task == "TOUCH": # returns string (status)
        client_sock.sendall("OK".encode()) # check if task available, when not, return NO
        length = int(client_sock.recv(128))
    # 3rd : get length & offer ID
        debug("Client Requesting Data length(bytes): " + str(length))
        offering_post_id = str(uuid.uuid1())
        #optional access control, when unavailable don't send uuid
        client_sock.sendall( offering_post_id.encode() ) 
    # 4th : get
        get_data = recvall( client_sock, length )
    # 5th : check
        get_data_length = len(get_data)
        debug("Got Length(bytes): " + str(get_data_length))

        if get_data_length == length:
            client_sock.sendall("SUCCESS".encode())
            touch_status = touch( offering_post_id, get_data )
            debug("Touch returns: " + str(touch_status))
        else:
            bad("Post Failed.")
            client_sock.sendall("FAIL".encode())
    # 6th : send
    
    if task == "CAT": #returns bytes
        client_sock.sendall("OK".encode()) # check if task available, when not, return NO
        target_post_id = str(client_sock.recv( POST_ID_MAX_LENGTH ).decode())
        #get post id
        debug("Client Requesting PostID: " + target_post_id)
        content = cat( target_post_id ) # a dict
        if content == None:
            client_sock.sendall(str(0).encode())
            debug("Client Asked for non-existing post.")

        else:
            content = content["content"] # bytes data
            content_length = len( content )
            client_sock.sendall(str(content_length).encode())

            client_status = str(client_sock.recv(128).decode())
            if client_status == "OK":
                debug("Client Ready. Sending content.")

            client_sock.sendall( content )


    if task == "LS": #returns list
        ls_return = ls()
        content = []
        for item in ls_return:
            content.append(item["postid"])

        content = ':'.join(content)
        content = content.encode()
        client_sock.sendall(str(len(content)).encode()) # check if task available, when not, return NO
        # 2nd send
        client_sock.recv(128) # client ready to recv
        client_sock.send( content )

    # disable rm command. post auto-removed in 24h
    # closing client socket
    client_sock.shutdown(socket.SHUT_RDWR)
    client_sock.close()
    debug("Client Socket Closed.")
