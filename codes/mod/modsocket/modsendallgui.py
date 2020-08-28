# why does this module exist?
# 'cus GUI can't do print("\b\b\b\b")
# so instead I replace it with " -- "
# LOUSY, but whatcha gonna do about it huh?
# bet you guys don't even see this comment.
# What a piece of JUNK.
# 
def percent( expected, received ):
    received = received*100
    output = int(received/expected)
    return output

def modsendall( to_socket, content, expected_msg_bytes):
    record = 0
    percent_now = 0
    percent_last = 0
    single_attempt_size = 1024
    while True:
        ret = to_socket.send( content[record:record+single_attempt_size] )
        record += ret
        if record >= expected_msg_bytes:
            break
        percent_now = percent(expected_msg_bytes, record)
        if percent_now - percent_last >= 10:
            print(str(percent_now)+" -- ", end='', flush=True)
            percent_last = percent_now
    print("100%",flush=True)
    return True
