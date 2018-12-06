import csv, os
from textblob import TextBlob
import pandas as pd

csv_dir = os.chdir('/Users/rubinakabir/Documents/550/Project/Data Collected')
dirs = os.listdir()
file_names = list()

for i in dirs:
    if i.endswith('.csv') and 'SNL' in i and 'output' in i:
        file_names.append(i)

print(file_names)
total_sentiment = 0
line_count = 0
pos_sentiment = 0
pos_lc = 0
neg_sentiment = 0
neg_lc = 0
neutral_sentiment = 0
neutral_lc = 0

path = '/Users/rubinakabir/Documents/550/Project/Data Collected/%s'
output_file = open('SNL_sentiment.csv', mode='w', encoding='UTF-8')
my_writer = csv.writer(output_file, delimiter=',')
header = ['File Name','Date','Positive Sentiments','Neutral Sentiments','Negative Sentiments']
my_writer.writerow(header)
for file in file_names:
    fhand = path % file
    print(fhand)
    with open(fhand, 'r', errors="ignore",) as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            if row == '' :
                continue

            if line_count == 0:
                line_count = line_count + 1
            else:
                try:
                    txt = row[2]
                except:
                    print(row, file)
                    continue
                sentiment = TextBlob(txt).polarity

                if sentiment == 0:
                    rr = [row[0], row[1], 0, sentiment, 0]
                    my_writer.writerow(rr)
                    neutral_sentiment = neutral_sentiment + 1
                    neutral_lc = neutral_lc + 1
                if sentiment != 0:
                    total_sentiment = total_sentiment + sentiment
                    line_count = line_count + 1
                if sentiment < 0:
                    rr = [row[0], row[1], 0, 0, sentiment]
                    my_writer.writerow(rr)
                    neg_sentiment = neg_sentiment + sentiment
                    neg_lc = neg_lc + 1
                if sentiment > 0:
                    rr = [row[0], row[1], sentiment, 0, 0]
                    my_writer.writerow(rr)
                    pos_sentiment = pos_sentiment + sentiment
                    pos_lc = pos_lc + 1
my_writer.writerow(['-','Total Sentiment Counts',pos_lc, neutral_lc, neg_lc])
my_writer.writerow(['Sum of Sentiment', total_sentiment, pos_sentiment, neutral_sentiment, neg_sentiment])
my_writer.writerow(['Average Sentiments', total_sentiment/(line_count - 1), pos_sentiment/pos_lc, 0, neg_sentiment/neg_lc])

print("Final")
print(total_sentiment/(line_count - 1))
print("Positive Sentiment")
print(pos_sentiment/pos_lc)
print("Negative Sentiment")
print(neg_sentiment/neg_lc)
print("Zeros, ", neutral_sentiment)
output_file.close()
