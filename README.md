
# 영상의 풍부한 메타데이터 자동 구축 및 효과적인 검색, 재생 시스템 <br/> (VMeta, Video Meta System)

<br/>

> Video Meta System (이하 VMeta)는 영상의 메타데이터를 자동으로 구축해 <br/>
> 사용자에게 세밀하고 용이한 검색을 가능하게 하는 시스템이다. 

<br/>

## ✔ NOTICE

2022년 7월부터, 본 프로젝트는 <b>Flask Framework를 사용합니다.</b><br/>
이전 Django Framework를 사용한 프로젝트는 [여기](https://github.com/yeondelight/VideoMetaSystem/tree/c8f0593a7dfdaf904dcb72204b0092fa8b1f5429)를 참고해주세요.

<br/>
<br/>

## 📷 소개 영상

하단 이미지를 클릭하시면 영상을 시청하실 수 있습니다.

[<img src="https://user-images.githubusercontent.com/73868349/171586152-85d907ca-51e4-4186-998c-c3c808e651e2.jpg" alt="VMeta"
 width = "480" height="270" />](https://youtu.be/-k8TcLdf65s)

<br/>
<br/>

## 📌 작품 소개

> 💡 VMeta는 영상의 메타데이터를 자동으로 구축하고<br/>
> 이를 통해 사용자에게 세밀하고 용이한 검색을 제공하는 웹 시스템입니다.

<br/>

### 1. 프로젝트 정의

  본 프로젝트는 영상을 실시간으로 분석해 영상의 속성을 반영하는 풍부한 메타데이터를 생성하여, 사용자에게 세밀하고 용이한 검색을 가능하게 하는 시스템 VMeta를 개발한다. VMeta는 음성인식 기술로 영상에서 음성을 텍스트로 자동 추출하고 OpenCV와 딥러닝 기술을 통해 각 프레임에서 정보를 추론한다. 이를 통해 영상의 키워드, 주요 구간, 주제 등 13개의 메타데이터를 생성하고 데이터베이스에 저장한다. 본 프로젝트는 Flask를 이용하여 웹 서비스로 구현되었다.

  사용자가 본 프로젝트에서 개발한 VMeta에 영상을 업로드하면 세밀한 메타데이터가 자동으로 구축된다. 시스템은 내부의 랭킹 알고리즘을 통해 사용자가 검색한 영상을 정확도 순으로 제공할 뿐만 아니라 강의 동영상을 PPT로 변환하여 제공한다. 검색한 영상에 대한 모든 메타데이터를 바탕으로 사용자는 긴 영상에서 원하는 시간 지점을 빠르게 찾고 쉽게 청취할 수 있다.
  
<br/>

### 2. 프로젝트 배경

  오늘날 인터넷을 통한 다양한 비디오 공유 플랫폼이 눈에 띄게 성장하게 되었다. 뿐만 아니라, 최근 코로나 팬데믹으로 인해 외부대신 집에서 활동하는 시간이 늘어났고, 대면 강의 대신 온라인 수업을 활용하기 시작했다. 이러한 시대적 흐름과 일련의 요인들로 인해 온라인 비디오 시청률과 미디어 콘텐츠의 소비는 자연스럽게 증가하게 되었다. 하지만 비디오의 증가는 사용자가 원하는 비디오를 찾는데 정확도가 떨어지는 문제가 발생한다. 또한, 검색을 통해 비디오를 찾았다고 할지라도 자신이 원하는 정보를 찾기 위해 비디오를 조금씩 재생하는 수고를 더하게 된다. 따라서 이러한 문제점을 해결하기 위해 VMeta 시스템을 제안했다.
  
   VMeta는 기존의 비디오 검색에 이용되었던 제목, 작성자, 설명 등 단순한 데이터뿐만 아니라 디테일한 검색이 가능하게 할 풍부한 메타데이터를 자동 구축한다. 풍부한 메타데이터를 바탕으로 사용자의 의도에 맞는 비디오를 찾기 위해 검색의 정확도를 높일 랭킹 알고리즘을 구현하고 사용자는 이러한 메타데이터를 직접 확인할 수 있다. 또한 긴 동영상 내에서 사용자가 원하는 지점에서 재생할 수 있는 플레이어를 제공한다.

<br/>

### 3. 프로젝트 목표

- **정확한 영상 검색**

  핵심어 추출을 기반으로 키워드 일치 순으로 결과를 정렬한다.   
  자동 추출된 메타데이터를 바탕으로 다양한 세부 검색을 제공하여 빠르고 정확한 정보를 얻을 수 있다.
  
    
- **쉬운 장면 검색**
    
  OpenCV와 STT를 활용하여 키워드와 스크립트를 추출한다.  
  이를 활용해 타임스탬프와 목차를 제공하고 영상 내에서 장면 검색이 가능하다.
    

<br/>
<br/>


<br/>
<br/>

## ⚙️ 시스템 구조

### √ 전체 구조

   ![flaskArch](./report/img/flaskArch.jpg)

<br/>
<br/>
<br/>
<br/>


### √ Ranking 알고리즘

Video Ranking 알고리즘은 3단계의 연산으로 이루어진다.

#### 1. Weight Decision
- 각 검색 파라미터의 가중치(Wi)의 초기 값은 Title, Presenter, Keyword, Category가 각각 0.3, 0.3, 0.2, 0.2이다. 검색 파라미터가 생략된 경우 모든 검색 파라미터 값을 수정한다. 검색 파라미터가 생략된 경우, 검색 파라미터의 가중치를 나머지 검색 파라미터들의 가중치에 균등하게 나누어준다. n번째 검색 파라미터가 생략되었다면 다음과 같이 Wi를 재계산한다.

	Wi  = Wi  + Wn/3, for all Wi (i≠n) <br/>
	Wn  = 0
	
	검색 파라미터의 가중치 Wi는 비디오에 종속되지 않는 값이다.
	
<br/>

#### 2. 각 비디오 V에 대해 PVi의 결정
- 데이터베이스에 저장된 각 비디오 V에 대해 PV0~PV3까지의 값을 계산한다. PVi는 i번째 검색 파라미터가 비디오 V와 일치할 확률을 나타낸다. PV0는 Title 파라미터가 데이터베이스에 저장된 비디오 V의 Title 메타 데이터과 일치할 때 1이고, 일치하지 않으면 0 값으로 결정된다. PV1  역시 Presenter 파라미터가 비디오 V의 Presenter 메타데이터와 일치할 때 1이고 일치하지 않으면 0을 값으로 결정된다.

- PV2와 PV3의 결정은 간단치 않다. Keyword 메타데이터는 표 3과 같이 키워드가 비디오에서의 중요도와 함께 중요도 순으로 저장된다. 중요도는 1보다 작거나 같은 실수로 표현되며 가장 중요한 키워드의 중요도는 1이다. 표 3은 한 비디오의 Keyword 메타데이터를 샘플을 보여준다. 여기서 “Operating System” 키워드는 해당 비디오에서 가장 중요한 키워드로서 1의 중요도를 가지고 그 다음 “Virtual Memory” 키워드는 0.4의 중요도를 가진다.

	|인덱스| Keyword | Importance(M) |
	|--|--|--|
	| 0 | Operating System | 1 |
	| 1 | Virtual Memory | 0.4 |
	| 2 | Linux | 0.3 |
	| ... | ... | ... |

	검색 키워드가 비디오 V의 메타데이터에서 발견되었을 때 중요도 값 M을 반영하여 PV2는 다음과 같이 계산된다.

	PV2  = PV2  x MV

	검색 키워드가 비디오 V의 Keyword 메타데이터에서 발견되지 않는다면 PV2는 0으로 계산된다.

	Category 메타데이터의 경우 Keyword 메타데이터와 같은 방법으로, 18개의 분야에 대해 각 분야별로 M 값을 저장한다. Pv3  역시 각 비디오에 대해 Pv2와 동일한 수식으로 계산된다.

<br/>
 
 #### 3. 비디오 랭킹 계산
- Wi와 비디오 v에 대한 Pvi가 모두 결정되면, 파라미터 Pvi와 가중치 Wi를 활용하여 검색에 대한 일치성을 나타내는 Rv를 다음 식과 같이 계산한다.

	Rv  = ∑Pvi·Wi, where ∑Wi = 1

	Rv가 높을수록 검색 파라미터가 비디오 v와 일치할 가능성이 높은 것으로 판단한다.

<br/>

##### 1~3의 과정을 표로 정리한 내용은 아래와 같다.
<br/>
   <img src=./report/img/rankingWeightTable_Flask.jpg alt="rankingAlgo" width = "500" /> 
    
<br/>
<br/>


<br/>
<br/>

## 🔧 적용 기술 및 특이 사항

### 개발 환경 

![Windows 10](https://img.shields.io/badge/Windows%2010-%234D4D4D.svg?style=for-the-badge&logo=windows-terminal&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

### 개발 도구

![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)

### 개발 언어

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![html](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Javascript](https://img.shields.io/badge/Javascript-F7DF1E?style=for-the-badge&logo=Javascript&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)

### 핵심 기술

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)

### 특이 사항

- MySQL로 메타데이터 관리가 가능한 Flask 서버
- Tensorflow의 Keras와 OpenCV, FFmpeg 등 다양한 기술을 활용해 풍부한 메타데이터를 생성
- HTML, CSS, Javascript를 이용한 웹 홈페이지 제작


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
 <img src=./report/img/executeScreenshot4.jpg alt="executeScreenshot5" width = "1000" />
 
<br/><br/>

 - 상세 모니터링 페이지 : Video Details
 <img src=./report/img/executeScreenshot4.jpg alt="executeScreenshot6" width = "1000" />
 
<br/><br/>
</b>
   
<br/>

### 2. 기대 효과

- 본 프로젝트의 영상 메타데이터 자동 생성 기술을 e-learning, 동영상 플랫폼 등에 적용 가능
- 본 프로젝트의 소프트웨어를 대학이나 동영상 플랫폼에 즉각 활용 및 상용화 가능
- 사용자가 원하는 영상을 정확도 순으로 정렬하여 제공
- 사용자에게 영상 내에서 원하는 시점과 장면 검색을 용이하게 함

<br/>
<br/>


<br/>
<br/>

## 📖 참고자료
- 음성 처리 기술 : ETRI. 2021. ETRI 음성처리기술. https://aiopen.etri.re.kr/# (2022)

- 한국어 전/후처리 : KoNLPy. 2022. KoNLPy. https://github.com/konlpy/konlpy (2022)

- Background task : ParthS007. 2021. background. https://github.com/ParthS007/background/releases/tag/v0.2.1 (2022)
