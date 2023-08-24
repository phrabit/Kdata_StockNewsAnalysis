from flask import Flask, request
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
import pandas as pd

# To load mysql in app.py
from flask import Flask, render_template
from app import get_data_from_mysql 

################################################################################

import pickle
import numpy as np
from konlpy.tag import Hannanum
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re

################################################################################

app = Flask(__name__)

model = pickle.load(open('CNN_model.pkl', 'rb'))
app.config['JSON_AS_ASCII'] = False

# Load tokenizer and summary
tokenizer = PreTrainedTokenizerFast.from_pretrained("ainize/kobart-news")
summary = BartForConditionalGeneration.from_pretrained("ainize/kobart-news")

def summarize_text(news_text):
    input_ids = tokenizer. encode(news_text, return_tensors="pt")
    summary_ids = summary.generate(
        input_ids=input_ids,
        max_length=128,
        min_length=2,
        num_beams=3,
        early_stopping=True
    )
    summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary_text


@app.route("/summarize", methods=["POST"])
def summarize_news():
    data = request.get_json()
    article_text = data.get("article_text")
    if article_text:
        summary = summarize_text(article_text)
        return {"summary": summary}
    else:
        return {"error": "No text provided"}
    
@app.route("/news/<int:stock_id>/<int:index>", methods=["GET"])
def view_full_news(stock_id, index):
    data = get_data_from_mysql(stock_id=stock_id, page=index // 10 + 1, per_page=10)
    local_index = index % 10
    if 0 <= local_index < len(data):
        article = data.iloc[local_index]['text']
        return render_template("news.html", article=article)
    else:
        return {"error": "Invalid local index."}

def total_pages(stock_id, per_page=10):
    total_articles = get_data_from_mysql(stock_id=stock_id).shape[0] # Total number of articles
    return -(-total_articles // per_page) # Ceiling division

@app.route('/newspage/stock/<int:stock_id>')
@app.route('/newspage/stock/<int:stock_id>/<int:page>')
def index(stock_id, page=1):
    data = get_data_from_mysql(stock_id=stock_id, page=page, per_page=10)
    total_pages_count = total_pages(stock_id=stock_id)
    return render_template("board.html", data=data, page=page, total_pages=total_pages_count, stock_id = stock_id)

################################################################################

@app.route("/")
def main_home():
    return render_template('home.html')

@app.route("/wordcloud")
def word():
    return render_template('wordcloud.html')

@app.route("/lda_result_건설")
def jpg1():
    return render_template('results/lda_result_건설.html')

@app.route("/lda_result_경기소비재")
def jpg2():
    return render_template('results/lda_result_경기소비재.html')

@app.route("/lda_result_금융")
def jpg3():
    return render_template('results/lda_result_금융.html')

@app.route("/lda_result_산업재")
def jpg4():
    return render_template('results/lda_result_산업재.html')

@app.route("/lda_result_생활소비재")
def jpg5():
    return render_template('results/lda_result_생활소비재.html')

@app.route("/lda_result_에너지_화학")
def jpg6():
    return render_template('results/lda_result_에너지_화학.html')

@app.route("/lda_result_정보기술")
def jpg7():
    return render_template('results/lda_result_정보기술.html')

@app.route("/lda_result_중공업")
def jpg8():
    return render_template('results/lda_result_중공업.html')

@app.route("/lda_result_철강_소재")
def jpg9():
    return render_template('results/lda_result_철강_소재.html')

@app.route("/lda_result_커뮤니케이션서비스")
def jpg10():
    return render_template('results/lda_result_커뮤니케이션서비스.html')

@app.route("/lda_result_헬스케어")
def jpg11():
    return render_template('results/lda_result_헬스케어.html')

@app.route('/result', methods=['post', 'GET'])
def home():
    data = request.get_data()
    time = request.form.get('time')
    value = str(data, 'utf-8')
    value = clean_text(value)
    value = sentiment_predict(value)
    positive = value*100
    negative = (1 - value) * 100

    return render_template('result.html', value = value, text=data, time=time, positive=positive, negative=negative), 200

def clean_text(d):
  text = re.sub(r'\([^)]*\)', '', d)
  text = re.sub(r'\[[^]]*\]', '', text)
  text = re.sub(r'\<[^>]*\>', '', text)
  pattern = r'[^가-힣0-9a-zA-Z\s]'
  text = re.sub(pattern, ' ', text)
  text = re.sub(r'사진', ' ', text)
  text = re.sub(r'.*뉴스', ' ', text)
  text = re.sub("\n", ' ', text)
  text = re.sub("  +", " ", text)
  return text

def sentiment_predict(new_sentence):
    tokenizer = Tokenizer(43662, oov_token='OOV')
    stopwords = [r'상승.*', r'하락.*', r'급등.*', r'급락.*', '상승세', '하락세', '폭등', '폭락', '오름세', '약세', '강세', '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다', '에', '은', '는', '하']
    new_token = [word for word in Hannanum().morphs(new_sentence) if word not in stopwords and not word.isdigit()]
    tokenizer.fit_on_texts(new_token)
    new_sequences = tokenizer.texts_to_sequences([new_token])
    new_pad = pad_sequences(new_sequences, maxlen=800)
    score = float(model.predict(new_pad))
    return round(float(score), 2)
    #return f'{score:.4f}'

################################################################################

if __name__ == "__main__":
    app.run(debug=True)