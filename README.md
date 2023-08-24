# 📰 News&Stocks NLP Analysis Project based on KOSPI 200

**2023 데이터청년캠퍼스 서울과기대 Team8** 
<br>

### Description
> 2023.07.31 - 2023.08.25

### Summary

> * 해당 뉴스기사로부터 다음날 특정 종목의 주가가 오를지 내릴지에 대한 등락율 예측해주는 서비스
> * kospi 200 종목들의 카테고리별 트렌드를 파악할 수 있도록 서비스를 제공
> * 어려운 경제 뉴스를 이해할 수 있도록 요약

### Pipeline

> ![image](https://github.com/phrabit/Kdata_StockNewsAnalysis_Team8/assets/70180003/78501c90-12c8-4c18-b238-8bfc8de162d9)


---
 
 ### 데이터 수집 및 분석
 
> - Data crawling
>
> 1) stock_id : Kospi 200 종목들의 기업코드를 크롤링
> 2) stock_price : 각 종목별 5/1일부터 7/31일까지의 종가, 시가, 일별 최고가, 일별 최저가 데이터 크롤링
> 3) stock_news : 데이터 크롤링을 활용하여 Naver Finance에서 Kospi 200 종목들의 4/28일부터 8/2일까지 (2023년 2분기) 뉴스 본문 데이터 크롤링
> 
> 수집된 데이터는 Database(MySQL)에 저장 
>
>
>
>
> - Data preprocessing 
>
> 1. <strong>결측치 제거</strong> : 중복 뉴스 제거 및  정규표현식을 사용하여 한글, 영문자, 숫자 및 공백문자를 제외한 모든 문자를 제거해 최종적으로 132,336개의 데이터를 사용
> 2. <strong>토큰화</strong> : okt와 한나눔을 고려하였고 속도가 빠른 한나눔을 사용해 명사만 추출
> 3. <strong>불용어 제거</strong> : 숫자가 포함된 단어 및 한 글자 단어를 제거, 상승, 하락, 증가, 감소와 같은 단어들의 경우 토픽 모델링 결과 해석할 시 함께 나타났을 때 무엇이 상승했고 하락했는지 파악이 불가능하므로 의미 없다고 판단하여 불용어 사전에 추가
> 4. <strong>주식 카테고리 분류</strong> : 각 카테고리별 트렌드를 분석하기 위해서 한국거래소로부터 생활소비재부터 커뮤니케이션 서비스까지 총 11개의 카테고리를 얻었습니다.
> 
> 총 1,071개의 불용어 사전을 생성해 전처리를 진행하였습니다.

---

### 데이터 분석 - 1) LDA 토픽모델링 

> 카테고리별 트렌드분석을 위해 LDA 토픽모델링을 사용했습니다. 확률 기반의 모델링 기법으로 토픽별로 어떤 키워드가 구성되었는지 정보를 제공하기 때문에, 키워드 조합을 통해 효과적인 인사이트를 도출하는 장점이 있습니다. 이는 주식 카테고리별 최신 트렌드 토픽 파악하는데 적합하다고 판단하였습니다.
> 
> - LDA 토픽모델링 로직
> 하이퍼파라미터인 토픽의 개수를 정하고 모든 문서의 모든 단어에 대해서 K개 중 하나의 토픽을 랜덤으로 할당합니다.
>
> - 경기소비재 주식카테고리 토픽모델링 결과
>   
> ![lda](https://github.com/phrabit/Kdata_StockNewsAnalysis_Team8/assets/70180003/7133a2e4-d210-4f4d-98d5-e7dd98126759)
>
> 
> - 경기소비재 주식카테고리 워드클라우드 결과
>   
> ![wordcloud](https://github.com/phrabit/Kdata_StockNewsAnalysis_Team8/assets/70180003/36c5c5e8-5bea-40b4-884e-1355cf5d7658)
>



### 데이터 분석 - 2) 주가 등락 예측

> - 데이터 라벨링
> Label1은 오늘 시가와 종가를 비교하여 주가가 오르거나 유지되면 1 내리면 0으로!
> Label2는 전날 종가와 오늘의 시가를 비교해 주가가 오르거나 유지되면 1, 내리면 0으로!
> 이후 최종적으로 뉴스데이터에 label을 추가할 때 해당 뉴스가 주식 장이 열린 날 오후 6시 이전에 나왔다면 label1의 값으로, 장 시간 이외에 나온 뉴스의 경우 label2의 값으로 할당
>
> - 데이터 모델링
> TextCNN Model : 기존 RNN 계열 모델의 경우 the, of 등 필요없는 단어들을 포함하고 마지막 단어의 영향을 많이 받는 문제가 존재합니다. 이를 해결하고자 CNN의 개념을 TEXT에도 도입한 TEXT CNN 모델을 사용
>
> - 모델 구조
> ![model](https://github.com/phrabit/Kdata_StockNewsAnalysis_Team8/assets/70180003/4237348a-0dee-491e-9b50-dd19f7268073)



### 데이터 분석 - 3) 뉴스 본문 요약

> - Kobart 모델
> 요약서비스를 위해 KO-BART 뉴스모델을 사용.
> BART 모델의 경우 입력 텍스트 일부에 노이즈를 추가하여 이를 다시 원문으로 복구하는 autoencoder의 형태로 학습이 됩니다. 이를 한국어에 맞게 학습한 모델이 kobart이고 뉴스 요약을 위해 finetuning된 모델을 사용했습니다.
> ![summary](https://github.com/phrabit/Kdata_StockNewsAnalysis_Team8/assets/70180003/1f46b634-285c-4a38-89eb-7af43772fc46)

---

### Web 구현

> - 구현 영상 링크

---
