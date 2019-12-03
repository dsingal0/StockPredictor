import json
 
from datetime import date, datetime, timedelta
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class Sentiment:
    def __init__(self, load_file=None):
        if load_file is None:
            self.sentiment_storage = {}
        else:
            with open(load_file) as f:
                self.sentiment_storage = json.load(f)

    def get_sentiment(self, text):
        sid = SentimentIntensityAnalyzer()
        sentiment = sid.polarity_scores(text)
        
        return sentiment

    def store_json(self, store_file):
        with open(store_file, 'w') as f:
            json.dump(self.sentiment_storage, f, indent=2)

class NYTSentiment(Sentiment):
    '''
    Note: all dates are datetime objects
    '''
    def __init__(self, load_file=None):
        super().__init__(load_file)

    def get_article_text(self, date, keyword):
        '''
        Params:
            date (datetime.date): date of articles
            keyword (string): keyword that articles should contain

        Return:
            string: Concatenated text of all articles from that date
        '''
        return "I love GOOGLE. I hate google."

    def get_sentiment_for_articles(self, from_date, to_date, company_name):
        time_delta = to_date-from_date

        if company_name not in self.sentiment_storage:
            self.sentiment_storage[company_name] = {}

        sentiment_storage_company = self.sentiment_storage[company_name]

        # + 1 b/c needs to be inclusive of date range
        for i in range(time_delta.days + 1):
            curr_date = from_date + timedelta(days=i)
            text = self.get_article_text(curr_date, company_name)

            sentiment = self.get_sentiment(text)
            sentiment_storage_company[str(curr_date)] = sentiment

    def store_sentiment_for_articles(self, from_date, to_date, company_name, 
                                     store_file='NYTSentiment.json'):

        if company_name not in self.sentiment_storage:
            self.sentiment_storage[company_name] = {}

        sentiment_storage_company = self.sentiment_storage[company_name]

        if 'from_date' not in sentiment_storage_company and \
            'to_date' not in sentiment_storage_company:

            sentiment_storage_company['from_date'] = str(from_date)
            sentiment_storage_company['to_date'] = str(to_date)
            self.get_sentiment_for_articles(from_date, to_date, company_name)

        else:

            prev_from_date = sentiment_storage_company['from_date']
            prev_from_date = datetime.strptime(prev_from_date, '%Y-%m-%d').date()

            self.get_sentiment_for_articles(prev_from_date, from_date, company_name)
            sentiment_storage_company['from_date'] = str(from_date)

            prev_to_date = sentiment_storage_company['to_date']
            prev_to_date = datetime.strptime(prev_to_date, '%Y-%m-%d').date()

            self.get_sentiment_for_articles(prev_to_date, to_date, company_name)
            sentiment_storage_company['to_date'] = str(to_date)

        self.store_json(store_file)


if __name__ == '__main__':
    nyt_sa = NYTSentiment()
    from_date = date(2019, 12, 1)
    to_date = date(2019, 12, 4)
    nyt_sa.store_sentiment_for_articles(from_date, to_date, 'apple', 'SentimentTest.JSON')
    
    '''
    nyt_sa = NYTSentiment('SentimentTest.JSON')
    from_date = date(2019, 12, 1)
    to_date = date(2019, 12, 5)
    nyt_sa.store_sentiment_for_articles(from_date, to_date, 'apple', 'SentimentTest.JSON')
    '''
