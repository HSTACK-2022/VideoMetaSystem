



# How to Install "VMeta"

Last Edit : 2022.10.06

<br/>

> 본 문서는 local 환경에서의VMeta 설치 방법에 대해 기술합니다. <br/>
> <b>Windows10</b>를 기준으로 작성되었습니다.

<br/>
<br/>

## 0. Get Project File

자신의 Workspace에 프로젝트 파일을 다운로드합니다.
이 문서에서는 Workspace의 위치를 <b>E:\Workspace</b>로 가정합니다.
```
C:\ > cd E:/Workspace
E:\Workspace > git clone https://github.com/HSTACK-2022/VideoMetaSystem.git
```

<br/>
<br/>
<br/>


## 1. Install Python

- <b>Install</b>

	<a href = "https://www.python.org/downloads/release/python-389/">Download Link</a><br/>
	VMeta는 <b>Python 3.8.9</b> 버전을 사용합니다.<br/>
	프로젝트 내 라이브러리와의 충돌을 방지하기 위해 <b>3.8.* ~ 3.9.*</b> 버전의 설치를 권장합니다.
	
<br/>	

- <b>Setup Virtual Env</b>

	<a href = "https://docs.python.org/ko/3/library/venv.html">Official Docs</a><br/>
	프로젝트 실행을 위한 가상환경을 설정합니다.<br/>
	```
	E:\Workspace > python -m venv venv (venv is your virtualenv name)
	E:\Workspace > .\venv\Scripts\activate.bat
	(venv) E:\Workspace >
	```
	
<br/>


## 2. Install Python Libraries

VMeta에 사용되는 라이브러리들을 설치합니다.


- <b>requirements.txt</b>

	requirements.txt에 있는 라이브러리들을 설치합니다.
	```
	(venv) E:\Workspace > cd VideoMetaSystem
	(venv) E:\Workspace\VideoMetaSystem > pip install -r requirements.txt
	```
	
<br/>

- <b>Ffmpeg</b>

	<a href = "https://ffmpeg.org/download.html#releases">Download Link</a><br/>
	영상에서의 음원 추출을 위해 Ffmpeg을 설치합니다.<br/>
	프로젝트 내 라이브러리와의 충돌을 방지하기 위해 <b>4.4.*</b> 버전의 설치를 권장합니다.<br/>
	${Workspace}\VideoMetaSytem 에 압축 파일을 해제하고, 환경변수를 등록합니다.<br/>
	VideoMetaSystem 하위의 구조가 아래와 같아야 합니다.
	```
	(venv) E:\Workspace\VideoMetaSystem > dir
	```
	
<br/>
<br/>
<br/>


## 3. Set up MySQL

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