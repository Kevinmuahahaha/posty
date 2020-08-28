from mod.mod_client_data_operation import ls, touch, cat
# testing units: ls touch cat
import random
import string
random.seed()

test_server = "w34dfgh.xyz"
test_port = 23869
count = 50

# -------------Testing ls()----------------
print("Testing LS")
result = ls( test_server, test_port )
# Test Result:
#   added
#     soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#   in 
#      mod/mod_client_data_operation.py
#   for quicker connect next time.
#
#   added retry (default 3 times) when there's a bad connection.
count = 50 # run ls 50 times
while count > 0:
    for line in result: # printing returned list from ls
        print(line, flush=True)
    print("[Test] End of ",count, " --------------\n")
    count -= 1





# -------------Testing cat()----------------
# Note: post_id must be encoded to bytes
#   for uniformed arguments
print("Testing CAT")
# Test Result:
#   *added SO_REUSEADDR for a quicker reconnection.
#   *added settimeout
#   *added corresponding try-catch phrase
#     to handle connection failure.
#   *using non-blocking(timeout) for cat, 
#     in case of bad connection to the oversea server.
#   *handled output when there's a bad connection
using_ls_result = ls( test_server, test_port )
good=0
bad=0
count = 20 # cat 20 times at most, for a cleaner output
for line in using_ls_result:
    if count < 1:
        break
    count -= 1
    # randomly decide to cat or not.
    if random.choice([True, False]):
        print("[Test] Trying to cat: ",line, flush=True)
        data = cat( line.encode(), test_server, test_port )
        if data == None:
            print("[Test] Fail to retrieve data.", flush=True)
            bad += 1
        else:
            print("[Test] Successfully retrieved data.", flush=True)
            good += 1
        print("--------------------------\n")
print("Success: ",good, "  Fail: ", bad)




# -------------Testing touch()----------------

# bug found: unresponsive connections might occur
# resolved: 
#    added timeout for touch, and corresponding try-catch phrases
#    added new return codes and error messages

print("Testing TOUCH")
def randomString(stringLength=8):
# found on https://pynative.com/python-generate-random-string/
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
count = 50 # run touch 50 times
while count > 0:
    count -= 1
    msg_length = random.randrange(1,1024)
    msg_filled = randomString(stringLength=msg_length)
    print("[Test] Sending ", msg_length, " random chars.")
    status = touch(msg_filled.encode(), test_server, test_port )
    print("--------------------------\n")

