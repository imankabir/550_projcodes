#import the relevant modules
import pandas as pd #to build dataframes
import seaborn as sns #for statistical data visualization
import matplotlib.pyplot as plt #for plotting in python
from wordcloud import WordCloud #to generate wordclouds
import nltk #for data cleaning
from nltk import sent_tokenize, word_tokenize #to create word tokens
import re #for data cleaning

df_yandhi = pd.read_csv('Yandhi_output.csv',encoding='latin-1') #reading the Yandhi CSV 
df_Kanye = pd.read_csv('Kanye_output.csv',encoding='latin-1') #reading the Kanye CSV
df_SNL = pd.read_csv('SNL_output.csv',encoding='latin-1') #reading the SNL CSV
df_yandhi.drop(['location'],axis = 1) #drop the location column 
df_Kanye.drop(['location'],axis = 1)
df_SNL.drop(['location'],axis = 1)

def wordcloud_generator(data,backgroundcolor,title): #this function generates the wordcloud using one of the datasets, the color for the background of the wordcloud and its title
    plt.figure(figsize = (150,150)) #setting the size of the canvas
    wc = WordCloud(background_color = backgroundcolor, max_words = 1000,  max_font_size = 50, width = 800, height = 400) #
    wc.generate(' '.join(data)) #generating the wordcloud with the data
    plt.imshow(wc) #show the images, pixels as default
    plt.axis('off') #remove the axes/gridlines

Yandhi_tweets = df_yandhi.loc[:,"tweet "] #extracting the tweets column 
Kanye_tweets = df_Kanye.loc[:,"tweet "]
SNL_tweets = df_SNL.loc[:,"tweet "]

def cleaned_tweets(listoftweets): #cleaning the tweets for the frequency distributions
	tweets_cleaned = re.sub('[^A-Za-z]+', ' ', str(listoftweets)) #remove all punctuation, numbers and return list of words
	word_tokens = word_tokenize(tweets_cleaned) #convert each word in each tweet into tokens
	cleaned_words = [] #list of cleaned words
	for word in word_tokens: #removing tokens that have a character length of less than 2
	    if len(word) >2:
	        cleaned_words.append(word)
	return cleaned_words

Yandhi_tweets_cleaned = cleaned_tweets(Yandhi_tweets) 
Kanye_tweets_cleaned = cleaned_tweets(Kanye_tweets)
SNL_tweets_cleaned = cleaned_tweets(SNL_tweets)

def frequency_distribution(cleanedtweets): #function creates the frequency distributions for each dataset
	freq_dist = nltk.FreqDist(cleanedtweets) #calculates how many times each token appears in the dataset
	frequencies = pd.DataFrame(freq_dist.most_common(100),columns=['Word','Frequency']) #generates pandas dataframe with the word and its frequencies
	return frequencies

Yandhi_fd = frequency_distribution(Yandhi_tweets_cleaned)
Kanye_fd = frequency_distribution(Kanye_tweets_cleaned)
SNL_fd = frequency_distribution(SNL_tweets_cleaned)

def frequency_plot(fd): #generate a histogram with frequencies of each word
	plt.figure(figsize=(15,15))
	sns.set_style("whitegrid") #white background
	sns.barplot(x="Word",y="Frequency",data=fd.head(20)) #generate bar plot with the 20 most common words of the dataset

frequency_plot(Yandhi_fd)
frequency_plot(Kanye_fd)
frequency_plot(SNL_fd)

wordcloud_generator(Yandhi_tweets_cleaned,'white','Yandhi Common Words' )
wordcloud_generator(Kanye_tweets_cleaned,'white','Kanye Common Words' )
wordcloud_generator(SNL_tweets_cleaned,'white','SNL Common Words' )

plt.show(block=True) #show the plot where running the python file in the terminal 

