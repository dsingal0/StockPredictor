from nltk.sentiment.vader import SentimentIntensityAnalyzer

class Sentiment:
    def __init__(self, text):
        self.text = text

    def get_sentiment(self):
        sid = SentimentIntensityAnalyzer()
        ss = sid.polarity_scores(self.text)
        
        return ss

if __name__ == '__main__':
    a = 'i love google'
    s = Sentiment(a)
    g = s.get_sentiment()
    print(g)
