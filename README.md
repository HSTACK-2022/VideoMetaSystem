# 영상의 풍부한 메타데이터 자동 구축 및 효과적인 검색, 재생 시스템 <br/> (VMeta, Video Meta System)

Video Meta System (이하 VMeta)는 영상의 메타데이터를 자동으로 구축해 사용자에게 세밀하고 용이한 검색을 가능하게 하는 시스템이다. 
<br/><br/>

---
<br/>

## ✔ NOTICE

2022년 7월부터, 본 프로젝트는 <b>Flask Framework를 사용합니다.</b><br/>
이전 Django Framework를 사용한 프로젝트는 [여기](https://github.com/yeondelight/VideoMetaSystem/tree/c8f0593a7dfdaf904dcb72204b0092fa8b1f5429)를 참고해주세요.

---
<br/>

## 🏆 수상 내역

### 2022 한성대학교 컴퓨터공학부 캡스톤디자인 작품 발표회

| <img src=./report/img/award.jpg alt="GOLD" width = "500" /> |
| --- |
| 모바일부문 최우수상 (1위) |

<br/>

---
<br/>

## 📷 소개 영상

하단 이미지를 클릭하시면 영상을 시청하실 수 있습니다.

[<img src="https://user-images.githubusercontent.com/73868349/171586152-85d907ca-51e4-4186-998c-c3c808e651e2.jpg" alt="VMeta"
 width = "480" height="270" />](https://youtu.be/-k8TcLdf65s)

---
<br/>

## 📌 작품 소개

```
💡 VMeta는 영상의 메타데이터를 자동으로 구축하고, 이를 통해 사용자에게 세밀하고 용이한 검색을 제공하는 웹 시스템입니다.
```

### 1. 프로젝트 정의

  본 프로젝트는 영상을 실시간으로 분석해 영상의 속성을 반영하는 풍부한 메타데이터를 생성하여, 사용자에게 세밀하고 용이한 검색을 가능하게 하는 시스템 VMeta를 개발한다. VMeta는 음성인식 기술로 영상에서 음성을 텍스트로 자동 추출하고 OpenCV와 딥러닝 기술을 통해 각 프레임에서 정보를 추론한다. 이를 통해 영상의 키워드, 주요 구간, 주제 등 13개의 메타데이터를 생성하고 데이터베이스에 저장한다. 본 프로젝트는 Django를 이용하여 웹 서비스로 구현되었다.

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

---

<br/>

## ⚙️ 시스템 구조

### √ 전체 구조

   ![flaskArch](./report/img/flaskArch.jpg)

<br/>
<br/>
<br/>
<br/>


### √ Ranking 알고리즘

- Ranking 알고리즘은 영상의 Title, Presenter, Keyword, Category를 기준으로 영상의 정확도를 계산합니다.
- 기본적으로 적용되는 가중치는 <b>Title : Presenter : Keyword : Category = 3 : 3 : 2 : 2</b>입니다.
- 만약 특정 기준에 대해 검색 결과가 없을 경우, 아래의 가중치 표를 따릅니다. 

   <img src=./report/img/rankingWeightTable_Flask.jpg alt="rankingAlgo" width = "500" /> 
    
<br/>
<br/>

---

<br/>

## 🔧 적용 기술 및 특이 사항

### 개발 환경

- Windows10, Linux 20.04 LTS

### 개발 도구

- Visual Studio Code, Django, MySQL

### 개발 언어

- Python, HTML, CSS, JavaScript, SQL

### 핵심 기술

- Django Framework, OpenCV, Tensorflow, FFmpeg

### 특이 사항

- MySQL로 메타데이터 관리가 가능한 Nginx, Gunicorn과 Flask로 이루어진 서버
- Tensorflow의 Keras와 OpenCV, FFmpeg 등 다양한 기술을 활용해 풍부한 메타데이터를 생성
- HTML, CSS, Javascript를 이용한 웹 홈페이지 제작


<br/>
<br/>

---

<br/>

## 🖼 프로젝트 결과

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
 <img src=./report/img/executeScreenshot4.jpg alt="executeScreenshot4" width = "600" />
 
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

---

<br/>

## 📖 참고자료
- 음성 처리 기술 : ETRI. 2021. ETRI 음성처리기술. https://aiopen.etri.re.kr/# (2022)

- 한국어 전/후처리 : KoNLPy. 2022. KoNLPy. https://github.com/konlpy/konlpy (2022)

- Background task : ParthS007. 2021. background. https://github.com/ParthS007/background/releases/tag/v0.2.1 (2022)
