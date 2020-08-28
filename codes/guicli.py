from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
import chardet

import subprocess
import shlex
import threading

def lauf_und_zeigt( textarea, command ):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    possible_encoding = ['GB2312','utf-8']
    while True:
        output = process.stdout.readline()
        if len(output) <= 0 and process.poll() is not None:
            break
        if output:
            # Behold, a piece of shit.
            # 
            decoded_line = None
            last_few_lines = textarea.text
            for possible in possible_encoding:
                try:
                    decoded_line = output.decode(possible)
                    break # if the 1st one works, no need to try anymore
                except:
                    #current_encoding = chardet.detect(output)['encoding']
                    #possible_encoding.append(current_encoding)
                    #decoded_line = output.decode(current_encoding)
                    continue


            current_output = last_few_lines + "\n" + decoded_line

            textarea.text = current_output
    rc = process.poll()
    print(possible_encoding)
    return rc

def befehl_macher(server_ip, server_port, task, file_path, post_id, textarea_content):
    ret_str=""
    cli_path="python ./guicliecht.py "
    tmp_file_location="._tmp_sendtoserver.txt" # randomize on each call for multithreading
    using_stdio = False
    if len(file_path) <= 0:
        using_stdio = True
    if task == 'ls':
        if using_stdio:
            ret_str = cli_path + " -s " + server_ip + " -p " + server_port\
                + " -t ls " 
        else:
            ret_str = cli_path + " -s " + server_ip + " -p " + server_port\
                + " -t ls " + " -f " + file_path

    if task == 'touch':
        if using_stdio:
            tmp_file = open(tmp_file_location, "wb")
            tmp_file.write(textarea_content.encode())
            tmp_file.close()
            ret_str = cli_path + " -s " + server_ip + " -p " + server_port\
                + " -t touch " + " -f " + tmp_file_location
        else:
            ret_str = cli_path + " -s " + server_ip + " -p " + server_port\
                + " -t touch " + " -f " + file_path

    if task == 'cat':
        if using_stdio:
            ret_str = cli_path + " -s " + server_ip + " -p " + server_port\
                + " -t cat "  + " -i " + post_id
        else:
            ret_str = cli_path + " -s " + server_ip + " -p " + server_port\
                + " -t cat " + " -f " + file_path + " -i " + post_id
    return ret_str


class Holder(Widget):
    #name = ObjectProperty(None)
    server_ip = ObjectProperty(None)
    server_port = ObjectProperty(None)
    task = ObjectProperty(None)
    file_path = ObjectProperty(None)
    post_id = ObjectProperty(None)
    textarea = ObjectProperty(None)
    def preset(self, l_properties):
        self.server_ip.text = l_properties[0]
        self.server_port.text = l_properties[1]

    def go(self):
        t_text_ip =  self.server_ip.text.strip()
        t_text_port = self.server_port.text.strip()
        t_text_task = self.task.text.strip()
        t_text_file_path = self.file_path.text.strip()
        t_text_post_id = self.post_id.text.strip()
        t_text_textarea = self.textarea.text.strip()

        if not ( len(t_text_task) and len(t_text_ip) and len(t_text_port) ):
            self.textarea.text = 'Missing mandatory arg(s)'
            return
        if t_text_task not in ['ls','touch','cat']:
            self.textarea.text = 'Task not recognized. (Available: ls, touch, cat)'
            return

        command=befehl_macher( t_text_ip, t_text_port, t_text_task, t_text_file_path, t_text_post_id, t_text_textarea )
        thread_tmp = threading.Thread(target=lauf_und_zeigt, args=(self.textarea, command))
        thread_tmp.start()

def check_config():
    default_path = './.posty.conf'
    server_ip = ''
    server_port = ''
    try:
        f_tmp = open(default_path, "r")
        server_ip = f_tmp.readline()
        server_port = f_tmp.readline()
        f_tmp.close()
    except:
        pass
    return [server_ip, server_port]
def save_config( ip, port ):
    default_path = './.posty.conf'
    try:
        f_tmp = open(default_path,"w")
        f_tmp.write( ip + '\n' )
        f_tmp.write( port )
        f_tmp.close()
        return True
    except:
        return False

class PostyGui(App):
    holder = None
    def build(self):
        self.holder = Holder()
        config = check_config()
        if len(config[0]) > 1 and len(config[1]) > 1:
            self.holder.server_ip.text = config[0]
            self.holder.server_port.text = config[1]
        return self.holder
    def on_stop(self):
        last_ip = self.holder.server_ip.text.strip()
        last_port = self.holder.server_port.text.strip()
        save_config(last_ip, last_port)
        print("Terminated.", flush=True)

if __name__ == '__main__':
    PostyGui().run()
