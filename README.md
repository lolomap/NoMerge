
# Install

## Client

1. For Windows you can download binaries from Release page or build it yourself.

2. Edit `.config` to set tracking path, files filter and server address. `TrackFiles` field uses python RegEx for files filtering.

3. Launch `clent.exe` to start tracking. You can add it to autostart.

### Build Client from sources

1. Install dependencies
2. Run `python setup.py build`

##  Server

Just place `server.py` script on your server and run it. Default host is  `localhost`, default API port is `8085`, default GUI port is `8080`.

You can provide needed host and API port in arguments.

### Example of configuring daemon and nginx for server script.

Daemon service for /etc/systemd/system/:
```
[Unit]
Description=NoMerge Server

[Service]
ExecStart=/usr/bin/python3 /opt/nomerge/server.py
Restart=always
WorkingDirectory=/opt/nomerge
User=root
Group=root
UserStopDelaySec=infinity
KillUserProcesses=no

[Install]
WantedBy=multi-user.target 

```

Nginx config for /etc/nginx/sites-available:
```
server {
    listen PUBLIC_API_PORT;
    location / {
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_set_header X-NginX-Proxy true;
        proxy_pass http://127.0.0.1:LOCAL_API_PORT;

	      proxy_redirect off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
server {
    listen PUBLIC_API_PORT;
    location / {
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_set_header X-NginX-Proxy true;
        proxy_pass http://127.0.0.1:LOCAL_GUI_PORT;

	      proxy_redirect off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```
