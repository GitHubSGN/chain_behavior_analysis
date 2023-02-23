#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project ：chain_behavior_analysis 
@File ：kmeans.py
@Author ：dongzhen
@Date ：2023/2/10 18:50 
'''
import os

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from tools.dir_util import project_dir

# color
from tools.draw_uitl import plot_hist

r_hex = '#dc2624'     # red,       RGB = 220,38,36
dt_hex = '#2b4750'    # dark teal, RGB = 43,71,80
tl_hex = '#45a0a2'    # teal,      RGB = 69,160,162
r1_hex = '#e87a59'    # red,       RGB = 232,122,89
tl1_hex = '#7dcaa9'   # teal,      RGB = 125,202,169
g_hex = '#649E7D'     # green,     RGB = 100,158,125
o_hex = '#dc8018'     # orange,    RGB = 220,128,24
tn_hex = '#C89F91'    # tan,       RGB = 200,159,145
g50_hex = '#6c6d6c'   # grey-50,   RGB = 108,109,108
bg_hex = '#4f6268'    # blue grey, RGB = 79,98,104
g25_hex = '#c7cccf'   # grey-25,   RGB = 199,204,207


def run_k_means():
    fdir = os.path.join( project_dir(), 'data', 'Uniswap-V3-APE_WETH-0p3-Pool.xlsx' )
    df = pd.read_excel( fdir, sheet_name='exp', index_col=0, header=1 )

    cols = ["Average Ratio of Price Range", "Ratio of Holding Periods", "Total Principal", "Average Principal"]
    df = df[cols]

    df.loc[ df["Average Ratio of Price Range"] > 4.5, "Average Ratio of Price Range" ] = 4.5
    df.loc[ df["Total Principal"] > 50, "Total Principal" ] = 50
    df.loc[ df["Average Principal"] > 20, "Average Principal" ] = 20



    scaler = StandardScaler()
    df.loc[:, df.columns] = scaler.fit_transform(df)


    # show
    # sns.pairplot(df, hue='Ratio of Holding Periods', palette='husl')
    n_cluster = 4
    model = KMeans(n_clusters=n_cluster)
    X = df.to_numpy()
    model.fit(X)

    df_org = pd.read_excel(fdir, sheet_name='工作表9', index_col=0, header=1)
    return_hist(df_org['Net Return APY'], model.labels_)


    # PCA to show
    # Center the data
    Xc = X - np.mean(X, axis=0)
    # Initialize the PCA model
    pca = PCA(n_components=2)
    # Fit and transform the data
    projected_data = pca.fit_transform(Xc)

    # draw
    from matplotlib.colors import ListedColormap

    cmap_light = ListedColormap(['#AAFFFF', '#FFAAFF', '#FFFFAA', '#FFAAAA', '#AAFFAA', '#AAAAFF'])
    # cmap_bold1 = ListedColormap([r_hex, g_hex, dt_hex])
    cmap_bold1 = ListedColormap([r_hex, g_hex, dt_hex, g25_hex, g50_hex, o_hex,])
    # , r1_hex, tl1_hex, o_hex, tn_hex, g25_hex, g50_hex
    cmap_bold2 = ListedColormap([r_hex, dt_hex, g_hex])

    centroid = model.cluster_centers_
    projected_centroid = pca.transform(centroid)
    # label = iris.target
    # true_centroid = np.vstack((X[label == 0, :].mean(axis=0),
    #                            X[label == 1, :].mean(axis=0),
    #                            X[label == 2, :].mean(axis=0)))

    plt.figure(figsize=(12, 6))

    idx_0 = 0
    idx_1 = 2

    plt.subplot(1, 2, 1)
    plt.scatter(X[:, idx_0], X[:, idx_1], c=model.labels_, cmap=cmap_bold1)
    plt.scatter(centroid[:, idx_0], centroid[:, idx_1], marker='o', s=200, edgecolors='k', c=list(range(n_cluster)), cmap=cmap_light)
    plt.xlabel(df.columns[idx_0])
    plt.ylabel(df.columns[idx_1])
    plt.title('Cluster Class_Ori')

    # plt.subplot(1, 2, 2)
    # plt.scatter(X[:, 0], X[:, 1], c=iris.target, cmap=cmap_bold2)
    # plt.scatter(true_centroid[:, 0], true_centroid[:, 1], marker='o', s=200, edgecolors='k', c=[0, 2, 1],
    #             cmap=cmap_light)
    # plt.xlabel('sepal length (cm)')
    # plt.ylabel('sepal width (cm)')
    # plt.title('True Class')

    plt.subplot(1, 2, 2)
    plt.scatter(projected_data[:, 0], projected_data[:, 1], c=model.labels_, cmap=cmap_bold1)
    plt.scatter(projected_centroid[:, 0], projected_centroid[:, 1], marker='o', s=200, edgecolors='k',
                c=list(range(n_cluster)), cmap=cmap_light)
    plt.xlabel('PCA dim_0')
    plt.ylabel('PCA dim_1')
    plt.title('Cluster Class_PCA')

    plt.show()

    print('haha')

def return_hist(X, labels):
    for lab in set(labels):
        title = f'net_return_cluster{lab}'
        plot_hist( data_plot = X.loc[labels == lab].values,
                   title = title, output_file = f'{title}.png',
                   show_plot=False)

    print('haha')




if __name__ == '__main__':
    run_k_means()


