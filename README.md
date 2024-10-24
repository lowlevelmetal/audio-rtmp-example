# audio-rtmp-example

## Preface
I used this python library https://github.com/Eittipat/pyrtmp and modified its example program

RTMP is a backwards protocol. The RTMP server ingests audio/video from a client.
In my code comments I explain how you would typically handle different kinds of RTMP packets.

## Build
For most Linux distros
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run
Server
```
python3 server.py
```

Client
```
ffmpeg -re -i your/awesome/video.mp4 -c copy -f flv rtmp://localhost:1935/live/stream
```

Now you should see data move from the client to the server in real time
