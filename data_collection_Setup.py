import tweepy, csv, retry

##### CHANGE CSV NAME BEFORE COLLECTING NEW DATA #####


def extract_tweet():
    name = '11_round_Yandhi.csv'
    header = 0
    count = 0
    try:
        consumer_key = 'uYfScUMrEtlNEGluvpkOTdGDw'
        consumer_secret = 'XeKoOdmYUzTh0sYLQEj3CZ1wljN1xhx0ud7kKcVvotT4yrxrp6'

        access_token = '1034184472252444672-94xYlw4Srou9EfI3mnCsZkx0Hbv086'
        access_token_sec = 'JxXz9bI4iWdmo5zXJfO4JOtMN9ixSxPDwzd3QQyCN01VJ'

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_sec)

        api = tweepy.API(auth)
        fetch_tweets = tweepy.Cursor(api.search, q= 'Yandhi-filter:retweets',tweet_mode='extended').items(2000)

        with open(name, mode='w', encoding='UTF-8') as my_file:
            my_writer = csv.writer(my_file, delimiter=',')
            for j in fetch_tweets:
                current_id = str(j.user.id)
                created = str(j.created_at)
                current_text = str(j.full_text)
                current_location = str(j.user.location)
                userHash = str(j.entities['hashtags'])
                row = [current_id,created, current_text, current_location, userHash]
                if header == 0:
                    my_writer.writerow(['tweet_id', 'created', 'tweet', 'location', 'Hashtags'])
                    header = header + 1
                my_writer.writerow(row)
                count = count + 1
            print(count)
            my_file.close()
    except tweepy.error.TweepError:
        print('\n\n\n\n\n NOT WORKING')

extract_tweet()