
import collections
import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def graphic_sl(data,name_band,id,num_columns=4, save=True,plot=True):
    max=data['SL'].max()
    sns.set(rc={'figure.figsize':(15,12)})
    sns.set_theme(style="white")
    axs=sns.catplot(x='group',y="SL",data=data,hue='database',dodge=True, kind="box",col='ROI',col_wrap=num_columns,palette='winter_r',fliersize=1.5,linewidth=0.5,legend=False)
    #plt.yticks(np.arange(0,round(max),0.1))
    axs.set(xlabel=None)
    axs.set(ylabel=None)
    axs.fig.suptitle('SL in '+r'$\bf{'+name_band+r'}$'+ ' in the ROIs of normalized data given by the databases ')
    axs.add_legend(loc='upper right',bbox_to_anchor=(.7,.95),ncol=4,title="Database")

    axs.fig.subplots_adjust(top=0.85,bottom=0.121, right=0.986,left=0.06, hspace=0.138, wspace=0.062) # adjust the Figure in rp
    axs.fig.text(0.5, 0.04, 'Group', ha='center', va='center')
    axs.fig.text(0.015, 0.5,  'SL', ha='center', va='center',rotation='vertical')
    if plot:
        plt.show()
    if save==True:
        plt.savefig('Manipulacion- Rois-Componentes de todas las DB\GraficosSL\{name_band}_SL_{id}.png'.format(name_band=name_band,id=id))
        plt.close()
    
    return 

def graphic_coherence(data,name_band,id, save=True,plot=True):
    max=data['Coherence'].max()
    sns.set(rc={'figure.figsize':(15,12)})
    sns.set_theme(style="white")
    axs=sns.catplot(x='group',y="Coherence",data=data,hue='database',dodge=True, kind="box",palette='winter_r',fliersize=1.5,linewidth=0.5,legend=False)
    #plt.yticks(np.arange(0,round(max),0.1))
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
        plt.savefig('Manipulacion- Rois-Componentes de todas las DB\GraficosCoherencia\{name_band}_Coherence_{id}.png'.format(name_band=name_band,id=id))
        plt.close()
    
    return 

def graphic_entropy(data,name_band,id, save=True,plot=True):
    #max=data['Entropy'].max()
    sns.set(rc={'figure.figsize':(15,12)})
    sns.set_theme(style="white")
    axs=sns.catplot(x='group',y="Entropy",data=data,hue='database',dodge=True, kind="box",palette='winter_r',fliersize=1.5,linewidth=0.5,legend=False)
    #plt.yticks(np.arange(0,round(max),0.1))
    axs.set(xlabel=None)
    axs.set(ylabel=None)
    axs.fig.suptitle('Entropy in '+r'$\bf{'+name_band+r'}$'+ ' of normalized data given by the databases ')
    axs.add_legend(loc='upper right',bbox_to_anchor=(0.8,0.94),ncol=4,title="Database")

    axs.fig.subplots_adjust(top=0.85,bottom=0.121, right=0.986,left=0.06, hspace=0.138, wspace=0.062) # adjust the Figure in rp
    axs.fig.text(0.5, 0.04, 'Group', ha='center', va='center')
    axs.fig.text(0.015, 0.5,  'Entropy', ha='center', va='center',rotation='vertical')
    if plot:
        plt.show()
    if save==True:
        plt.savefig('Manipulacion- Rois-Componentes de todas las DB\GraficosEntropia\{name_band}_Entropia_{id}.png'.format(name_band=name_band,id=id))
        plt.close()
    
    return 

F = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8'] 
T = ['FT7', 'FC5', 'FC6', 'FT8', 'T7', 'C5', 'C6', 'T8', 'TP7', 'CP5', 'CP6', 'TP8']
C = ['FC3', 'FC1', 'FCZ', 'FC2', 'FC4', 'C3', 'C1', 'CZ', 'C2', 'C4', 'CP3', 'CP1', 'CPZ', 'CP2', 'CP4'] 
PO = ['P7', 'P5', 'P3', 'P1', 'PZ', 'P2', 'P4', 'P6', 'P8', 'PO7', 'PO5', 'PO3', 'POZ', 'PO4', 'PO6', 'PO8', 'CB1', 'O1', 'OZ', 'O2', 'CB2']
rois = [F,C,PO,T]
roi_labels = ['F','C','PO','T']

#se cargan los datos para hacer los graficos
data_sl_roi=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_para_graficos_SL_desdeunionpotencias_roi.feather')
data_sl_com=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_para_graficos_SL_desdeunionpotencias_Componentes.feather')
data_c_roi=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_para_graficos_COHERENCE_desdeunionpotencias_roi.feather')
data_c_com=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_para_graficos_COHERENCE_desdeunionpotencias_componentes.feather')
data_e_roi=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_para_graficos_ENTROPY_desdeunionpotencias_roi.feather')
data_e_com=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_para_graficos_ENTROPY_desdeunionpotencias_componentes.feather')

bands= data_sl_com['Band'].unique()
for band in bands:
    d_banda=data_sl_roi[data_sl_roi['Band']==band]
    d_banda1=data_sl_com[data_sl_com['Band']==band]
    d_banda2=data_c_roi[data_c_roi['Band']==band]
    d_banda3=data_c_com[data_c_com['Band']==band]
    d_banda4=data_e_roi[data_e_roi['Band']==band]
    d_banda5=data_e_com[data_e_com['Band']==band]
    graphic_sl(d_banda,band,'desderoi',num_columns=2,save=True,plot=False)
    graphic_sl(d_banda1,band,'desdecomponentes',num_columns=2,save=True,plot=False)
    graphic_coherence(d_banda2,band,'desderoi',save=True,plot=False)
    graphic_coherence(d_banda3,band,'desdecomponentes',save=True,plot=False)
    graphic_entropy(d_banda4,band,'desderoi',save=True,plot=False)
    graphic_entropy(d_banda5,band,'desdecomponentes',save=True,plot=False)


print('Graficos SL y coherencia guardados')