import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load Kanye DataFrame
k_df = pd.read_csv('Kanye_sentiment.csv', index_col=0)

# Fix dates for time series plot
dates = []
for row in k_df.iterrows():
    slash = row[1][0].rfind('/')
    date = row[1][0][0:slash]
    if slash == -1:
        date = 'Delete Row'
    if date == '10/8':
        date = '10/08'
    dates.append(date)
k_df['Fixed Date'] = dates

dates = list(np.unique(dates))
dates.remove('Delete Row')
# Set up Time Series to Plo
time_series_pos = dict.fromkeys(dates, 0)
time_series_neu = dict.fromkeys(dates, 0)
time_series_neg = dict.fromkeys(dates, 0)

# Set up dfs for pos and neg sentiment values
pos_df = pd.DataFrame(columns=['Date', 'Sentiment'])
neg_df = pd.DataFrame(columns=['Date', 'Sentiment'])
for r in k_df[['Fixed Date', 'Positive Sentiments', 'Neutral Sentiments', 'Negative Sentiments']].iterrows():
    arr = [r[1][1], r[1][2], r[1][3]]
    if '-' in row[0]:  # skip stats at end of data frame
        break
    if max(arr) > 0:
        time_series_pos[r[1][0]] = time_series_pos.get(r[1][0], 0) + 1
        temp = pd.Series({'Date': r[1][0], 'Sentiment': r[1][1]})
        pos_df = pos_df.append(temp, ignore_index=True)
    if max(arr) == 0 and min(arr) == 0:
        time_series_neu[r[1][0]] = time_series_neu.get(r[1][0], 0) + 1
    if min(arr) < 0:
        time_series_neg[r[1][0]] = time_series_neg.get(r[1][0], 0) + 1
        temp = pd.Series({'Date': r[1][0], 'Sentiment': r[1][3]})
        neg_df = neg_df.append(temp, ignore_index=True)

# Remove 'Delete Row'
time_series_neu.pop('Delete Row')
time_series_neg.pop('Delete Row')
time_series_pos.pop('Delete Row')

y1 = []
y2 = []
y3 = []
for k1 in sorted(dates):
    y1.append(time_series_pos[k1])
    y2.append(time_series_neg[k1])
    y3.append(time_series_neu[k1])

# Plot Kanye Time Series
plt.figure(figsize=(20, 10))
plt.plot(dates, y1, 'g', label="Positive")
plt.plot(dates, y2, 'r', label="Negative")
plt.plot(dates, y3, 'b', label="Neutral")
plt.legend()
plt.grid(axis='both')
plt.title('Key word: Kanye West', fontsize=30)
plt.xlabel('Date')
plt.ylabel('Tweet Count')
plt.savefig('kanye_ts.png', bbox_inches='tight')

# Plot Sentiment Value analysis box plots
pos_dates = list(sorted(np.unique(pos_df['Date'])))
pos_dates.pop()

pos_dict = dict.fromkeys(pos_dates)
for r in pos_df.iterrows():
    if r[1][0] == 'Delete Row':
        break
    if pos_dict[r[1][0]] == None:
        pos_dict[r[1][0]] = []
    pos_dict[r[1][0]].append(r[1][1])

neg_dates = list(sorted(np.unique(neg_df['Date'])))
neg_dates.pop()

neg_dict = dict.fromkeys(neg_dates)
for r in neg_df.iterrows():
    if r[1][0] == 'Delete Row':
        break
    if neg_dict[r[1][0]] == None:
        neg_dict[r[1][0]] = []
    neg_dict[r[1][0]].append(r[1][1])

plt.figure(figsize=(20, 10))
plt.boxplot(pos_dict.values(), vert=False)
plt.yticks(range(1, len(pos_dict.values()) + 1), pos_dates)
plt.xlabel('Sentiment Value')
plt.title('Key Word: Kanye West\n Positive Sentiment Spread', fontsize=30)
plt.savefig('kanye_posbp.png', bbox_inches='tight')

plt.figure(figsize=(20, 10))
plt.boxplot(neg_dict.values(), vert=False)
plt.yticks(range(1, len(neg_dict.values()) + 1), neg_dates)
plt.xlabel('Sentiment Value')
plt.title('Key Word: Kanye West\n Negative Sentiment Spread', fontsize=30)
plt.savefig('kanye_negbp.png', bbox_inches='tight')

# Make sentiment analysis with scale plots
v_neg = neg_df['Sentiment'] <= -0.6
m = neg_df['Sentiment'] <= -1
v_neg_df = neg_df[v_neg]
hard_neg_count = v_neg_df.shape[0]

bb = neg_df['Sentiment'] > -0.6
neg = neg_df['Sentiment'] <= -0.4
negg_df = neg_df[bb & neg]
neg_count = negg_df.shape[0]

bbp = pos_df['Sentiment'] > 0.4
pos = pos_df['Sentiment'] <= 0.6
poss_df = pos_df[bbp & pos]

pos_count = poss_df.shape[0]

hard_pos = pos_df['Sentiment'] > 0.6
hard_pos_df = pos_df[hard_pos]
hard_pos_count = hard_pos_df.shape[0]

bar_plot_dates = dict.fromkeys(list(sorted(np.unique(pos_df['Date']))))
frames = [v_neg_df, negg_df, poss_df, hard_pos_df]

for i in range(0, len(frames)):
    for row in frames[i].iterrows():
        try:
            if bar_plot_dates[row[1][0]] == None:
                bar_plot_dates[row[1][0]] = dict.fromkeys(range(0, 5))
        except:
            continue
        if bar_plot_dates[row[1][0]][i] == None:
            bar_plot_dates[row[1][0]][i] = 0

        bar_plot_dates[row[1][0]][i] = bar_plot_dates[row[1][0]][i] + 1

nn = []
n = []
neu = []
p = []
vp = []
d = []
for kk, v in bar_plot_dates.items():
    if kk == 'Delete Row':
        continue
    d.append(kk)
    for k, vv in v.items():
        if vv == None:
            vv = 0
        if k == 0:
            nn.append(vv)
        if k == 1:
            n.append(vv)
        if k == 2:
            p.append(vv)
        if k == 3:
            vp.append(vv)
plt.figure(figsize=(20, 10))
df = pd.DataFrame(columns=range(0, 4))
df[0] = nn
df[1] = n
df[2] = p
df[3] = vp
ax = df.plot(kind='bar', figsize=(20, 10))
ax.set_xticklabels(d, rotation=0)
ax.legend(['Very Negative', 'Negative', 'Positive', 'Very Positive'])
plt.title('Key Word = Kanye West \n Sentiment Value Analysis (with scale)', fontsize=30)
plt.savefig('kanye_sentscale.png', bbox_inches="tight")


#########################################################################################
# Load Yandhi DataFrame
y_df = pd.read_csv('Yandhi_sentiment.csv', index_col=0)

# Fix dates for time series plot
dates = []
for row in y_df.iterrows():
    slash = row[1][0].rfind('/')
    date = row[1][0][0:slash]
    if slash == -1:
        date = 'Delete Row'
    if len(date) < 5:
        s = date.find('/')
        date = date[0:s + 1] + '0' + date[s + 1:]
    dates.append(date)
y_df['Fixed Date'] = dates

dates = list(np.unique(dates))
dates.remove('Delete Row')
# Set up Time Series to Plo
time_series_pos = dict.fromkeys(dates, 0)
time_series_neu = dict.fromkeys(dates, 0)
time_series_neg = dict.fromkeys(dates, 0)

# Set up dfs for pos and neg sentiment values
pos_df = pd.DataFrame(columns=['Date', 'Sentiment'])
neg_df = pd.DataFrame(columns=['Date', 'Sentiment'])
for r in y_df[['Fixed Date', 'Positive Sentiments', 'Neutral Sentiments', 'Negative Sentiments']].iterrows():
    arr = [r[1][1], r[1][2], r[1][3]]
    if '-' in row[0]:  # skip stats at end of data frame
        break
    if max(arr) > 0:
        time_series_pos[r[1][0]] = time_series_pos.get(r[1][0], 0) + 1
        temp = pd.Series({'Date': r[1][0], 'Sentiment': r[1][1]})
        pos_df = pos_df.append(temp, ignore_index=True)
    if max(arr) == 0 and min(arr) == 0:
        time_series_neu[r[1][0]] = time_series_neu.get(r[1][0], 0) + 1
    if min(arr) < 0:
        time_series_neg[r[1][0]] = time_series_neg.get(r[1][0], 0) + 1
        temp = pd.Series({'Date': r[1][0], 'Sentiment': r[1][3]})
        neg_df = neg_df.append(temp, ignore_index=True)

# Remove 'Delete Row'
time_series_neu.pop('Delete Row')
time_series_neg.pop('Delete Row')
time_series_pos.pop('Delete Row')

y1 = []
y2 = []
y3 = []
for date in sorted(dates):
    y1.append(time_series_pos[date])
    y2.append(time_series_neg[date])
    y3.append(time_series_neu[date])

# Plot Kanye Time Series
plt.figure(figsize=(20, 10))
plt.plot(dates, y1, 'g', label="Positive")
plt.plot(dates, y2, 'r', label="Negative")
plt.plot(dates, y3, 'b', label="Neutral")
plt.legend()
plt.grid(axis='both')
plt.title('Key Word: Yandhi', fontsize=30)
plt.xlabel('Date')
plt.ylabel('Tweet Count')
plt.savefig('yandhi_ts.png', bbox_inches='tight')

# Plot Sentiment Value analysis box plots
pos_dates = list(sorted(np.unique(pos_df['Date'])))
pos_dates.pop()

pos_dict = dict.fromkeys(pos_dates)
for r in pos_df.iterrows():
    if r[1][0] == 'Delete Row':
        break
    if pos_dict[r[1][0]] == None:
        pos_dict[r[1][0]] = []
    pos_dict[r[1][0]].append(r[1][1])

neg_dates = list(sorted(np.unique(neg_df['Date'])))
neg_dates.pop()

neg_dict = dict.fromkeys(neg_dates)
for r in neg_df.iterrows():
    if r[1][0] == 'Delete Row':
        break
    if neg_dict[r[1][0]] == None:
        neg_dict[r[1][0]] = []
    neg_dict[r[1][0]].append(r[1][1])

plt.figure(figsize=(20, 10))
plt.boxplot(pos_dict.values(), vert=False)
plt.yticks(range(1, len(pos_dict.values()) + 1), pos_dates)
plt.xlabel('Sentiment Value')
plt.title('Key Word: Yandhi\n Positive Sentiment Spread', fontsize=30)
plt.savefig('yandhi_posbp.png', bbox_inches='tight')

plt.figure(figsize=(20, 10))
plt.boxplot(neg_dict.values(), vert=False)
plt.yticks(range(1, len(neg_dict.values()) + 1), neg_dates)
plt.xlabel('Sentiment Value')
plt.title('Key Word: Yandhi \n Negative Sentiment Spread', fontsize=30)
plt.savefig('yandhi_negbp.png', bbox_inches='tight')

# Make sentiment analysis plots with scale
v_neg = neg_df['Sentiment'] <= -0.6
m = neg_df['Sentiment'] <= -1
v_neg_df = neg_df[v_neg]
hard_neg_count = v_neg_df.shape[0]

bb = neg_df['Sentiment'] > -0.6
neg = neg_df['Sentiment'] <= -0.4
negg_df = neg_df[bb & neg]
neg_count = negg_df.shape[0]

bbp = pos_df['Sentiment'] > 0.4
pos = pos_df['Sentiment'] <= 0.6
poss_df = pos_df[bbp & pos]

pos_count = poss_df.shape[0]

hard_pos = pos_df['Sentiment'] > 0.6
hard_pos_df = pos_df[hard_pos]
hard_pos_count = hard_pos_df.shape[0]

bar_plot_dates = dict.fromkeys(list(sorted(np.unique(pos_df['Date']))))
frames = [v_neg_df, negg_df, poss_df, hard_pos_df]

for i in range(0, len(frames)):
    for row in frames[i].iterrows():
        try:
            if bar_plot_dates[row[1][0]] == None:
                bar_plot_dates[row[1][0]] = dict.fromkeys(range(0, 5))
        except:
            continue
        if bar_plot_dates[row[1][0]][i] == None:
            bar_plot_dates[row[1][0]][i] = 0

        bar_plot_dates[row[1][0]][i] = bar_plot_dates[row[1][0]][i] + 1
nn = []
n = []
neu = []
p = []
vp = []
d = []
for kk, v in bar_plot_dates.items():
    if kk == 'Delete Row' or v == None:
        continue
    d.append(kk)
    for k, vv in v.items():
        if vv == None:
            vv = 0
        if k == 0:
            nn.append(vv)
        if k == 1:
            n.append(vv)
        if k == 2:
            p.append(vv)
        if k == 3:
            vp.append(vv)
plt.figure(figsize=(20, 10))
df = pd.DataFrame(columns=range(0, 4))
df[0] = nn
df[1] = n
df[2] = p
df[3] = vp
ax = df.plot(kind='bar', figsize=(20, 10))
ax.set_xticklabels(d, rotation=0)
ax.legend(['Very Negative', 'Negative', 'Positive', 'Very Positive'])
plt.title('Key Word = Yandhi \n Sentiment Value Analysis (with scale)', fontsize=30)
plt.savefig('yandhi_sentscale.png', bbox_inches="tight")


##########################################################################################
# Load SNL DataFrame
snl_df = pd.read_csv('SNL_sentiment.csv', index_col=0)

# Fix dates for time series plot
dates = []
for row in snl_df.iterrows():
    slash = row[1][0].rfind('/')
    date = row[1][0][0:slash]
    if slash == -1:
        date = 'Delete Row'
    if len(date) < 5:
        s = date.find('/')
        date = date[0:s + 1] + '0' + date[s + 1:]
    dates.append(date)
snl_df['Fixed Date'] = dates

dates = list(np.unique(dates))
dates.remove('Delete Row')
# Set up Time Series to Plo
time_series_pos = dict.fromkeys(dates, 0)
time_series_neu = dict.fromkeys(dates, 0)
time_series_neg = dict.fromkeys(dates, 0)

# Set up dfs for pos and neg sentiment values
pos_df = pd.DataFrame(columns=['Date', 'Sentiment'])
neg_df = pd.DataFrame(columns=['Date', 'Sentiment'])

for r in snl_df[['Fixed Date', 'Positive Sentiments', 'Neutral Sentiments', 'Negative Sentiments']].iterrows():
    arr = [r[1][1], r[1][2], r[1][3]]
    if '-' in row[0]:  # skip stats at end of data frame
        break
    if max(arr) > 0:
        time_series_pos[r[1][0]] = time_series_pos.get(r[1][0], 0) + 1
        temp = pd.Series({'Date': r[1][0], 'Sentiment': r[1][1]})
        pos_df = pos_df.append(temp, ignore_index=True)
    if max(arr) == 0 and min(arr) == 0:
        time_series_neu[r[1][0]] = time_series_neu.get(r[1][0], 0) + 1
    if min(arr) < 0:
        time_series_neg[r[1][0]] = time_series_neg.get(r[1][0], 0) + 1
        temp = pd.Series({'Date': r[1][0], 'Sentiment': r[1][3]})
        neg_df = neg_df.append(temp, ignore_index=True)

# Remove 'Delete Row'
time_series_neu.pop('Delete Row')
time_series_neg.pop('Delete Row')
time_series_pos.pop('Delete Row')

y1 = []
y2 = []
y3 = []
for date in sorted(dates):
    # Store values for time series
    y1.append(time_series_pos[date])
    y2.append(time_series_neg[date])
    y3.append(time_series_neu[date])

# Plot Time Series
plt.figure(figsize=(20, 10))
plt.plot(dates, y1, 'g', label="Positive")
plt.plot(dates, y2, 'r', label="Negative")
plt.plot(dates, y3, 'b', label="Neutral")
plt.legend()
plt.grid(axis='both')
plt.title('Key Word: Kanye on SNL', fontsize=30)
plt.xlabel('Date')
plt.ylabel('Tweet Count')
plt.savefig('snl_ts.png', bbox_inches='tight')

# Plot Sentiment Value analysis box plots
pos_dates = list(sorted(np.unique(pos_df['Date'])))
pos_dates.pop()

pos_dict = dict.fromkeys(pos_dates)
scale_dict = dict.fromkeys(pos_dates)
for r in pos_df.iterrows():
    if r[1][0] == 'Delete Row':
        break
    if pos_dict[r[1][0]] == None:
        pos_dict[r[1][0]] = []
    pos_dict[r[1][0]].append(r[1][1])

neg_dates = list(sorted(np.unique(neg_df['Date'])))
neg_dates.pop()

neg_dict = dict.fromkeys(neg_dates)
for r in neg_df.iterrows():
    if r[1][0] == 'Delete Row':
        break
    if neg_dict[r[1][0]] == None:
        neg_dict[r[1][0]] = []
    neg_dict[r[1][0]].append(r[1][1])

plt.figure(figsize=(20, 10))
plt.boxplot(pos_dict.values(), vert=False)
plt.yticks(range(1, len(pos_dict.values()) + 1), pos_dates)
plt.xlabel('Sentiment Value')
plt.title('Key Word: Kanye on SNL \n Positive Sentiment Spread', fontsize=30)
plt.savefig('snl_posbp.png', bbox_inches='tight')

plt.figure(figsize=(20, 10))
plt.boxplot(neg_dict.values(), vert=False)
plt.yticks(range(1, len(neg_dict.values()) + 1), neg_dates)
plt.xlabel('Sentiment Value')
plt.title('Key Word: Kanye on SNL \n Negative Sentiment Spread', fontsize=30)
plt.savefig('snl_negbp.png', bbox_inches='tight')

# make sentiment analysis plots with scale
v_neg = neg_df['Sentiment'] <= -0.6
m = neg_df['Sentiment'] <= -1
v_neg_df = neg_df[v_neg]
hard_neg_count = v_neg_df.shape[0]

bb = neg_df['Sentiment'] > -0.6
neg = neg_df['Sentiment'] <= -0.4
negg_df = neg_df[bb & neg]
neg_count = negg_df.shape[0]

bbp = pos_df['Sentiment'] > 0.4
pos = pos_df['Sentiment'] <= 0.6
poss_df = pos_df[bbp & pos]

pos_count = poss_df.shape[0]

hard_pos = pos_df['Sentiment'] > 0.6
hard_pos_df = pos_df[hard_pos]
hard_pos_count = hard_pos_df.shape[0]

bar_plot_dates = dict.fromkeys(list(sorted(np.unique(pos_df['Date']))))
frames = [v_neg_df, negg_df, poss_df, hard_pos_df]

for i in range(0, len(frames)):
    for row in frames[i].iterrows():
        try:
            if bar_plot_dates[row[1][0]] == None:
                bar_plot_dates[row[1][0]] = dict.fromkeys(range(0, 5))
        except:
            continue
        if bar_plot_dates[row[1][0]][i] == None:
            bar_plot_dates[row[1][0]][i] = 0

        bar_plot_dates[row[1][0]][i] = bar_plot_dates[row[1][0]][i] + 1

nn = []
n = []
neu = []
p = []
vp = []
d = []
for kk, v in bar_plot_dates.items():
    if kk == 'Delete Row' or v == None:
        continue
    d.append(kk)
    for k, vv in v.items():
        if vv == None:
            vv = 0
        if k == 0:
            nn.append(vv)
        if k == 1:
            n.append(vv)
        if k == 2:
            p.append(vv)
        if k == 3:
            vp.append(vv)
plt.figure(figsize=(20, 10))
df = pd.DataFrame(columns=range(0, 4))
df[0] = nn
df[1] = n
df[2] = p
df[3] = vp
ax = df.plot(kind='bar', figsize=(20, 10))
ax.set_xticklabels(d, rotation=0)
ax.legend(['Very Negative', 'Negative', 'Positive', 'Very Positive'])
plt.title('Key Word = Kanye on SNL \n Sentiment Value Analysis (with scale)', fontsize=30)
plt.savefig('snl_sentscale.png', bbox_inches="tight")