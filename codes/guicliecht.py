from mod.modlog import debug, bad
from mod.mod_client_data_operation_gui import ls, touch, cat
import argparse
import sys
    
parser = argparse.ArgumentParser()
parser.add_argument('--server','-s', help='Server\'s IP.')
parser.add_argument('--port','-p', help='Server\'s Port.')
parser.add_argument('--task','-t', help='Set Task. [cat | touch | ls]')
parser.add_argument('--file-path','-f', help='Specify output/input file')
parser.add_argument('--post-id','-i', help='(Used with cat command)Specify Post-ID')
args = parser.parse_args()
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    print("\nExampe: client_cli -s 127.0.0.1 -p 23000 -t ls\n")
    sys.exit(1)

get = vars(args)
ARG_POST_ID=get['post_id']
ARG_TASK=get['task']
ARG_SERVER_IP=get['server']
ARG_SERVER_PORT=get['port']
try:
    ARG_SERVER_PORT=int(ARG_SERVER_PORT)
except:
    bad("Port must be an integer.")
    sys.exit(1)
ARG_FILE_PATH=get['file_path']
USING_STDIO=False

if not ARG_TASK or not ARG_SERVER_IP or not ARG_SERVER_PORT  :
    parser.error('Mandatory args: task, server ip, server port.')
    sys.exit(1)
elif ARG_TASK not in ['ls','touch','cat']:
    parser.error('Task not understood. Abort.')
    sys.exit(1)

if not ARG_FILE_PATH:
    USING_STDIO=True # when file path isn't set, use stdio as input/output
else:
    USING_STDIO=False

if ARG_TASK == 'cat' and not ARG_POST_ID:
    bad("Cat command requires an ID (post-id)")
    sys.exit(1)

if ARG_TASK == 'touch':
    debug("Sending contents to %s:%s"%(ARG_SERVER_IP,ARG_SERVER_PORT))
    content = None
    if not USING_STDIO:
        try:
            f_tmp = open(ARG_FILE_PATH,"rb")
            content = f_tmp.read()
            f_tmp.close()
        except:
            bad("Can\'t open input. Have you try double-back-slash?")
    else:
        content = input(">>>")
        content = content.encode()
    touch_result = touch(content, ARG_SERVER_IP, ARG_SERVER_PORT)
    debug(touch_result)

if ARG_TASK == 'cat':
    debug("Retrieving contents from %s:%s"%(ARG_SERVER_IP,ARG_SERVER_PORT))
    cat_result = cat(ARG_POST_ID.encode(), ARG_SERVER_IP, ARG_SERVER_PORT)
    if not USING_STDIO:
        debug("Dumping cat result to file: %s"%(ARG_FILE_PATH))
        try:
            f_tmp = open(ARG_FILE_PATH, "wb")
            f_tmp.write(cat_result)
            f_tmp.close()
        except:
            bad("Can\'t open output. Check your file name.");
    else:
        debug("Dumping cat result to stdout:")
        try:
            print(cat_result.decode(), end='', flush=True)
        except:
            bad("Data not printable.")

if ARG_TASK == 'ls':
    debug("Checking posts on %s:%s"%(ARG_SERVER_IP,ARG_SERVER_PORT))
    post_list = ls(ARG_SERVER_IP, ARG_SERVER_PORT)
    for item in post_list:
        print(item)
