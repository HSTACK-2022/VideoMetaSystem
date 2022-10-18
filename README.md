
# 영상의 풍부한 메타데이터 자동 구축 및 효과적인 검색, 재생 시스템 <br/> (VMeta, Video Meta System)

<br/>

> Video Meta System (이하 VMeta)는 영상의 메타데이터를 자동으로 구축해 <br/>
> 사용자에게 세밀하고 용이한 검색을 가능하게 하는 시스템이다. 

<br/>
<br/>
<br/>

## 🔑 GUIDE

VMeta의 라이선스, 설치 및 실행 과정은 아래 문서를 참고해주세요.

<h4>LICENSE : <a href="LICENSE">GPL v3.0</a> / <a href="LICENSE_3rd.md">3rd-party</a> </h4>
<h4>Installation Docs : <a href="INSTALL_KO.md">KO</a> / <a href="INSTALL_EN.md">EN</a> </h4>
<h4>Execute Docs : <a href="EXECUTE_KO.md">KO</a> / <a href="EXECUTE_EN.md">EN</a> </h4>

<br/>
<br/>

## ✔ NOTICE

2022년 7월부터, 본 프로젝트는 <b>Flask Framework를 사용합니다.</b><br/>
이전 Django Framework를 사용한 프로젝트는 [여기](https://github.com/yeondelight/VideoMetaSystem/tree/c8f0593a7dfdaf904dcb72204b0092fa8b1f5429)를 참고해주세요.

<br/>
<br/>
<br/>

## 📷 시연 영상

하단 이미지를 클릭하시면 영상을 시청하실 수 있습니다. (youtube)

[<img src="https://user-images.githubusercontent.com/73868349/190308249-a1e155d6-1c6c-498b-b770-3e878201305e.png" alt="VMeta"/>](https://www.youtube.com/watch?v=Yx6FR8dVEGw)

<br/>
<br/>
<br/>
<br/>

## 📌 작품 소개

### 1. 개발 배경

&nbsp;&nbsp; 인터넷을 통한 비디오 공유 플랫폼의 성장과 온라인 강의나 e-learning 교육 기관의 증가, 기업들의 온라인 이용도가 높아지면서 미디어 콘텐츠의 제작과 소비는 자연스럽게 증가하게 되었다.

&nbsp;&nbsp; 하지만 온라인 미디어 콘텐츠의 증가는 수많은 영상 중에 사용자가 원하는 영상을 찾는데 어려움을 부가한다. 보통의 검색 엔진은 영상에 붙은 설명, 자막, 해시태그, 영상의 제목, 영상 소유자의 이름 등 단순하고 한정적인 정보에 의존하여 검색이 이루어지기 때문이다. 또한, 사용자가 영상을 추천을 받았다 할지라도 자신이 원하는 정보를 찾기 위해 영상을 조금씩 재생하는 수고를 더하게 된다.
  
&nbsp;&nbsp; 본 팀은 이러한 문제를 개선하기 위해 영상의 검색 정확도를 높이고, 사용자가 원하는 지점을 단번에 찾아낼 수 있도록 영상에 대한 풍부한 메타데이터를 구축하는 웹 시스템인 Video Meta System, VMeta를 제안한다.

<br/>

### 2. 개발 목적

1. VMeta는 사용자가 영상을 입력 받아 <b>영상 검색에 필요한 풍부한 메타데이터를 자동으로 구축</b> 하는 웹 시스템이다. 영상의 메타데이터는 총 13가지로 이루어진다.

2. 풍부한 메타데이터를 바탕으로 수많은 영상 가운데 <b>사용자의 의도에 맞는 영상을 찾기 위해 검색의 정확도를 높일 Deep Rank 알고리즘을 개발</b>했다.

3. 영상 내에서 <b>영상에 대한 메타데이터를 직접 보여줄 수 있는 기능</b>을 구축한다.<br/>
따라서 사용자는 동영상의 세세한 정보를 스스로 확인할 수 있다.

4. 영상 내에서 <b>사용자가 원하는 지점을 단번에 찾아내고, 재생할 수 있는 웹 플레이어</b> 기능이 있다.

5. 영상 당 메타데이터의 정보와 비율, 성능, 그리고 검색어의 빈도수와 같은 데이터들의 상태를 쉽게 파악할 수 있는 <b>모니터링 시스템</b>이 제공된다. 모니터링 데이터는 추후 랭킹 알고리즘 정확도 개선에 이용되고, 통계 자료들은 성능 평가에 이용된다.

<br/>
<br/>
<br/>
<br/>

## ⚙️ 시스템 구성 및 아키텍처

### 1. VMeta 시스템 구성

&nbsp;&nbsp; VMeta는 사용자가 정확도 높은 영상을 검색하고 확인할 수 있는 시스템이다. VMeta는 아래 그림과 같이 웹 서비스로 구현했다. 파이썬 기반의 Flask 웹 프레임워크를 사용하고, 모든 웹 서버 애플리케이션은 파이썬으로 작성되었다. 이를 위해 OpenCV, Tensorflow, FFmpeg 등 라이브러리들을 이용한다. 웹 클라이언트 애플리케이션은 파일 시스템의 자바 스크립트 코드들이 HTML과 CSS로 작성된 웹과 작용한다. 데이터베이스는 MySQL을 사용하고 메타데이터와 영상 파일, 모니터링 데이터들을 저장한다. 
   
&nbsp;&nbsp; VMeta를 이용하는 사용자는 영상을 업로드하거나 모니터링하는 관리자와 영상을 검색하고 영상을 찾는 사용자로 나뉜다. 영상을 업로드하는 사용자는 시스템에 영상을 업로드하면, 시스템 내에서 자동으로 영상의 메타데이터를 생성하고 데이터베이스에 저장한다. 데이터베이스에 저장된 메타데이터는 서버에게 JSON 형식으로 반환된다. 반환된 데이터로 사용자는 영상을 검색할 수 있고 관리자는 모니터링 시스템을 사용할 수 있다. 

   <p align="center"><img src=./report/img/flaskArch1.jpg alt="flaskArch1" width="800"/></p>

<br/>
<br/>
   
### 2. VMeta 웹 서버 어플리케이션 구조

&nbsp; 1의 시스템 구성 중 웹 서버 애플리케이션의 구조는 아래 그림과 같다. 웹 서버 애플리케이션은 크게 3가지의 모듈들로 구성되어 있고, 웹 프레임워크가 받은 request에 따라 모듈들이 동작한다. 모듈 중 메타데이터 생성 모듈은 STT(Sound To Text) Open API 서비스를 이용한다. 모듈들은 필요시 데이터베이스에서 필요한 정보를 반환 받는다.

   <p align="center"><img src=./report/img/flaskArch2.jpg alt="flaskArch2" width="600"/></p>

<br/>
   
웹 서버 애플리케이션의 3가지 모듈의 기능은 다음과 같다. 

<details>
<summary><b>메타데이터 생성 모듈</b></summary>
<div markdown="1">       
&nbsp;&nbsp; 영상을 업로드하는 사용자인 관리자 브라우저에서 영상을 업로드하면 Flask 내의 메타데이터 생성 모듈이 데이터를 받아 영상의 메타데이터를 자동으로 처리한다. 영상을 분석하고 메타데이터 생성하는 스레드들이 비동기적으로 처리하고 인터넷을 통해 Open API와 데이터를 주고받는다. 생성된 메타데이터는 데이터베이스에 영상과 함께 저장된다.
</div>
</details>

<details>
<summary><b>영상 검색 모듈</b></summary>
<div markdown="1">       
&nbsp;&nbsp; 영상 검색 모듈은 사용자가 영상을 검색하면 시스템 내의 Deep Rank 알고리즘을 이용하여 검색된 영상의 리스트를 웹에 전송한다. 데이터베이스에 저장된 메타데이터는 JSON 트리 형태로 서버에 반환된다. 사용자는 검색된 영상 리스트로 영상을 선택하고, 해당 영상의 메타데이터를 확인할 수 있다.
</div>
</details>

<details>
<summary><b>모니터링 모듈</b></summary>
<div markdown="1">       
&nbsp;&nbsp; 영상 당 메타데이터의 정보와 비율, 성능, 그리고 검색어의 빈도수와 같은 데이터들의 상태를 확인하는 관리자 브라우저에서 데이터베이스에 저장된 모니터링 데이터를 받는다. 관리자는 브라우저에서 모니터링 관련 데이터들을 확인할 수 있다.
</div>
</details>

<br/>
<br/>
   
### 3. VMeta 웹 클라이언트 어플리케이션 구조

&nbsp; 1의 시스템 구성 중 웹 클라이언트 애플리케이션의 구조는 아래 그림과 같다. 웹 클라이언트 애플리케이션은 크게 4가지의 모듈들로 구성되어 있다. 모듈들은 파일 시스템의 자바 스크립트 코드들로 동작한다. 

   <p align="center"><img src=./report/img/flaskArch3.jpg alt="flaskArch3" width = "500"/></p>

<br/>

<details>
<summary><b>영상 내부 검색 모듈</b></summary>
<div markdown="1">       
&nbsp;&nbsp; 영상 내부 검색 모듈은 사용자가 영상 내부에서 검색할 때 데이터베이스 반환 받은 음성 스크립트에서 사용자가 검색한 검색어를 찾는다. 찾은 검색어와 검색어가 영상에 나타나는 시간을 브라우저에 나타나도록 한다.
</div>
</details>

<details>
<summary><b>타임라인 생성 모듈</b></summary>
<div markdown="1">       
&nbsp;&nbsp; 타임라인 생성 모듈은 영상 플레이 중 사용자가 원하는 지점의 장면을 플레이할 수 있도록 타임라인을 생성하는 기능을 한다. 음성 스크립트나 인덱스 메타데이터의 시간과 영상 내부 검색 결과의 시간을 타임라인으로 생성한다.

</div>
</details>

<details>
<summary><b>zip, ppt 다운로드 모듈</b></summary>
<div markdown="1">       
&nbsp;&nbsp; 추출된 장면 프레임들을 PPT 슬라이드 또는 jpg 이미지들을 ZIP 파일로 묶어 다운로드 받을 수 있도록 한다.
</div>
</details>

<details>
<summary><b>모니터링 로그 기록 모듈</b></summary>
<div markdown="1">       
&nbsp;&nbsp; 사용자가 영상을 시청하고 시청을 끝냈을 때의 시간과 영상 내부 검색어를 로그 파일에 기록한다. 이 로그 파일을 기반으로 영상의 조회수와 평균 시청 시간, 영상 내부 검색어의 빈도수를 모니터링 데이터로 사용할 수 있다. 
</div>
</details>

<br/>
<br/>
<br/>
<br/>

## 🔧 적용 기술

### - 핵심 기술

- MySQL로 메타데이터 관리가 가능한 Flask 서버
- Tensorflow의 Keras와 OpenCV, FFmpeg 등 다양한 기술을 활용해 풍부한 메타데이터를 생성
- HTML, CSS, Javascript를 이용한 웹 홈페이지 제작
- 직접 개발한 Deep Rank 알고리즘을 활용하여 영상 검색의 정확도 향상

### - 개발 환경 

![Windows 10](https://img.shields.io/badge/Windows%2010-%234D4D4D.svg?style=for-the-badge&logo=windows-terminal&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

### - 개발 도구

![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-007808.svg?style=for-the-badge&logo=FFmpeg&logoColor=white)

### - 개발 언어

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![html](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Javascript](https://img.shields.io/badge/Javascript-F7DF1E?style=for-the-badge&logo=Javascript&logoColor=white)

<br/>
<br/>
<br/>
<br/>

## 🖼 프로젝트 결과

### 1. 작품 사진

<b> 

- 검색 화면 
 <img src=./report/img/executeScreenshot1.jpg alt="executeScreenshot1" width = "1000" />
 
<br/><br/>

 - 영상 업로드 화면
 <img src=./report/img/executeScreenshot2.jpg alt="executeScreenshot2" width = "1000" />
 
<br/><br/>

 - 영상 상세 정보 확인 화면
 <img src=./report/img/executeScreenshot3.jpg alt="executeScreenshot3" width = "1000" />
 
<br/><br/>

 - 영상 메타데이터 수정 화면
 <img src=./report/img/executeScreenshot4.jpg alt="executeScreenshot4" height = "300" />
 
<br/><br/>

 - 전체 모니터링 페이지 : Data Overview
 <img src=./report/img/executeScreenshot5.jpg alt="executeScreenshot5" width = "1000" />
 
<br/><br/>

 - 상세 모니터링 페이지 : Video Details
 <img src=./report/img/executeScreenshot6.jpg alt="executeScreenshot6" width = "1000" />
 
</b>
<br/>
<br/>

### 2. 기대 효과

- <b>영상 메타데이터 자동 생성 기술 확보 </b>

	영상을 세밀하게 분석하여 풍부한 메타데이터를 자동 생성하는 기술을 가지고 있다. 영상 작성자는 이 기술로 부가적인 영상 정보를 제공할 수고로움을 덜 수 있다.

- <b>사용자에게 정확한 영상 검색 제공</b>

	자동 생성된 풍부한 메타데이터와 자체 고안한 Deep Rank 알고리즘을 통해 사용자 검색 의도에 맞는 정확한 영상 검색 기능을 제공한다.

- <b>영상 내 원하는 지점에서 즉각 재생 가능</b>

	영상을 끝까지 시청하지 않더라도 사용자는 영상 내에서 원하는 정보를 검색 가능하다. 검색된 정보와 함께 제공된 타임라인을 통해 사용자는 영상에서 원하는 부분을 빠르게 찾을 수 있다.

- <b>영상으로부터 PPT 자동 생성</b>

	영상의 작성자가 추가로 영상 화면 파일을 제공할 필요 없이, PPT또는 이미지파일로 영상의 화면들을 다운로드 받을 수 있다.

<br/>
<br/>

### 3. 활용 분야

- <b>VMeta의 영상 메타데이터 자동 생성 기술을 대학이나 동영상 플랫폼에 적용 가능 </b>

	온라인 영상 매체의 수가 증가함에 따라 많아지는 온라인 교육기관들과 동영상 플랫폼에 본 프로젝트의 소프트웨어를 적용 가능하다.

- <b>영상으로부터 PPT를 자동 생성하는 웹 서비스 제공 </b>

- <b>VMeta의 소프트웨어를 e-learning, 동영상 플랫폼에 즉각 활용 및 상용화 가능 </b>

	VMeta는 영상을 업로드하면 영상에 해당하는 메타데이터를 자동으로 생성하고, 수집하므로 빠르고 영상에서 세밀한 데이터 수집과 분석을 요구하는 서비스에 적용하기에 용이하다.
	
- <b>데이터를 분석하고 공유할 수 있는 빅데이터 영상 플랫폼 구축 가능 </b>

	모니터링 시스템을 활용하여 영상의 메타데이터를 체계적으로 수집, 축적, 분석, 공유할 수 있는 빅데이터 영상 플랫폼을 구축할 수 있다.

<br/>
<br/>
<br/>
<br/>

## 📖 참고자료

- 음성 처리 기술 : FFmpeg. 2016. FFmpeg. https://github.com/FFmpeg/FFmpeg#documentation (2022)

- 음성-언어 변환 (STT) : ETRI. 2021. ETRI 음성처리기술. https://aiopen.etri.re.kr/# (2022)

- 한국어 언어처리 (전/후) : KoNLPy. 2022. KoNLPy. https://github.com/konlpy/konlpy (2022)

- 영상 처리 기술 (장면전환) : opencv. 2022. opencv. https://github.com/opencv/opencv (2022)

- 이미지에서 글자 추출 (OCR) : madmaze. 2022. pytesseract. https://github.com/madmaze/pytesseract (2022)

- Background task (비동기 실행) : ParthS007. 2021. background. https://github.com/ParthS007/background/releases/tag/v0.2.1 (2022)
