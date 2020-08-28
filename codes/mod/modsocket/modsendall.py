def percent_str( expected, received ):
    received = received*100
    output = int(received/expected)
    return str(output) + "%"

def modsendall( to_socket, content, expected_msg_bytes):
    record = 0
    single_attempt_size = 1024
    while True:
        try:
            ret = to_socket.send( content[record:record+single_attempt_size] )
        except:
            print("Send failure. Bad connection.")
            return False
        record += ret
        if record >= expected_msg_bytes:
            break
        print("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b", end='', flush=True)
        print(percent_str(expected_msg_bytes,record)+" -- ", end='', flush=True)
    print("100%",flush=True)
    return True
