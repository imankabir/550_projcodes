import pandas as pd #import pandas module 

df_yandhi_VOS = pd.read_csv('Yandhi_output_VOS_network.csv',encoding='latin-1') #read VOS output CSV
df_Kanye_VOS = pd.read_csv('Kanye_output_VOS_network.csv',encoding='latin-1')
df_SNL_VOS = pd.read_csv('SNL_output_VOS_network.csv',encoding='latin-1')

grouped_yandhi_cluster = df_yandhi_VOS.groupby('cluster') #group by cluster
grouped_Kanye_cluster = df_Kanye_VOS.groupby('cluster')
grouped_SNL_cluster = df_SNL_VOS.groupby('cluster')

pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

print('\n'+ 'Yandhi Clustering' + '\n')
for group in grouped_yandhi_cluster:
    print(group)

print('\n'+ 'Kanye Clustering' + '\n')
for group in grouped_Kanye_cluster:
    print(group)

print('\n'+ 'SNL Clustering' + '\n')
for group in grouped_SNL_cluster:
    print(group)
