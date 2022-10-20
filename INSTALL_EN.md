# How to Install VMeta

<br/>

> This document describes how to install VMeta in your local environment.<br/>
> It is base on <b>Windows10</b>.<br/><br/>
> Last Edit : 2022.10.20

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

Download the project file to your workspace.
This document assumes the workspace location as <b>E:\Workspace</b>.
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
	VMeta uses Python <b>v3.8.9.</b><br/>
	Installation of <b>3.8.* to 3.9.*</b> version is recommended to avoid conflicts with libraries within the project.
	<br/>
	![Python install steps](https://user-images.githubusercontent.com/73868349/194226601-3b692582-04ef-4a82-8f3f-cffe4db866b1.jpg)
<br/>	

- <b>Setup Virtual Env</b>

	<a href = "https://docs.python.org/ko/3/library/venv.html">Official Docs</a><br/>
	Set up a virtual environment for project execution.<br/>
	```
	E:\Workspace\VideoMetaSystem > python -m venv venv (venv is your virtualenv name)
	E:\Workspace\VideoMetaSystem > .\venv\Scripts\activate.bat
	(venv) E:\Workspace >
	```
	
<br/>


## 3. Install Libraries

Install the libraries uses in VMeta.

- <b>Ffmpeg</b>

	<a href = "https://www.gyan.dev/ffmpeg/builds/">Download Link</a><br/>
	Install Ffmpeg to extract the sound source from the video.<br/>
	This project uses <b>v4.4.1</b>, but is compatible with <b>4.*</b> or higher.<br/>
	![ffmpeg install](https://user-images.githubusercontent.com/73868349/194247003-7a3941c8-38d0-4025-aee1-c7f7b3df29cf.jpg)
	
	Release the compressed file on ${Workspace}\VideoMetaSytem and set up the env.<br/>
	![setup $PATH](https://user-images.githubusercontent.com/73868349/194247822-cd6ef909-eda1-4a85-beaa-1f7547397c17.jpg)
	
	tree arch under directory VideoMetaSystem must be like this.
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
	Install Tesseract to use OCR.<br/>
	Download by referring to the <b>Windows part</b> of the official document.<br/>
	![Tesseract download](https://user-images.githubusercontent.com/73868349/196878213-a9b52f42-2d37-49c5-b636-906c9ac9278b.png)

	
	After downloading the installation file, follow the installation guide to proceed with the installation.<br/>
	Please remember the path of Tesseract to proceed [Setup config.py](#5-set-up-configpy) in 5.<br/>
	
<br/>

- <b>Java</b>

	<a href = "https://www.oracle.com/java/technologies/downloads/#java11"> Download link</a><br/>
	Download Java to use JPype1.<br/>
	Installation of <b>JDK 11</b> is recommended to avoid conflicts with libraries within the project.<br/>
	![JAVA download](https://user-images.githubusercontent.com/73868349/196880251-d2c8239c-58f1-4f50-bb83-08cb5e34bcc0.png)

	
	After downloading the installation file, follow the installation guide to proceed with the installation.<br/>
	And, Set up the system env.<br/>
	![그림3](https://user-images.githubusercontent.com/73868349/196880993-09d5dc4f-3cd2-461b-89ed-e7ea24e005b4.png)

	You have to craete env JAVA_HOME if you don't have it.

<br/>

- <b>requirements.txt</b>

	Install libraries in requirements.txt
	```
	(venv) E:\Workspace\VideoMetaSystem > pip install -r requirements.txt
	```

<br/>

- <b>special requirements</b>

	For execute subprocess, certain libraries are installed in a non-virtual environment.<br/>
	```
	(venv) E:\Workspace\VideoMetaSystem > deactivate
	E:\Workspace\VideoMetaSystem > pip install -r special_requirements.txt
	```
	<br/>


	Also, some libraries are imported separately from git.<br/>
	<a href = "https://github.com/haven-jeon/PyKoSpacing">pykospacing</a> : Use for Korean preprocessing.<br/>
	<a href = "https://github.com/ParthS007/background">background</a> :Use to run uploadApi asynchronously.<br/>
	```
	(venv) E:\Workspace\VideoMetaSystem > pip install git+https://github.com/haven-jeon/PyKoSpacing.git
	(venv) E:\Workspace\VideoMetaSystem > pipenv install background
	```


<br/>
<br/>
<br/>


## 4. Set up MySQL

Set up the project DB.<br/>
Assume MySQL is installed on your computer.<br/>

- Create hstackDB <br/>
	```
	CREATE DATABASE hstackDB;
	```

- Create table for Metadata <br/>
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
	
- Create table for Monitoring <br/>
	```
	use hstackDB;

	CREATE TABLE SearchSatisfy (
		val int PRIMARY KEY,
    		cnt int
	);

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

- Insert Column for SearchSatisfy<br/>
	```
	INSERT INTO searchSatisfy (val, cnt) VALUE (1, 0);
	INSERT INTO searchSatisfy (val, cnt) VALUE (2, 0);
	INSERT INTO searchSatisfy (val, cnt) VALUE (3, 0);
	INSERT INTO searchSatisfy (val, cnt) VALUE (4, 0);
	INSERT INTO searchSatisfy (val, cnt) VALUE (5, 0);
	```

<br/>
<br/>
<br/>



## 5. Set up config.py

Modify the configuration file using your DB and API Key.


- FLASK\hstack\hstack
	```
	# in __init__.py
	# line 15
	
	app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:${YOUR_DB_PASSWORD}@localhost/hstackdb"
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
	'password' : ${YOUR_DB_PASSWORD},
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
	
	app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:${YOUR_DB_PASSWORD}@localhost/hstackdb"
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
	'password' : ${YOUR DB PASSWORD},
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
