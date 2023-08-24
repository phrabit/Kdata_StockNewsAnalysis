# 📰 News&Stocks NLP Analysis Project based on KOSPI 200

**2023 데이터청년캠퍼스 서울과기대 Team8** 
<br>
### Description
> 2023.07.31 - 2023.08.25

### Summary

* 해당 뉴스기사로부터 다음날 특정 종목의 주가가 오를지 내릴지에 대한 등락율 예측해주는 서비스
* kospi 200 종목들의 카테고리별 트렌드를 파악할 수 있도록 서비스를 제공
* 어려운 경제 뉴스를 이해할 수 있도록 요약
  <br>
  <br>
---
 
 ### 데이터 수집 및 분석
 
> - data crawling
>
> 1) stock_id : Kospi 200 종목들의 기업코드를 크롤링
> 2) stock_price : 각 종목별 5/1일부터 7/31일까지의 종가, 시가, 일별 최고가, 일별 최저가 데이터 크롤링
> 3) stock_news : 데이터 크롤링을 활용하여 Naver Finance에서 Kospi 200 종목들의 4/28일부터 8/2일까지 (2023년 2분기) 뉴스 본문 데이터 크롤링
> 
> 수집된 데이터는 Database(MySQL)에 저장

![naver_finance](https://github.com/phrabit/Kdata_StockNewsAnalysis_Team8/assets/70180003/56780304-bcf2-4fda-beea-f04d441438d5)





> 
>![image](https://user-images.githubusercontent.com/61912635/107111598-b1a8a480-6894-11eb-9371-8e7303d2ca81.png)
>
> 네이버 쇼핑은 모든 쇼핑몰의 리뷰를 보여주기 때문에 일일이 쇼핑몰 별 리뷰를 모으지 않아도 되고, 카테고리화 되어 있어 리뷰가 어떤 이야기를 하는 지 쉽게 확인할 수 있음 볼
>
> - data preprocessing 
>
> stopword 제거 , 형태소 분석 후 빈도수 분석으로 dictionary 생성
>
> - analysis
>
> 생성된 긍정/부정어 사전으로 감성 분석 진행 후 긍정도의 변화를 비교
>
> ### 에어팟 1세대vs 2세대 차이점
>
> - 차이 있음 : 페어링 속도, 통화 품질, 반응속도 개선, 배터리 개선, 음성 시리 호출 기능
> 
> - 차이 없음 : 디자인, 음질
>
> 즉, 리뷰의 [품질, 성능, 배터리수명, 기능, 조작성] 카테고리는 실제로 1세대와 2세대의 차이가 있는 카테고리이며 [디자인, 착용감, 휴대성, 음질] 카테고리는 실제 변화가 없는 기능이다.

## 전처리 과정

- 불용어 제거 : 특문, 자/모음 제거

- 형태소 분석 : 리뷰를 단어별로 tokenize하여 긍정/부정 단어 매칭에 활용

![image](https://user-images.githubusercontent.com/61912635/107111732-a9049e00-6895-11eb-879f-4784d96170ee.png)

- 빈도 분석 : 사용빈도가 잦은 단어를 긍정/부정 사전에 추가

![image](https://user-images.githubusercontent.com/61912635/107111729-a144f980-6895-11eb-8f4d-0e72bd2d0ee3.png)

긍정/부정어 사전은 아래와 같음

![image](https://user-images.githubusercontent.com/61912635/107111738-bf125e80-6895-11eb-83f1-865e308d456c.png)

## 결과

실제 수집된 데이터는 아래와 같다

![image](https://user-images.githubusercontent.com/61912635/107111693-588d4080-6895-11eb-983c-fcefcfaa86be.png)

![image](https://user-images.githubusercontent.com/61912635/107111699-63e06c00-6895-11eb-9f72-076fdcfec4b6.png)

## statistics

카테고리 별 리뷰수

![image](https://user-images.githubusercontent.com/61912635/107111749-ea954900-6895-11eb-8eb0-17893f9e87eb.png)

데이터 분석의 정확성을 위해 별점과 리뷰 내용이 상이한 리뷰는 제외
ex) 너무 좋고 만족합니다 (별점1점)

에어팟 1세대에서 2세대 평균 긍정도는 증가

![image](https://user-images.githubusercontent.com/61912635/107112077-2a5d3000-6898-11eb-9ad0-6477c69a37d3.png)

## 심리 분석

제품 사양의 개선이 있는 카테고리의 긍정도 평균 변화량이 사양 변화 없는 카테고리보다 3.5배 높다

즉, 소비자들은 에어팟 2의 개선된 성능 자체에 만족하여 그 결과로 리뷰의 긍정도가 28%높아졌다고 해석할 수 있다.
하지만 성능에 전혀 변화가 없는 카테고리의 긍정도가 소폭 (8%)증가한 것으로 보아, 어느정도 보유 효과와 심적회계원리가
작용하였다고 볼 수 있다.

![image](https://user-images.githubusercontent.com/61912635/107112101-524c9380-6898-11eb-9e22-68694d2e79bd.png)

