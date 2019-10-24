import praw

def generate():
    return get_worldnews_hot_25()

def get_worldnews_hot_25():
    r = praw.Reddit('bot1', user_agent='worldnews_get_hot_25')
    submissions = r.subreddit('worldnews').hot(limit=25)
    return [str(x.title) for x in submissions]
if __name__=="__main__":
    print(generate())
