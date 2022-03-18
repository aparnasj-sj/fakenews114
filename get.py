import praw
import time
import config

def loginToReddit():
    try:
        print("* Logging into Reddit...")
        reddit = praw.Reddit(client_id=config.client_id,
                             client_secret=config.client_secret,
                             user_agent='meme api by jaychandra'
                            )
        print("* Login successful!")
        return reddit
    except:
        print('* Login failed!')

reddit = loginToReddit()

def main(limit=1, subs=config.subreddits, upvotes=config.min_upvotes):
    try:
        json_list = []
        #while(True):
        submission = reddit.subreddit(subs).hot(limit=limit)
        print(submission)
        for post in submission:
            json_dict = { "title":post.title,
                            "url_to_scrape" : post.url,
                            
                }
            
            json_list.append(json_dict)
        res = {"objects":json_list}
        return res
    except Exception as e:
        print("* Something went wrong!")
        print(e)

if __name__ == "__main__":
    main()