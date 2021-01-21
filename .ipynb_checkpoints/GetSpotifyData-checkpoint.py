# Credit for code comes from https://colab.research.google.com/drive/1-c-F9BTy2W2PkuArX0S4Rbp_kNhwB8rI#scrollTo=M3lO_HXXCpLM

# spotify API use module
import spotipy 
sp = spotipy.Spotify() 

from spotipy.oauth2 import SpotifyClientCredentials 
import spotipy.util as util
# import sys

# Set up client credentials
cid = 'f3e33e9da81b4f8388a53b5641f2dd48'
secret = 'c5e56a7d8260457a951c975b1d19294f'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# create empty lists where the results are going to be stored
artist_name = []
track_name = []
popularity = []
track_id = []

# Iterate up to 2000 incrementing offset by 50 for each query
for i in range(0,2000,50):
    track_results = sp.search(q='year:2016', type='track', limit=50,offset=i)
    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        popularity.append(t['popularity'])

import pandas as pd

df_tracks = pd.DataFrame({  'artist_name':artist_name,
                            'track_name':track_name,
                            'track_id':track_id,
                            'popularity':popularity
                        })

# group the entries by artist_name and track_name and check for duplicates
grouped = df_tracks.groupby(['artist_name','track_name'], as_index=True).size()
# grouped[grouped > 1].count()

# Drop any duplicates
df_tracks[df_tracks.duplicated(subset=['artist_name','track_name'],keep=False)].count()

# empty list, batchsize and the counter for None results
rows = []
batchsize = 100
None_counter = 0

for i in range(0,len(df_tracks['track_id']),batchsize):
    batch = df_tracks['track_id'][i:i+batchsize]
    feature_results = sp.audio_features(batch)
    for i, t in enumerate(feature_results):
        if t == None:
            None_counter = None_counter + 1
        else:
            rows.append(t)

df_audio_features = pd.DataFrame.from_dict(rows,orient='columns')

# dropping unnecessary columns
columns_to_drop = ['analysis_url','track_href','type','uri']
df_audio_features.drop(columns_to_drop, axis=1,inplace=True)
df_audio_features.rename(columns={'id': 'track_id'}, inplace=True)

# Merge the data frames
df = pd.merge(df_tracks,df_audio_features,on='track_id',how='inner')

# Save data to cwd
df.to_csv('spotify_data.csv', index=False)
