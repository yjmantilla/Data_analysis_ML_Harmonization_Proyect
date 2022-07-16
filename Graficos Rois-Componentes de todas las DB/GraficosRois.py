import collections
import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


def add_roi(data,rois,roi_labels):
    """Función para añadir la columna Roi dependiendo del canal, esto para los dataframes largos"""
    for i in range(len(rois)):
        filas=data.Channels.isin(rois[i])
        data.loc[filas,'Roi']=roi_labels[i]
    return data

def graphic_roi(data,name_band,num_columns=4, save=True,plot=True):
    max=data['Powers'].max()
    sns.set(rc={'figure.figsize':(15,12)})
    sns.set_theme(style="white")
    axs=sns.catplot(x='Group',y="Powers",data=data,hue='Study',dodge=True, kind="box",col='Roi',col_wrap=num_columns,palette='winter_r',fliersize=1.5,linewidth=0.5,legend=False)
    #plt.yticks(np.arange(0,round(max),0.1))
    axs.set(xlabel=None)
    axs.set(ylabel=None)
    axs.fig.suptitle('Relative '+r'$\bf{'+name_band+r'}$'+ ' power in the ROIs of normalized data given by the databases ')
    axs.add_legend(loc='upper right',bbox_to_anchor=(.99,.99),ncol=1,title="Database")

    axs.fig.subplots_adjust(top=0.85,bottom=0.121, right=0.986,left=0.06, hspace=0.138, wspace=0.062) # adjust the Figure in rp
    axs.fig.text(0.5, 0.04, 'Group', ha='center', va='center')
    axs.fig.text(0.015, 0.5,  'Relative powers', ha='center', va='center',rotation='vertical')
    if plot:
        plt.show()
    if save==True:
        plt.savefig('Graficos Rois-Componentes de todas las DB\Graficos-Rois\{name_band}_Rois.png'.format(name_band=name_band))
        plt.close()
    
    return 


F = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8'] 
T = ['FT7', 'FC5', 'FC6', 'FT8', 'T7', 'C5', 'C6', 'T8', 'TP7', 'CP5', 'CP6', 'TP8']
C = ['FC3', 'FC1', 'FCZ', 'FC2', 'FC4', 'C3', 'C1', 'CZ', 'C2', 'C4', 'CP3', 'CP1', 'CPZ', 'CP2', 'CP4'] 
PO = ['P7', 'P5', 'P3', 'P1', 'PZ', 'P2', 'P4', 'P6', 'P8', 'PO7', 'PO5', 'PO3', 'POZ', 'PO4', 'PO6', 'PO8', 'CB1', 'O1', 'OZ', 'O2', 'CB2']
rois = [F,C,PO,T]
roi_labels = ['F','C','PO','T']

#se cargan los datos para hacer los graficos
BIO=pd.read_feather(r'D:\BASESDEDATOS\BIOMARCADORES_DERIVATIVES_VERO\derivatives\longitudinal_data_powers_long_CE_norm_channels.feather')
SRM=pd.read_feather(r'D:\BASESDEDATOS\SRM\derivatives\longitudinal_data_powers_long_resteyesc_norm_channels.feather')
CHBMP=pd.read_feather(r'D:\BASESDEDATOS\CHBMP\derivatives\longitudinal_data_powers_long_protmap_norm_channels.feather')

datos=pd.concat([SRM,BIO,CHBMP])

#Filtrado de los grupos en los que vana quedar los datos (Preguntar a Vero)
datos['Group']=datos['Group'].replace({'CTR':'Control','G2':'Control','CHBMP':'Control','SRM':'Control','G1':'Control'})

data_roi=add_roi(datos,rois,roi_labels)
bands= data_roi['Bands'].unique()
for band in bands:
    d_banda=data_roi[data_roi['Bands']==band]
    graphic_roi(d_banda,band,num_columns=2,save=True,plot=False)

print('valelinda')