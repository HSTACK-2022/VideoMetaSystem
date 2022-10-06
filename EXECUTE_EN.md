# How to Execute VMeta

<br/>

> This document describes how to run VMeta in your local environment. <br/>
> It is base on <b>Windows10</b>.<br/><br/>
> Last Edit : 2022.10.06

<br/>
<br/>


## 1. Run UploadApi
UploadApi is an API for extracting metadata.
If you run VMeta on local, change the port number to 8000 to avoid conflict.

```
(venv) E:\Workspace\VideoMetaSystem\FLASK\hstack > set FLASK_APP=uploadApi
(venv) E:\Workspace\VideoMetaSystem\FLASK\hstack > set FLASK_DEBUG=1
(venv) E:\Workspace\VideoMetaSystem\FLASK\hstack > flask run --host 127.0.0.1 --port 8000
```

<br/>

If you run uploadApi on different env (not local), modify some code.

```
# in FLASK/hstack/hstack/views/main_views.py
# line 56

reqUrl = 'http://${YOUR_HOST_ADDRESS}:${YOUR_PORT_NUM}/upload'
```

<br/>
<br/>
<br/>


## 2. Run hstack

App hstack contains main pages of VMeta.

```
(venv) E:\Workspace\VideoMetaSystem\FLASK\hstack > set FLASK_APP=hstack
(venv) E:\Workspace\VideoMetaSystem\FLASK\hstack > set FLASK_DEBUG=1
(venv) E:\Workspace\VideoMetaSystem\FLASK\hstack > flask run
```