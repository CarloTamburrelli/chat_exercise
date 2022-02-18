

## How it works?

Before starting the server, set the IP address and port, otherwise the local address **127.0.0.1** with port **64446** will be used
The project contains both the client part of the app and the server part, the files are respectively:
- client.cs 
- server.py


# Install and run Server

Type the follow:
```sh
python3 -m venv venv
```

```sh
source venv/bin/activate
```

```sh
pip install -r requirements.txt
```
And run:

```sh
python server.py
```

# Run Client
Client executable in both windows and linux, for a quick installation on linux, install the **mono-complete** program
and then run:
```sh
mono client.exe
```