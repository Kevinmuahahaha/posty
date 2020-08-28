# posty
Share and fetch messages( or any data ) within CLI across the web.

# Running

for cli client use:
  ```
  client_cli.py -s <server.location> -p 23869 -t [ls|touch|cat]
  ```
   
for GUI client use:
  ```
  guicliecht.py
  
  Note that there're extra libs required: kivy, Pillow, pysdl2 (via pip)
  ```
    
*Running in VBox fix:
  ```
  pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
  ```

# Setup
1. setup virtualenv
  ```
	pip install virtualenv

	$ virtualenv /path/ 
		or
	$ python3 -m venv /path/

	-Linux/Mac: 
		$ source mypython/bin/activate
	-Windows: 
		> venv\Scripts\activate

	# to disable virtual env, use cmd: deactivate
```
2. install libs
  ```
	pip install -r requirements.txt
  ```
	

# Configuring Server-side (Tested on Ubuntu16.04)

1. Configuring MongoDB
```
	# apt update
	# apt install python3 python3-pip mongodb

	Don't want to use MongoDB?
	modify:
		mod/data_operation.py 
	for a different IO implementation.
	
	There's little need of configuring MongoDB,
	just make sure it's running:
	# systemctl status mongodb

	Wanna configure your MongoDB?
	make sure to change:
		mod/data_operation.py
		(line:11)
	so that there could be connection to the DB.
```
2. Edit server.py
```
	line:6	Server ip
	line:7	Server port
```
3. Los geht! (Running the service)
```
	$ python3 ./server.py
	In case the system kills your instance,
	run:
	$ nohup python3 ./server.py 2>&1 >> output.log &
	instead.
```

