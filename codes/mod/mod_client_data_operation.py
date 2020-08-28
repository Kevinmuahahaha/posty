from mod.modsocket.recvall import recvall
from mod.modsocket.modsendall import modsendall
from mod.modlog import debug, bad, good
import socket
import sys

def ls( HOST_IP, HOST_PORT ): # takes nothing, return list of strings
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.settimeout(3)
        soc.connect((HOST_IP,HOST_PORT))
    except :
        debug("socket not being (re)connected.")
    force_retry = 3

    while force_retry > 0:
        try:
            debug("Sending Task")
            soc.sendall("LS".encode())
            status = soc.recv(128)

            if status.decode() != "NO":
                # task available
                debug("Size of list(bytes): " + status.decode())
                soc.sendall("Ready".encode())
                content_list = recvall(soc, int(status.decode()))

            content_list = content_list.decode()
            content_list = content_list.split(':')
            ret_list = []
            for item in content_list:
                ret_list.append(item)
            soc.close()
            return ret_list
        except:
            print("Bad connection. Retr(ies) left: ", force_retry)
            soc.close()
            # renew socket
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            soc.settimeout(3)
            soc.connect((HOST_IP,HOST_PORT))
            force_retry -= 1

def touch( content, HOST_IP, HOST_PORT ): #takes binary content, returns post-id/Fail/None (string/None)
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.settimeout(9)
        soc.connect((HOST_IP,HOST_PORT))
    except :
        debug("socket not being (re)connected.")

    try:
        soc.sendall("TOUCH".encode())
        status = str(soc.recv(128).decode()) 
        # do remember to check return status before posting.
        # when server doesn't say "OK", then it refuses to receive.
    except:
        print("Server ignored your request. Could be a bad connection.")
        return "SRV NO RESP"

    content_length = len( content )
    if status == "OK":
        good("Posting Service Available")
        soc.sendall(str(content_length).encode())
        postid = soc.recv(128).decode()
        debug("Posting to ID: "+str(postid))
        send_status = False
        try:
            send_status = modsendall(soc, content, content_length)
            #soc.sendall(content)
        except:
            debug("Send process done.")
        if send_status == False:
            bad("Bad connection. Abort.")
            soc.close()
            return None
        try:
            status = soc.recv(128)
            debug("Post status: " + str(status))
        except:
            print("Can\'t receive server confirmation.")
            print("Actual post status unknown.")
        finally:
            soc.close() # closing socket
            return "SERV NO RESP"
        if str(status.decode()) == "SUCCESS":
            good("Post Success.")
            return str(postid)
        else:
            bad("Posted. But server messed it up.")
            return str(status)
    else:
        bad("Post Failed: Server recv failure.")
        soc.close() # closing socket
        return None

def cat( post_id, HOST_IP, HOST_PORT ): #takes binary id, returns binary content
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.settimeout(9)
        soc.connect((HOST_IP,HOST_PORT))
    except :
        debug("socket not being (re)connected.")
    soc.sendall("CAT".encode())
    try:
        status = str(soc.recv(128).decode())
    except:
        bad("Cat failed. Bad connection.")
        return None
    if status == "OK":
        debug("Requesting data from ID: " + str(post_id.decode()))
        soc.sendall( post_id )
        content_length = int(str(soc.recv(128).decode()))
        if content_length == 0:
            debug("Empty content.")
            return None
        debug("Ready to receive bytes: " + str( content_length ))
        soc.sendall( "OK".encode() )
        content = recvall( soc, content_length )
        if content == None:
            bad("Cat failed. Bad connection.")
            soc.close()
            return None
        else:
            get_content_length = len(content)
            debug("Data length get: " + str(get_content_length))
            soc.close()
            return content
    else:
        bad("Cat Failed: Server rejected.")
        soc.close()
        return None
