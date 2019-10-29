LIST_OF_COMPANIES_WIKI = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

class Dataset:
    def __init__(self):
        self.labels = None

    def scrape(self):
        '''
        Scrapes from wikipedia
        '''
        import requests
        website_url = requests.get(LIST_OF_COMPANIES_WIKI).text
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(website_url, "html.parser")
        #print(soup.prettify())

        my_table = soup.find('table',{'class':'wikitable sortable', 'id': "constituents"})
        #print(my_table)

        label_items = my_table.findAll('a', {'class': 'external text', 'rel': 'nofollow'})
        #print(labels)

        labels = []
        for label_item in label_items:
            label = label_item.get_text()
            if label == 'reports' or label == 'Aptiv Plc':
                continue
            labels.append(label)

        #print(labels)
        #print(len(labels))

        return labels
    
def generate():
    return get_worldnews_hot_25()

def get_worldnews_hot_25():
    import praw

    r = praw.Reddit('bot1', user_agent='worldnews_get_hot_25')
    submissions = r.subreddit('worldnews').hot(limit=25)
    return [str(x.title) for x in submissions]

d = Dataset()
d.scrape()
