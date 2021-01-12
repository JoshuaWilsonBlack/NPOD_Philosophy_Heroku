import pandas as pd

philoso_sub_df = pd.read_pickle('pickles/philoso_sub_df.tar.gz')

philoso_sub_df = philoso_sub_df.sample(n=500)
philoso_sub_df.to_pickle('pickles/philoso_sub_df.tar.gz')
del philoso_sub_df


nb1_sub_df = pd.read_pickle('pickles/nb1_philoso_df.tar.gz')
nb1_sub_df = nb1_sub_df.sample(n=500)
nb1_sub_df.to_pickle('pickles/nb1_sub_df.tar.gz')
del nb1_sub_df


nb2_sub_df = pd.read_pickle('pickles/nb2_philoso_df.tar.gz')
nb2_sub_df = nb2_sub_df.sample(n=500)
nb2_sub_df.to_pickle('pickles/nb2_sub_df.tar.gz')
del nb2_sub_df
