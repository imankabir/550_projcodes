def open_reader(file,output_file_name):
    output_file = open(output_file_name,"a")
    with open(file,errors="ignore") as  csv_file:
        csv_reader=csv.reader(csv_file,delimiter=",")
        for row in csv_reader:
            if len(row)<5:
                continue
            row[2] = remove_handles(row[2])
            row[2] = preprocess_tweet(row[2])
            tweet = ""
            for word in row[2]:
                tweet+=word + " "
            row[2] = tweet
            if len(row[2]) >  1:
                for word in row:
                    output_file.write(word)
                    output_file.write(",")
                output_file.write("\n")
    output_file.close()
    csv_file.close()


def remove_handles(tweet):
    tweet = tweet.split()
    new_tweet = list()
    for word in tweet:
        if '@' in word:
            continue
        new_tweet.append(word)
    tweet = " ".join(new_tweet)
    return tweet


def preprocess_tweet(tweet):
    words = tweet.split(' ')
    preprocessed_tweet = ""
    for word in words:
        if "http" in word:
            continue
        else:
            preprocessed_tweet += word + " "

    return make_lower(remove_stopwords(remove_punctuation(remove_non_ascii(preprocessed_tweet.split()))))


def make_lower(words_list):
    new_words=[]
    for word in words_list:
        new_word=word.lower()
        new_words.append(new_word)
    return new_words


import unicodedata
import html
def remove_non_ascii(words_list):
    new_words=[]
    for word in words_list:
        new_word = html.unescape(word)
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8',)
        new_word = html.unescape(new_word)
        new_words.append(new_word)
    return new_words


def remove_punctuation(words_list):
    new_words = []
    for word in words_list:
        word = word.replace(",", "").replace(".", "").replace("!", "").replace("/", "").replace("'", "").replace('"',
                                                                                                                 "").replace(
            "$", "")
        new_words.append(word)
    return new_words


import nltk
from nltk.corpus import stopwords
def remove_stopwords(words_list):
    new_words = []
    for word in words_list:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words


def read_file(file, name):
    if file.endswith('.csv') and (name in file):
        output_file_name = name + "_output.csv"
        open_reader(file, output_file_name)


import csv, os
csv_dir = os.chdir('/Users/rubinakabir/Documents/550/Project/Data Collected')
dirs=os.listdir()
names = ["Kanye", "SNL", "Yandhi"]
for file in dirs:
    for name in names:
        if name in file:
            if "output" in file:
                continue
            read_file(file, name)