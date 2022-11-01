from pandas import read_excel
from neuroHarmonize import harmonizationLearn
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from kneed import  KneeLocator
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import umap

import os
import errno


'''
links:
PCA: ttps://www.aprendemachinelearning.com/comprende-principal-component-analysis/
Grafico con Silhouette: https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html#sphx-glr-auto-examples-cluster-plot-kmeans-silhouette-analysis-py
'''

'''
Modificación del dataframe original
'''
datos=read_excel(r'Analisis de datos Emilse\DATOS_PARA_ARMONIZAR.xlsx')
datos=datos.drop(columns=['SUJETO', 'sujeto sin guion','APOE'])

status=['AD', 'DCL','CN_AD', 'CN_DCL' ]
#Cambiar status a categorico modo dummy
for s in status:
    datos_status=datos['STATUS'].copy()
    for i in status:
        if i==s:
            datos_status.replace({i:1}, inplace=True)
        else:
            datos_status.replace({i:0}, inplace=True)
    datos['STATUS_'+s]=datos_status
#datos=datos.drop(columns=['STATUS'])#Borro la columna de status ya que la categorice

#Cambiar CENTRO a categorico modo labeled encode
centro={'OASIS':0, 'ADNI':1}
datos['CENTRO'].replace({'OASIS':0, 'ADNI':1},inplace=True)

#Cambiar CENTRO a categorico modo labeled encode
sexo={'M':1, 'F':0}
datos['SEXO'].replace({'M':1, 'F':0},inplace=True)

datos.rename(columns={'RESONADOR':'SITE'},inplace=True) #Cambiar el nombre de la columna de RESONADOR por SITE
area=[]

espesor=[]
curv_med=[]
subcorticales=[]
col_completas=list(datos.columns)
col_eliminar=['STATUS', 'CENTRO', 'SITE', 'SEXO', 'EDAD', 'ESCOLARIDAD', 'MMSE', 'CDR_TOTAL', 'CDR_SOB','STATUS_AD', 'STATUS_DCL', 'STATUS_CN_AD','STATUS_CN_DCL']
for j in col_eliminar:
    col_completas.remove(j)
volumen=col_completas[col_completas.index('Left-Thalamus'):col_completas.index('EstimatedTotalIntraCranialVol')+1]
subcorticales=col_completas[col_completas.index('left_Lateral-nucleus'):]
#Para encontrar los nombres de las columnas correspondientes a area, curvatura media y espesor
for i in range(len(col_completas)):
    if '_area' in col_completas[i]:
        area.append(col_completas[i])
    elif 'meancurv' in col_completas[i]:
        curv_med.append(col_completas[i])
    elif 'thickness' in col_completas[i]:
        espesor.append(col_completas[i])
Conjuntos={'area':area,'curvatura_media':curv_med,'espesor':espesor,'volumen':volumen}
datosvacios=datos.isnull().sum() 
print('Cantidad de datos vacios',datosvacios) #No hay datos vacios


'''
Funciones de armonización y reducción de dimensiones 
'''

def Silhoutte_graficos(X,n_clusters,carpeta,tipo,grupo):
    
    #Crear directorio antes de guardar si no se encuentra
    try:
        os.mkdir("Analisis de datos Emilse\\Graficos\\{carpeta}\\{tipo}".format(carpeta=carpeta,tipo=tipo))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    #Graficos
    # Create a subplot with 1 row and 2 columns
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(18, 7)

    # The 1st subplot is the silhouette plot
    # The silhouette coefficient can range from -1, 1 but in this example all
    # lie within [-0.1, 1]
    #ax1.set_xlim([-0.1, 1])
    # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

    # Initialize the clusterer with n_clusters value and a random generator
    # seed of 10 for reproducibility.
    clusterer = KMeans(n_clusters=n_clusters, random_state=10)
    cluster_labels = clusterer.fit_predict(X)

    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
    silhouette_avg = silhouette_score(X, cluster_labels)
    # print(
    #     "For n_clusters =",
    #     n_clusters,
    #     "The average silhouette_score is :",
    #     silhouette_avg,
    # )

    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(X, cluster_labels)

    y_lower = 10
    for i in range(n_clusters):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.nipy_spectral(float(i) / n_clusters)
        ax1.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            ith_cluster_silhouette_values,
            facecolor=color,
            edgecolor=color,
            alpha=0.7,
        )

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title("The silhouette plot for the various clusters\nThe average silhouette_score is: "+str(np.round(silhouette_avg,2)))
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    # 2nd Plot showing the actual clusters formed
    colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
    ax2.scatter(
        X[:, 0], X[:, 1], marker=".", s=30, lw=0, alpha=0.7, c=colors, edgecolor="k"
    )

    # Labeling the clusters
    centers = clusterer.cluster_centers_
    # Draw white circles at cluster centers
    ax2.scatter(
        centers[:, 0],
        centers[:, 1],
        marker="o",
        c="white",
        alpha=1,
        s=200,
        edgecolor="k",
    )

    for i, c in enumerate(centers):
        ax2.scatter(c[0], c[1], marker="$%d$" % i, alpha=1, s=50, edgecolor="k")

    ax2.set_title("The visualization of the clustered data.")
    ax2.set_xlabel("Feature space for the 1st feature")
    ax2.set_ylabel("Feature space for the 2nd feature")

    plt.suptitle(
        "Silhouette analysis for KMeans clustering on sample data with n_clusters = %d"
        % n_clusters,
        fontsize=14,
        fontweight="bold",
    )
    
    #Se guarda la figura
    plt.savefig('Analisis de datos Emilse\\Graficos\\{carpeta}\\{tipo}\\Grafico_{n_clusters}_componentes_{grupo}_{tipo}.png'.format(carpeta=carpeta,n_clusters=n_clusters,tipo=tipo, grupo=grupo))
    plt.close()
    return fig



def elbow(data,carpeta,tipo,grupo):
    distortions = []
    K = range(1,10)
    for k in K:
        kmeanModel = KMeans(n_clusters=k)
        kmeanModel.fit(data)
        distortions.append(kmeanModel.inertia_) #inertia
    
    kn = KneeLocator(K, distortions, curve='convex', direction='decreasing')
    fig,ax=plt.subplots()  
    ax.plot(K, distortions, marker='o',color='purple')
    ax.vlines(kn.knee, plt.ylim()[0], plt.ylim()[1], linestyles='dashed',color='lightblue')
    plt.xlabel('k')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method showing the optimal k \n'+'Optimal k: '+str(kn.knee))
    plt.savefig('Analisis de datos Emilse\Graficos\{carpeta}\{tipo}\Grafico_ELBOW_{tipo}.png'.format(carpeta=carpeta,tipo=tipo))
    plt.close()

def explained_variance_ratio(data,carpeta,tipo):
    #Crear directorio antes de guardar si no se encuentra
    try:
        os.mkdir("Analisis de datos Emilse\\Graficos\\{carpeta}\\{tipo}".format(carpeta=carpeta,tipo=tipo))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    pca = PCA(n_components=10).fit(data)
    kn = KneeLocator(range(1,pca.n_components+1), pca.explained_variance_ratio_, curve='convex', direction='decreasing')
    fig,ax=plt.subplots()
    ax.plot(range(1,pca.n_components+1),np.cumsum(pca.explained_variance_ratio_),label="Cumulative explained variance",color='purple',marker='o')
    ax.bar(range(1,pca.n_components+1),pca.explained_variance_ratio_,label="Explained variance ratio",color="orange")
    plt.gca().legend()
    plt.title('Explained Variance Ratio by Number of Principal Components\n'+'Optimal k: '+str(kn.knee))
    plt.xlabel('Number of Principal Components')
    plt.ylabel('Explained Variance Ratio')
    plt.savefig('Analisis de datos Emilse\\Graficos\\{carpeta}\\{tipo}\\Grafico_explanined_variance_ratio_{tipo}.png'.format(carpeta=carpeta,tipo=tipo))
    plt.close()
    return kn.knee
    
def harmonization_graficos(data,columnas,col_covars,grupo,carpeta):
    #Crear directorio antes de guardar si no se encuentra
    try:
        os.mkdir("Analisis de datos Emilse\\Graficos\\{carpeta}".format(carpeta=carpeta))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    my_data = np.array(data.loc[:,columnas])
    covars = data.loc[:,col_covars]
    my_model, data_harmonized = harmonizationLearn(my_data, covars)

     #elbow PCA grafica
    
    #Explained variance ratio
    k_armonizado=explained_variance_ratio(pd.DataFrame(data_harmonized),carpeta=carpeta,tipo='PCA_datos_armonizados')
    k_sin_armonizar=explained_variance_ratio(pd.DataFrame(my_data),carpeta=carpeta,tipo='PCA_datos_originales')
    elbow(pd.DataFrame(data_harmonized),carpeta=carpeta,grupo=grupo,tipo='PCA_datos_armonizados')
    elbow(pd.DataFrame(my_data),carpeta=carpeta,grupo=grupo,tipo='PCA_datos_originales')
  
    for comp in range(2,11,1):
        #PCA datos armonizados
        pca=PCA(n_components=comp) # Otra opción es instanciar pca sólo con dimensiones nuevas hasta obtener un mínimo "explicado" ej.: pca=PCA(.85)
        pca.fit(data_harmonized) # obtener los componentes principales
        X_pca=pca.transform(data_harmonized) # convertimos nuestros datos con las nuevas dimensiones de PCA
        Silhoutte_graficos(X_pca,n_clusters=comp,carpeta=carpeta,tipo='PCA_datos_armonizados',grupo=grupo)
        #PCA datos sin armonizar
        pca1=PCA(n_components=comp) # Otra opción es instanciar pca sólo con dimensiones nuevas hasta obtener un mínimo "explicado" ej.: pca=PCA(.85)
        pca1.fit(my_data) # obtener los componentes principales
        X_pca1=pca1.transform(my_data) # convertimos nuestros datos con las nuevas dimensiones de PCA
        Silhoutte_graficos(X_pca1,n_clusters=comp,carpeta=carpeta,tipo='PCA_datos_originales',grupo=grupo)

        #T-SNE datos armonizados
        X_TSNE = TSNE(n_components=comp,method='exact').fit_transform(data_harmonized)
        Silhoutte_graficos(X_TSNE,n_clusters=comp,carpeta=carpeta,tipo='T_SNE_datos_armonizados',grupo=grupo)
        #T-SNE datos sin armonizar
        X_TSNE1 = TSNE(n_components=comp,method='exact').fit_transform(my_data)
        Silhoutte_graficos(X_TSNE1,n_clusters=comp,carpeta=carpeta,tipo='T_SNE_datos_originales',grupo=grupo)
        
        #UMAP datos armonizados
        d_UMAP = umap.UMAP(n_neighbors=comp,min_dist=0.3,metric='correlation').fit_transform(data_harmonized)
        Silhoutte_graficos(d_UMAP,n_clusters=comp,carpeta=carpeta,tipo='UMAP_datos_armonizados',grupo=grupo)
        #UMAP datos sin armonizar
        d_UMAP1 = umap.UMAP(n_neighbors=comp,min_dist=0.3,metric='correlation').fit_transform(my_data)
        Silhoutte_graficos(d_UMAP1,n_clusters=comp,carpeta=carpeta,tipo='UMAP_datos_originales',grupo=grupo)

        if comp==k_armonizado:
            X_TSNE_pca = TSNE(n_components=comp,method='exact').fit_transform(X_pca)
            Silhoutte_graficos(X_TSNE_pca,n_clusters=comp,carpeta=carpeta,tipo='T_SNE_desde_PCA_datos_armonizados',grupo=grupo)
            d_UMAP_pca  = umap.UMAP(n_neighbors=comp,min_dist=0.3,metric='correlation').fit_transform(X_pca)
            Silhoutte_graficos(d_UMAP_pca,n_clusters=comp,carpeta=carpeta,tipo='UMAP_desde_PCA_datos_armonizados',grupo=grupo)
        if comp==k_sin_armonizar:
            X_TSNE_pca_o = TSNE(n_components=comp,method='exact').fit_transform(X_pca1)
            Silhoutte_graficos(X_TSNE_pca_o,n_clusters=comp,carpeta=carpeta,tipo='T_SNE_desde_PCA_datos_originales',grupo=grupo)
            d_UMAP_pca_o  = umap.UMAP(n_neighbors=comp,min_dist=0.3,metric='correlation').fit_transform(X_pca1)
            Silhoutte_graficos(d_UMAP_pca_o,n_clusters=comp,carpeta=carpeta,tipo='UMAP_desde_PCA_datos_originales',grupo=grupo)

    

    print('Done!')

#Para todos los datos
columnas_covars=['SITE', 'SEXO', 'EDAD', 'ESCOLARIDAD', 'MMSE','CDR_TOTAL', 'CDR_SOB','STATUS_AD', 'STATUS_DCL', 'STATUS_CN_AD', 'STATUS_CN_DCL']



for i in Conjuntos.keys():
    #Todos los grupos juntos separados por area, espesor, curvatura media y volumen
    harmonization_graficos(datos,columnas=Conjuntos[i],col_covars=columnas_covars,carpeta='Todoslosgrupos\\'+i,grupo=i+'_Todostodoslosdatos')
    status=['AD', 'DCL','CN_AD', 'CN_DCL' ]
    for s in status:
        #por cada grupo tomo proceso por area, espesor, curvatura media y volumen
        harmonization_graficos(datos[datos['STATUS']==s],columnas=Conjuntos[i],col_covars=columnas_covars[:7],carpeta=s+'\\'+i,grupo=i+'_datosdelgrupo_'+s)
        
status=['AD', 'DCL','CN_AD', 'CN_DCL' ]
for s in status:
    #por acad grupo hago todas las columnas
    harmonization_graficos(datos[datos['STATUS']==s],columnas=[*area,*curv_med,*espesor,*volumen,*subcorticales],col_covars=columnas_covars[:7],carpeta=s+'\\todaslascolumnas',grupo=i+'_datosdelgrupo_'+s)
    #por acad grupo hago solo subcorticales
    harmonization_graficos(datos[datos['STATUS']==s],columnas=subcorticales,col_covars=columnas_covars[:7],carpeta=s+'\\subcorticales',grupo=i+'_datosdelgrupo_'+s)
    #por acad grupo hago solo corticales
    harmonization_graficos(datos[datos['STATUS']==s],columnas=[*area,*curv_med,*espesor,*volumen],col_covars=columnas_covars[:7],carpeta=s+'\\corticales',grupo=i+'_datosdelgrupo_'+s)
            
harmonization_graficos(datos,columnas=[*area,*curv_med,*espesor,*volumen,*subcorticales],col_covars=columnas_covars,carpeta='Todoslosgrupos\\todaslascolumnas',grupo='Todos_los_datos')
harmonization_graficos(datos,columnas=subcorticales,col_covars=columnas_covars,carpeta='Todoslosgrupos\\subcorticales',grupo='Todos_los_datos')
harmonization_graficos(datos,columnas=[*area,*curv_med,*espesor,*volumen],col_covars=columnas_covars,carpeta='Todoslosgrupos\\corticales',grupo='Todos_los_datos')

#    

print('Valelinda')