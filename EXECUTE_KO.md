# How to Execute VMeta

<br/>

> 본 문서는 local 환경에서의 VMeta 실행 방법에 대해 기술합니다. <br/>
> <b>Windows10</b>를 기준으로 작성되었습니다.<br/><br/>
> Last Edit : 2022.10.06

<br/>
<br/>


## 1. Run UploadApi

UploadApi는 메타데이터를 추출하기 위한 API 입니다.
local에서 실행할 경우 port번호를 8000번으로 바꿔 실행합니다.
```
(venv) E:\Workspace\VideoMetaSystem\FLASK\hstack > set FLASK_APP=uploadApi
(venv) E:\Workspace\VideoMetaSystem\FLASK\hstack > set FLASK_DEBUG=1
(venv) E:\Workspace\VideoMetaSystem\FLASK\hstack > flask run --host 127.0.0.1 --port 8000
```

<br/>

만약 uploadApi를 local에서 실행하지 않을 경우, 코드 일부를 수정합니다.

```
# in FLASK/hstack/hstack/views/main_views.py
# line 56

reqUrl = 'http://${YOUR_HOST_ADDRESS}:${YOUR_PORT_NUM}/upload'
```

<br/>
<br/>
<br/>


## 2. Run hstack

hstack은 메인 페이지에 해당합니다.

```
(venv) E:\Workspace\VideoMetaSystem\FLASK\hstack > set FLASK_APP=hstack
(venv) E:\Workspace\VideoMetaSystem\FLASK\hstack > set FLASK_DEBUG=1
(venv) E:\Workspace\VideoMetaSystem\FLASK\hstack > flask run
```