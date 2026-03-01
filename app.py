from flask import Flask, render_template, request, jsonify
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('punkt_tab')

app = Flask(__name__)
sia = SentimentIntensityAnalyzer()
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text)
    lemmatized = [lemmatizer.lemmatize(token.lower()) for token in tokens]
    return " ".join(lemmatized)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'text' in request.form:
        text = request.form['text']
    elif 'file' in request.files:
        file = request.files['file']
        text = file.read().decode('utf-8')
    else:
        return jsonify({'error': 'No text provided'}), 400

    cleaned_text = preprocess_text(text)
    sentiment_scores = sia.polarity_scores(cleaned_text)

    compound = sentiment_scores['compound']
    # if compound >= 0.05:
    #     sentiment = 'Positive'
    # elif compound <= -0.05:
    #     sentiment = 'Negative'
    # else:
    #     sentiment = 'Neutral'

    if compound >= 0.2:
        sentiment = 'Positive'
        chart_scores = {"Positive": 1, "Negative": 0, "Neutral": 0}
    elif compound <= -0.2:
        sentiment = 'Negative'
        chart_scores = {"Positive": 0, "Negative": 1, "Neutral": 0}
    else:
        sentiment = 'Neutral'
        chart_scores = {"Positive": 0, "Negative": 0, "Neutral": 1}

    return jsonify({
        'sentiment': sentiment,
        'scores': chart_scores
    })

if __name__ == '__main__':
    app.run(debug=True)
