
import collections
import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def graphics(data,type,path,name_band,id,num_columns=4, save=True,plot=True):
    '''Function to make graphs of the given data '''
    max=data[type].max()
    sns.set(rc={'figure.figsize':(15,12)})
    sns.set_theme(style="white")
    axs=sns.catplot(x='group',y=type,data=data,hue='database',dodge=True, kind="box",col='ROI',col_wrap=num_columns,palette='winter_r',fliersize=1.5,linewidth=0.5,legend=False)
    plt.yticks(np.arange(0,round(max),0.1))
    axs.set(xlabel=None)
    axs.set(ylabel=None)
    if type=='Cross_Frequency':
        type1='Cross Frequency'
    else:
        type1=type

    axs.fig.suptitle(type1+' in '+r'$\bf{'+name_band+r'}$'+ ' in the ROIs of normalized data given by the databases')
    axs.add_legend(loc='upper right',bbox_to_anchor=(.7,.95),ncol=4,title="Database")

    axs.fig.subplots_adjust(top=0.85,bottom=0.121, right=0.986,left=0.06, hspace=0.138, wspace=0.062) # adjust the Figure in rp
    axs.fig.text(0.5, 0.04, 'Group', ha='center', va='center')
    if type=='Cross_Frequency':
        axs.fig.text(0.015, 0.5,  'Cross Frequency', ha='center', va='center',rotation='vertical')
    else:
        axs.fig.text(0.015, 0.5,  type, ha='center', va='center',rotation='vertical')
    if plot:
        plt.show()
    if save==True:
        plt.savefig('{path}\Graficos_{type}\{name_band}_{type}_{id}.png'.format(path=path,name_band=name_band,id=id,type=type))
        plt.close()
    
    return 

def graphic_coherence(data,path,name_band,id, save=True,plot=True):
    '''Function to make graphs of coherence'''
    max=data['Coherence'].max()
    sns.set(rc={'figure.figsize':(15,12)})
    sns.set_theme(style="white")
    axs=sns.catplot(x='group',y="Coherence",data=data,hue='database',dodge=True, kind="box",palette='winter_r',fliersize=1.5,linewidth=0.5,legend=False)
    plt.yticks(np.arange(0,round(max),0.1))
    axs.set(xlabel=None)
    axs.set(ylabel=None)
    axs.fig.suptitle('Coherence in '+r'$\bf{'+name_band+r'}$'+ ' of normalized data given by the databases ')
    axs.add_legend(loc='upper right',bbox_to_anchor=(0.8,0.94),ncol=4,title="Database")

    axs.fig.subplots_adjust(top=0.85,bottom=0.121, right=0.986,left=0.06, hspace=0.138, wspace=0.062) # adjust the Figure in rp
    axs.fig.text(0.5, 0.04, 'Group', ha='center', va='center')
    axs.fig.text(0.015, 0.5,  'Coherence', ha='center', va='center',rotation='vertical')
    if plot:
        plt.show()
    if save==True:
        plt.savefig('{path}\Graficos_Coherencia\{name_band}_Coherence_{id}.png'.format(path=path,name_band=name_band,id=id))
        plt.close()
    
    return 


path=r'C:\Users\valec\OneDrive - Universidad de Antioquia\Resultados_Armonizacion_BD' #Cambia dependieron de quien lo corra

#data loading
data_sl_roi=pd.read_feather(r'{path}\Datosparaorganizardataframes\Datos_para_graficos_SL_desdeunionpotencias_roi.feather'.format(path=path))
data_sl_com=pd.read_feather(r'{path}\Datosparaorganizardataframes\Datos_para_graficos_SL_desdeunionpotencias_Componentes.feather'.format(path=path))
data_c_roi=pd.read_feather(r'{path}\Datosparaorganizardataframes\Datos_para_graficos_COHERENCE_desdeunionpotencias_roi.feather'.format(path=path))
data_c_com=pd.read_feather(r'{path}\Datosparaorganizardataframes\Datos_para_graficos_COHERENCE_desdeunionpotencias_componentes.feather'.format(path=path))
data_e_roi=pd.read_feather(r'{path}\Datosparaorganizardataframes\Datos_para_graficos_ENTROPY_desdeunionpotencias_roi.feather'.format(path=path))
data_e_com=pd.read_feather(r'{path}\Datosparaorganizardataframes\Datos_para_graficos_ENTROPY_desdeunionpotencias_componentes.feather'.format(path=path))
data_cr_roi=pd.read_feather(r'{path}\Datosparaorganizardataframes\Datos_para_graficos_CROSS_Frequency_desdeunionpotencias_roi.feather'.format(path=path))
data_cr_com=pd.read_feather(r'{path}\Datosparaorganizardataframes\Datos_para_graficos_CROSS_Frequency_desdeunionpotencias_components.feather'.format(path=path))


bands= data_sl_com['Band'].unique()
for band in bands:
    d_banda=data_sl_roi[data_sl_roi['Band']==band]
    d_banda1=data_sl_com[data_sl_com['Band']==band]
    d_banda2=data_c_roi[data_c_roi['Band']==band]
    d_banda3=data_c_com[data_c_com['Band']==band]
    d_banda4=data_e_roi[data_e_roi['Band']==band]
    d_banda5=data_e_com[data_e_com['Band']==band]
    d_banda6=data_cr_roi[data_cr_roi['Band']==band]
    d_banda7=data_cr_com[data_cr_com['Band']==band]
    graphics(d_banda,'SL',path,band,'desderoi',num_columns=2,save=True,plot=False)
    graphics(d_banda1,'SL',path,band,'desdecomponentes',num_columns=2,save=True,plot=False)
    graphic_coherence(d_banda2,path,band,'desderoi',save=True,plot=False)
    graphic_coherence(d_banda3,path,band,'desdecomponentes',save=True,plot=False)
    graphics(d_banda4,'Entropy',path,band,'desderoi',num_columns=2,save=True,plot=False)
    graphics(d_banda5,'Entropy',path,band,'desdecomponentes',num_columns=2,save=True,plot=False)
    graphics(d_banda6,'Cross_Frequency',path,band,'desderoi',num_columns=2,save=True,plot=False)
    graphics(d_banda7,'Cross_Frequency',path,band,'desdecomponentes',num_columns=2,save=True,plot=False)


print('Graficos SL,coherencia,entropia y cross frequency guardados')