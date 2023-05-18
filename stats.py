import matplotlib.pyplot as plt
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
def fetch_stats(selected_user, df):
    if selected_user != "Overview":
        df =  df[df['user'] == selected_user]

    # 1. fetching total messages done by user
    messages = df.shape[0]

    #2. Fetching total words
    words = []
    for word in df['message']:
        words.extend(word.split())

    #3. fetching total media files share
    media_files = df[df['message'] == '<Media omitted>\n'].shape[0]

    #4. fetching count of links
    links = []
    extractor = URLExtract()
    for link in df['message']:
        links.extend(extractor.find_urls(link))


    return messages, len(words), media_files, len(links)

def most_busy_users(df):
    busy = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns ={'index' : 'name', 'user':'percent'})
    return busy, new_df

def wc_maker(selected_user, df):
    if selected_user != "Overview":
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    f = open('C://Users/abhay/wp_chat_analyser/stop_hinglish.txt', 'r')
    stop_words = f.read()
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)


    wc = WordCloud(width=500, height=500, min_font_size=10, background_color= (179, 179, 204))
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc

def common_words(selected_user, df):
    if selected_user != "Overview":
        df =  df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    f = open('C://Users/abhay/wp_chat_analyser/stop_hinglish.txt', 'r')
    stop_words = f.read()
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    common_df = pd.DataFrame(Counter(words).most_common(20))

    return common_df
## EMOJI
def emojis_helper(selected_user, df):
    if selected_user != "Overview":
        df =  df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.distinct_emoji_list(message)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != "Overview":
        df =  df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != "Overview":
        df =  df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count().reset_index()

    return daily_timeline

def week_activity(selected_user, df):
    if selected_user != "Overview":
        df =  df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity(selected_user, df):
    if selected_user != "Overview":
        df =  df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != "Overview":
        df =  df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message',aggfunc='count').fillna(0)
    return user_heatmap