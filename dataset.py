import pandas as pd

df = pd.read_csv('table.1.1.csv')
df.groupby('bid')
b = df.groupby('bid').first()

df = pd.read_csv('table.1.1.csv')
df['bid'] = df['bid'].map(lambda v: v.strip('B')).astype(int)
df.pivot(index='pos', columns='lid', values='bid').as_matrix()
