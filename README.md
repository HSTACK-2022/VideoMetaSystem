
# 영상의 풍부한 메타데이터 자동 구축 및 효과적인 검색, 재생 시스템 <br/> (VMeta, Video Meta System)

<br/>

> Video Meta System (이하 VMeta)는 영상의 메타데이터를 자동으로 구축해 <br/>
> 사용자에게 세밀하고 용이한 검색을 가능하게 하는 시스템이다. 

<br/>
<br/>
<br/>
<br/>

## ✔ NOTICE

2022년 7월부터, 본 프로젝트는 <b>Flask Framework를 사용합니다.</b><br/>
이전 Django Framework를 사용한 프로젝트는 [여기](https://github.com/yeondelight/VideoMetaSystem/tree/c8f0593a7dfdaf904dcb72204b0092fa8b1f5429)를 참고해주세요.

<br/>
<br/>
<br/>
<br/>

## 📷 시연 영상

하단 이미지를 클릭하시면 영상을 시청하실 수 있습니다.

[<img src="https://user-images.githubusercontent.com/73868349/190308249-a1e155d6-1c6c-498b-b770-3e878201305e.png" alt="VMeta"
 width = "480" height="270" />](https://www.youtube.com/watch?v=Yx6FR8dVEGw)

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

1. VMeta는 사용자가 영상을 입력 받아 <b>영상 검색에 필요한 풍부한 메타데이터를 자동으로 구축</b> 하는 웹 시스템이다.<br/>
영상의 메타데이터는 총 13가지로 이루어진다.

2. 풍부한 메타데이터를 바탕으로 수많은 영상 가운데 <b>사용자의 의도에 맞는 영상을 찾기 위해 검색의 정확도를 높일 Deep Rank 알고리즘을 개발</b>했다.

3. 영상 내에서 <b>영상에 대한 메타데이터를 직접 보여줄 수 있는 기능</b>을 구축한다.<br/>
따라서 사용자는 동영상의 세세한 정보를 스스로 확인할 수 있다.

4. 영상 내에서 <b>사용자가 원하는 지점을 단번에 찾아내고, 재생할 수 있는 웹 플레이어</b> 기능이 있다.

5. 영상 당 메타데이터의 정보와 비율, 성능, 그리고 검색어의 빈도수와 같은 데이터들의 상태를 쉽게 파악할 수 있는 <b>모니터링 시스템</b>이 제공된다.<br/>
모니터링 데이터는 추후 랭킹 알고리즘 정확도 개선에 이용되고, 통계 자료들은 성능 평가에 이용된다.

<br/>
<br/>
<br/>
<br/>

## ⚙️ 시스템 구성 및 아키텍처

### - 시스템 구성

&nbsp;&nbsp; VMeta는 사용자가 디테일하고 정확도 높은 영상을 검색하고 확인할 수 있는 시스템으로 다음 그림과 같이 VMeta가 실행되는 사용자들의 브라우저와 웹페이지와 소프트웨어 모듈이 있는 Flask, MySQL DB로 구성된다. 
   
&nbsp;&nbsp; VMeta를 이용하는 사용자는 영상을 업로드하거나 모니터링하는 관리자와 영상을 검색하고 영상을 찾는 사용자로 나뉜다. 영상을 업로드하는 사용자는 시스템에 영상을 업로드하면, 시스템 내에서 자동으로 영상의 메타데이터를 생성하고 데이터베이스에 저장한다. 데이터베이스에 저장된 메타데이터는 서버에게 JSON 형식으로 반환된다. 반환된 데이터로 사용자는 영상을 검색할 수 있고 관리자는 모니터링 시스템을 사용할 수 있다. 

<br/>

   <img src=./report/img/flaskArch.jpg alt="flaskArch1" width = "700"/>

<br/>
<br/>
   
### - VMeta 구조

&nbsp; VMeta의 웹과 Flask, 스토리지, Open API의 시스템 구조는 아래 그림과 같이 설계되었다. 

<br/>

   <img src=./report/img/flaskArch.jpg alt="flaskArch2" width = "700"/>

<br/>
   
<b> VMeta는 크게 4가지의 기능으로 구현했다. </b> 

<br/>

* 메타데이터 생성 모듈

&nbsp;&nbsp; 이 시스템을 이용하는 사용자가 영상을 서버에 올리면 서버에서 영상을 분석하여 풍부한 메타데이터를 자동으로 구축한다. 영상 분석은 영상의 음성 데이터와 영상 데이터를 FFmpeg, STT서비스, OpenCV, Tenserflow 등 다양한 기법을 통해 처리된다. 분석한 결과는 총 13가지의 메타데이터가 생성되고, 메타데이터는 영상의 제목, 작성자, 영상의 길이, 프레임, 타입, 크기, 업로드 시각, Category, Narrative type, Presentation, Index, Keyword, Script로 구성된다. 

<br/>

* 영상 검색 모듈

&nbsp;&nbsp; 그리고 VMeta는 본 팀이 고안한 Deep Rank 알고리즘을 이용하여 사용자의 영상 검색 요청 의도에 가장 적합한 영상을 추천한다. Deep Rank 알고리즘은 자동으로 분석된 메타데이터를 이용하기 때문에 기존의 검색 엔진에 사용된 정보보다 더 다양한 정보를 사용할 수 있어 검색 정확도가 높다.

<br/>

* 타임라인 생성 모듈

&nbsp;&nbsp; 또한 영상 내에서 원하는 지점을 단번에 찾아내고, 찾은 영상을 바로 재생할 수 있는 웹 플레이어 기능이 있어 사용자가 원하는 정보를 쉽게 찾을 수 있다.

<br/>

* 모니터링 모듈

&nbsp;&nbsp; 관리자에게 메타데이터의 정보와 비율, 성능, 검색어의 빈도수와 같은 데이터들의 현황을 파악할 수 있는 모니터링 시스템을 제공한다. 이 데이터들은 추후에 Deep Rank 알고리즘의 정확도 개선에 이용될 수 있고, 통계 자료들은 성능을 평가하는데 이용될 수 있다.


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
 
<br/><br/>
</b>
   
<br/>

### 2. 기대 효과 및 활용 분야

#### - 기대 효과

- 사용자가 영상 내에서 원하는 시점으로 이동가능
- 장면 검색을 용이하게 함
- 사용자의 의도에 맞는 정확한 영상 검색 가능
- 접근성이 쉬운 시스템


#### - 활용 분야

- 본 프로젝트의 영상 메타데이터 자동 생성 기술을 e-learning, 동영상 플랫폼 등에 적용 가능
- 본 프로젝트의 소프트웨어를 동영상 플랫폼에 즉각 활용 및 상용화 가능

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
