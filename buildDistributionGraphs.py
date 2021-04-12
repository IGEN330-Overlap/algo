import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# SET PLOT PARAMETERS and other
sns.set()

sns.set(font_scale=10)
sns.set(font="open sans sans-serif")
sns.set_style("darkgrid", {'axes.grid': False})
sns.set(rc={'figure.figsize': (14, 8),
            'axes.facecolor': "#79cced",
            'figure.facecolor': "#79cced",
            'axes.grid': False
            })

pd.options.display.max_columns = None

# ----- Import Data ----- #
def loadData():

    df_spotify = pd.read_json("algo/data/SpotifyData.json")
    df_BL = pd.read_csv("algo/data/brendan-spotify.csv")
    df_NL = pd.read_csv("algo/data/nick-spotify.csv")
    df_BT = pd.read_csv("algo/data/btam-spotify.csv")
    df_DD = pd.read_csv("algo/data/danica-spotify.csv")
    df_TLC = pd.read_csv("algo/data/toma-spotify.csv")

    frames = [df_spotify, df_BL, df_NL, df_BT, df_DD, df_TLC]
    df = pd.concat(frames).reset_index(drop=True)
    df = df.drop_duplicates(subset=["track_name", "artist_name"])

    # Remove the track popularity 0 and any prop out of range
    df = df[df.popularity > 5]
    df = df[df.valence < 1]
    df = df[df.valence > 0]
    df = df[df.energy < 1]
    df = df[df.energy > 0]
    df = df[df.danceability < 1]
    df = df[df.danceability > 0]

    return df


def buildAndSaveDistributionPlot(attribute):
    # Verify valid attribute string passed
    if type(attribute) != str:
        return "bad attribute sent"

    # note that distplot is being deprecated so maybe switch to displot if find the time
    x = sns.distplot(df[attribute], hist=True, bins=int(50/5), color='#e5e8ee', hist_kws={'edgecolor': '#4747fc', 'linewidth': 2},
                     kde=True, kde_kws={'linewidth': 4, "color": "#4747fc"})

    sns.despine(left=True)
    plt.yticks([], [])
    x.set_xticklabels([0, 0, 0.2, 0.4, 0.6, 0.8, 1], size=20)
    x.spines['bottom'].set_color('black')

    plt.xlabel("")
    plt.ylabel("")
    plt.title(attribute.capitalize() + " Distribution For Songs", size=32)

    # Doesnt wrap the title and axis in the color palette for some reason
    plt.savefig("algo/song-distribution-pngs/" + attribute + "Dist.png")
    plt.show()
    print("Saved" + attribute + "figure to ./data/<attribute>Dist.png")
    return


if __name__ == "__main__":

    df = loadData()  # Load data

    # PLOTS AND SAVE -- Comment out line you don't need to plot
    buildAndSaveDistributionPlot("danceability")
    buildAndSaveDistributionPlot("valence")
    buildAndSaveDistributionPlot("energy")
    buildAndSaveDistributionPlot("popularity")
    buildAndSaveDistributionPlot("instrumentalness")
    buildAndSaveDistributionPlot("liveness")
    buildAndSaveDistributionPlot("speechiness")
    buildAndSaveDistributionPlot("acousticness")

    print("Saved the graphs to: " + os.getcwd() +
          "/algo/song-distributions-pngs")
