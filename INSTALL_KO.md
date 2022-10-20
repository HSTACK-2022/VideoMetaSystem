
# How to Install VMeta

<br/>

> 본 문서는 local 환경에서의 VMeta 설치 방법에 대해 기술합니다. <br/>
> <b>Windows10</b>를 기준으로 작성되었습니다.<br/><br/>
> Last Edit : 2022.10.06

<br/>

**Docs Map** <br/>
1. [Get Project File](#1-get-project-file)
2. [Install Python](#2-install-python)
3. [Install Libraries](#3-install-libraries)
4. [Set up MySQL](#4-set-up-mysql)
5. [Set up config.py](#5-set-up-configpy)
<br/>
<br/>


## 1. Get Project File

자신의 Workspace에 프로젝트 파일을 다운로드합니다.
이 문서에서는 Workspace의 위치를 <b>E:\Workspace</b>로 가정합니다.
```
C:\ > cd E:/Workspace
E:\Workspace > git clone https://github.com/HSTACK-2022/VideoMetaSystem.git
E:\Workspace > cd VideoMetaSystem
```

<br/>
<br/>
<br/>


## 2. Install Python

- <b>Install</b>

	<a href = "https://www.python.org/downloads/release/python-389/">Download Link</a><br/>
	VMeta는 <b>Python 3.8.9</b> 버전을 사용합니다.<br/>
	프로젝트 내 라이브러리와의 충돌을 방지하기 위해 <b>3.8.* ~ 3.9.*</b> 버전의 설치를 권장합니다.
	<br/>
	![Python install steps](https://user-images.githubusercontent.com/73868349/194226601-3b692582-04ef-4a82-8f3f-cffe4db866b1.jpg)
<br/>	

- <b>Setup Virtual Env</b>

	<a href = "https://docs.python.org/ko/3/library/venv.html">Official Docs</a><br/>
	프로젝트 실행을 위한 가상환경을 설정합니다.<br/>
	```
	E:\Workspace\VideoMetaSystem > python -m venv venv (venv is your virtualenv name)
	E:\Workspace\VideoMetaSystem > .\venv\Scripts\activate.bat
	(venv) E:\Workspace >
	```
	
<br/>


## 3. Install Libraries

VMeta에 사용되는 라이브러리들을 설치합니다.

- <b>Ffmpeg</b>

	<a href = "https://www.gyan.dev/ffmpeg/builds/">Download Link</a><br/>
	영상에서의 음원 추출을 위해 Ffmpeg을 설치합니다.<br/>
	본 프로젝트는 <b>4.4.1</b> 버전을 사용하였으나, <b>3.*</b> 이상의 버전이면 호환 가능합니다.<br/>
	![ffmpeg install](https://user-images.githubusercontent.com/73868349/194247003-7a3941c8-38d0-4025-aee1-c7f7b3df29cf.jpg)
	
	${Workspace}\VideoMetaSytem 에 압축 파일을 해제하고, 환경 변수를 등록합니다.<br/>
	![setup $PATH](https://user-images.githubusercontent.com/73868349/194247822-cd6ef909-eda1-4a85-beaa-1f7547397c17.jpg)
	
	VideoMetaSystem 하위의 구조가 아래와 같아야 합니다.
	```
	(venv) E:\Workspace\VideoMetaSystem > dir
	E 드라이브의 볼륨: 
	볼륨 일련 번호: 

	E:\Workspace\VideoMetaSystem 디렉터리

	2022-10-06  오후 03:24    <DIR>          .
	2022-10-06  오후 03:24    <DIR>          ..
	2022-10-06  오후 02:42             6,076 .gitignore
	2022-10-06  오후 02:42    <DIR>          DJANGO
	2022-04-15  오전 05:13    <DIR>          ffmpeg-5.0.1-full_build
	2022-10-06  오후 02:43    <DIR>          FLASK
	2022-10-06  오후 02:43            35,823 LICENSE
	2022-10-06  오후 02:43            14,735 README.md
	2022-10-06  오후 02:43    <DIR>          report
	2022-10-06  오후 03:11    <DIR>          venv
	               3개 파일              56,634 바이트
	               7개 디렉터리  12,588,204,032 바이트 남음
	```

<br/>

- <b>Tesseract</b>

	<a href = "https://tesseract-ocr.github.io/tessdoc/Installation.html">Official Docs / Download link</a><br/>
	OCR을 사용하기 위해 Tesseract를 설치합니다.<br/>
	공식 문서의 Windows 부분을 참고하여 다운로드 합니다.<br/>
	![Tesseract download](https://user-images.githubusercontent.com/73868349/196878213-a9b52f42-2d37-49c5-b636-906c9ac9278b.png)

	
	install 파일을 다운로드 한 후, 설치 가이드에 따라 설치를 진행합니다. <br/>
	5의 [Set up config.py](#5-set-up-configpy)를 진행하기 위해, Tesseract의 경로를 기억해주시기 바랍니다.<br/>

<br/>

- <b>Java</b>

	<a href = "https://www.oracle.com/java/technologies/downloads/#java11"> Download link</a><br/>
	JPype1의 정상적인 사용을 위해 Java를 다운로드합니다.<br/>
	프로젝트 내 라이브러리와의 충돌을 방지하기 위해 <b>JDK 11</b>의 설치를 권장합니다.<br/>
	![JAVA download](https://user-images.githubusercontent.com/73868349/196880251-d2c8239c-58f1-4f50-bb83-08cb5e34bcc0.png)

	
	install 파일을 다운로드 한 후, 설치 가이드에 따라 설치를 진행합니다. <br/>
	이후 시스템 환경 변수를 설정합니다.<br/>
	![그림3](https://user-images.githubusercontent.com/73868349/196880993-09d5dc4f-3cd2-461b-89ed-e7ea24e005b4.png)

	만약 JAVA_HOME 환경변수가 없다면 새로 생성합니다.

<br/>

- <b>requirements.txt</b>

	requirements.txt에 있는 라이브러리들을 설치합니다.
	```
	(venv) E:\Workspace\VideoMetaSystem > pip install -r requirements.txt
	```

<br/>

- <b>special requirements</b>

	subprocess에서의 정상 동작을 위해 특정 라이브러리들은 가상환경이 아닌 곳에도 설치합니다.<br/>
	```
	(venv) E:\Workspace\VideoMetaSystem > deactivate
	E:\Workspace\VideoMetaSystem > pip install -r special_reqirements.txt
	```
	<br/>


	또한, 일부 라이브러리는 git에서 별도로 가져와 사용합니다.<br/>
	<a href = "https://github.com/haven-jeon/PyKoSpacing">pykospacing</a> : 한국어 전처리에 이용합니다.<br/>
	<a href = "https://github.com/ParthS007/background">background</a> : uploadApi를 비동기적으로 실행하기 위해 사용합니다.<br/>
	```
	(venv) E:\Workspace\VideoMetaSystem > pip install git+https://github.com/haven-jeon/PyKoSpacing.git
	(venv) E:\Workspace\VideoMetaSystem > pipenv install background
	```


<br/>
<br/>
<br/>


## 4. Set up MySQL

프로젝트 DB를 설정합니다.<br/>
컴퓨터에 MySQL이 설치되어 있다고 가정합니다.<br/>

- hstackDB 생성 <br/>
	```
	CREATE DATABASE hstackDB;
	```

- 메타데이터 테이블 생성 <br/>
	```
	use hstackDB;
	
	CREATE TABLE videopath (
		id int PRIMARY KEY AUTO_INCREMENT,
		title VARCHAR(50),
		videoAddr VARCHAR(200),
		audioAddr VARCHAR(200),
		textAddr VARCHAR(200),
		imageAddr VARCHAR(200),
		extracted int,
		password VARCHAR(10)
	);

	CREATE TABLE metadata (
		id int PRIMARY KEY,
		title VARCHAR(50),
		presenter VARCHAR(50),
		category VARCHAR(20),
		narrative VARCHAR(30),
		presentation VARCHAR(10),
		videoLength VARCHAR(10),
		videoFrame VARCHAR(10),
		videoType VARCHAR(5),
		videoSize VARCHAR(10),
		uploadDate DATE,
		voiceManRate FLOAT,
		voiceWomanRate FLOAT,
		category_percent VARCHAR(30),
		FOREIGN KEY (id) REFERENCES videopath(id)
	);

	CREATE TABLE keywords (
		id int,
		keyword VARCHAR(10),
		expose int,
		sysdef int,
		percent float,
		PRIMARY KEY (id, keyword),
		FOREIGN KEY (id) REFERENCES videopath(id)
	);

	CREATE TABLE timestamp (
		id int,
		time VARCHAR(10),
		subtitle VARCHAR(100),
		expose int,
		sysdef int,
		PRIMARY KEY (id, time),
		FOREIGN KEY (id) REFERENCES videopath(id)
	);
	```
	
- 모니터링 테이블 생성 <br/>
	```
	use hstackDB;

	CREATE TABLE SearchSatisfy (
		val int PRIMARY KEY,
    		cnt int
	);

	CREATE TABLE upload_time (
		id int PRIMARY KEY,
		time float,
		size float,
		FOREIGN KEY (id) REFERENCES videopath(id)
	);

	CREATE TABLE total_search (
		tKeyword VARCHAR(50) PRIMARY KEY,
		cnt int
	);

	CREATE TABLE title_search (
		tiKeyword VARCHAR(50) PRIMARY KEY,
		cnt int
	);

	CREATE TABLE presenter_search (
		pKeyword VARCHAR(50) PRIMARY KEY,
		cnt int
	);

	CREATE TABLE keyword_search (
		kKeyword VARCHAR(50) PRIMARY KEY,
		cnt int
	);
	```

<br/>
<br/>
<br/>



## 5. Set up config.py

자신의 DB와 API Key를 이용해 설정파일을 수정합니다.


- FLASK\hstack\hstack
	```
	# in __init__.py
	# line 15
	
	app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:${YOUR_DB_PASWORD}@localhost/hstackdb"
	```
	```
	# in config.py
	
	import  os
	import  platform
	
	from  flask_sqlalchemy  import  SQLAlchemy
	
	OS = platform.system()
	BASE_DIR = os.path.dirname(__file__)
	UPLOAD_FILE_DIR = os.path.join('.', 'media', 'Uploaded')
	UPLOAD_LOG_DIR = os.path.join('.', 'logs')

	STT_API_KEY = {
		YOUR_ETRI_API_KEY
		(We need at least 5 Keys.)
	}
	
	db = {
	'user' : 'root',
	'password' : ${YOUR_DB_PASWORD},
	'host' : 'localhost',
	'port' : 3306,
	'database' : 'hstackDB'
	}
	
	DB = SQLAlchemy()

	DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
	```
	
<br/>

- FLASK\hstack\uploadApi
	```
	# in __init__.py
	# line 17
	
	app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:${YOUR_DB_PASWORD}@localhost/hstackdb"
	```
	```
	# in config.py
	
	import  os
	import  platform
	
	from  flask_sqlalchemy  import  SQLAlchemy
	
	OS = platform.system()
	BASE_DIR = os.path.dirname(__file__)
	UPLOAD_FILE_DIR = os.path.join('.', 'media', 'Uploaded')
	UPLOAD_LOG_DIR = os.path.join('.', 'logs')

	STT_API_KEY = {
		YOUR_ETRI_API_KEY
		(We need at least 5.)
	}
	
	db = {
	'user' : 'root',
	'password' : ${YOUR DB PASWORD},
	'host' : 'localhost',
	'port' : 3306,
	'database' : 'hstackDB'
	}
	
	DB = SQLAlchemy()

	DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
	```
	```
	# in sceneText.py
	# line 47
	
	pytesseract.pytesseract.tesseract_cmd = ${YOUR_TESSERACT_LOCATION}
	```