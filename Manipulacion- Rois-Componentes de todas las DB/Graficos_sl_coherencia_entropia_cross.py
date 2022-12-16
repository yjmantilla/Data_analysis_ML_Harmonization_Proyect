
import collections
import pandas as pd 
import seaborn as sns
import numpy as np
import pingouin as pg
from numpy import ceil 
import errno
from matplotlib import pyplot as plt
import os
import io
from itertools import combinations
from PIL import Image
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def graphics(data,type,path,name_band,id,id_cross=None,num_columns=4,save=True,plot=True):
    '''Function to make graphs of the given data '''
    max=data[type].max()
    sns.set(rc={'figure.figsize':(15,12)})
    sns.set_theme(style="white")
    if id=='IC':
        col='Component'
    else:
        col='ROI'
    axs=sns.catplot(x='group',y=type,data=data,hue='database',dodge=True, kind="box",col=col,col_wrap=num_columns,palette='winter_r',fliersize=1.5,linewidth=0.5,legend=False)
    #plt.yticks(np.arange(0,round(max),0.1))
    axs.set(xlabel=None)
    axs.set(ylabel=None)
    if id_cross==None:
        axs.fig.suptitle(type+' in '+r'$\bf{'+name_band+r'}$'+ ' in the ICs of normalized data given by the databases')
    else:
        axs.fig.suptitle(type+' in '+id_cross+' of ' +r'$\bf{'+name_band+r'}$'+ ' in the ICs of normalized data given by the databases')

    if id=='IC':
        
        axs.add_legend(loc='upper right',bbox_to_anchor=(.59,.95),ncol=4,title="Database")
        axs.fig.subplots_adjust(top=0.85,bottom=0.121, right=0.986,left=0.05, hspace=0.138, wspace=0.062) 
        axs.fig.text(0.5, 0.04, 'Group', ha='center', va='center')
        axs.fig.text(0.01, 0.5,  type, ha='center', va='center',rotation='vertical')
    else:
        
        axs.add_legend(loc='upper right',bbox_to_anchor=(.7,.95),ncol=4,title="Database")
        axs.fig.subplots_adjust(top=0.85,bottom=0.121, right=0.986,left=0.06, hspace=0.138, wspace=0.062) # adjust the Figure in rp
        axs.fig.text(0.5, 0.04, 'Group', ha='center', va='center')
        axs.fig.text(0.015, 0.5,  type, ha='center', va='center',rotation='vertical')
    if plot:
        plt.show()
    if save==True:
        if id_cross==None:
            path_complete='{path}\Graficos_{type}\{id}\{name_band}_{type}_{id}.png'.format(path=path,name_band=name_band,id=id,type=type)  
        else:
            path_complete='{path}\Graficos_{type}\{id}\{name_band}_{id_cross}_{type}_{id}.png'.format(path=path,name_band=name_band,id=id,type=type,id_cross=id_cross)
        plt.savefig(path_complete)
    plt.close()
    return path_complete
    
def stats_pair(data,metric,space,path,name_band,id,id_cross=None):
    import dataframe_image as dfi
    groups=data['group'].unique()
    combinaciones = list(combinations(groups, 2))
    pruebas={}
    for i in combinaciones:
        a=data.groupby(['database',space]).apply(lambda data:pg.compute_effsize(data[data['group']==i[0]][metric],data[data['group']==i[1]][metric])).to_frame()
        a=a.rename(columns={0:'valores'})
        a['groups']=[i[0]+'-'+i[1]]*len(a)
        a['prueba']=['effsize']*len(a)
        pruebas['effsize-'+i[0]+'-'+i[1]]=a
        #pg.pairwise_gameshowell(data_sl_com,dv)
    table=pd.concat(list(pruebas.values()),axis=0)
    if id_cross==None:
        path_complete='{path}\Graficos_{type}\{id}\{name_band}_{type}_{id}_table.png'.format(path=path,name_band=name_band,id=id,type=metric)  
    else:
        path_complete='{path}\Graficos_{type}\{id}\{name_band}_{id_cross}_{type}_{id}_table.png'.format(path=path,name_band=name_band,id=id,type=metric,id_cross=id_cross)
    dfi.export(table, path_complete)
    return path_complete
        


path=r'C:\Users\valec\OneDrive - Universidad de Antioquia\Resultados_Armonizacion_BD' #Cambia dependieron de quien lo corra

#data loading
data_sl_roi=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_long_sl_roi.feather'.format(path=path))
data_sl_com=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_long_sl_components.feather'.format(path=path))
data_c_roi=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_long_coherence_roi.feather'.format(path=path))
data_c_com=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_long_coherence_components.feather'.format(path=path))
data_e_roi=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_long_entropy_roi.feather'.format(path=path))
data_e_com=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_long_entropy_components.feather'.format(path=path))
data_cr_roi=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_long_crossfreq_roi.feather'.format(path=path))
data_cr_com=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_long_crossfreq_components.feather'.format(path=path))

datos_roi={'SL':data_sl_roi,'Coherence':data_c_roi,'Entropy':data_e_roi,'Cross Frecuency':data_cr_roi}
datos_com={'SL':data_sl_com,'Coherence':data_c_com,'Entropy':data_e_com,'Cross Frecuency':data_cr_com}

bands= data_sl_com['Band'].unique()
bandsm= data_cr_com['M_Band'].unique()

for band in bands:
    for metric in datos_roi.keys():
        d_roi=datos_roi[metric]
        d_banda_roi=d_roi[d_roi['Band']==band]
        d_com=datos_com[metric]
        d_banda_com=d_com[d_com['Band']==band]
        if metric!='Cross Frecuency':       
            graphics(d_banda_roi,metric,path,band,'ROI',num_columns=2,save=True,plot=False)
            graphics(d_banda_com,metric,path,band,'IC',num_columns=4,save=True,plot=False)
        else:
            for bandm in bandsm:   
                if d_banda_roi[d_banda_roi['M_Band']==bandm]['Cross Frequency'].iloc[0]!=0:
                    graphics(d_banda_roi[d_banda_roi['M_Band']==bandm],'Cross Frequency',path,band,'ROI',id_cross=bandm,num_columns=2,save=True,plot=False)
                if d_banda_com[d_banda_com['M_Band']==bandm]['Cross Frequency'].iloc[0]!=0:
                    graphics(d_banda_com[d_banda_com['M_Band']==bandm],'Cross Frequency',path,band,'IC',id_cross=bandm,num_columns=4,save=True,plot=False)
    
    # groups=data_sl_com['group'].unique()
    # combinaciones = list(combinations(groups, 2))
    # pruebas={}
    # for i in combinaciones:
    #     a=data_sl_com.groupby(['database','Component']).apply(lambda data_sl_com:pg.compute_effsize(data_sl_com[data_sl_com['group']==i[0]]['SL'],data_sl_com[data_sl_com['group']==i[1]]['SL'])).to_frame()
    #     a=a.rename(columns={0:'valores'})
    #     a['groups']=[i[0]+'-'+i[1]]*len(a)
    #     a['prueba']=['effsize']*len(a)
    #     pruebas['effsize-'+i[0]+'-'+i[1]]=a
    #     pg.pairwise_gameshowell(data_sl_com,dv)
    # #pd.concat(list(pruebas.values()),axis=1)
    # print(a)
        

print('Graficos SL,coherencia,entropia y cross frequency guardados')