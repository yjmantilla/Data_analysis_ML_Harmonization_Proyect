
import collections
import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

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
            plt.savefig('{path}\Graficos_{type}\{id}\{name_band}_{type}_{id}.png'.format(path=path,name_band=name_band,id=id,type=type))
            plt.close()
        else:
            plt.savefig('{path}\Graficos_{type}\{id}\{name_band}_{id_cross}_{type}_{id}.png'.format(path=path,name_band=name_band,id=id,type=type,id_cross=id_cross))
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
bandsm= data_cr_com['M_Band'].unique()
for band in bands:
    d_banda=data_sl_roi[data_sl_roi['Band']==band]
    d_banda1=data_sl_com[data_sl_com['Band']==band]
    d_banda2=data_c_roi[data_c_roi['Band']==band]
    d_banda3=data_c_com[data_c_com['Band']==band]
    d_banda4=data_e_roi[data_e_roi['Band']==band]
    d_banda5=data_e_com[data_e_com['Band']==band]
    d_banda6=data_cr_roi[data_cr_roi['Band']==band]
    d_banda7=data_cr_com[data_cr_com['Band']==band]
    graphics(d_banda,'SL',path,band,'ROI',num_columns=2,save=True,plot=False)
    graphics(d_banda1,'SL',path,band,'IC',num_columns=4,save=True,plot=False)
    graphics(d_banda2,'Coherence',path,band,'ROI',num_columns=2,save=True,plot=False)
    graphics(d_banda3,'Coherence',path,band,'IC',num_columns=4,save=True,plot=False)
    graphics(d_banda4,'Entropy',path,band,'ROI',num_columns=2,save=True,plot=False)
    graphics(d_banda5,'Entropy',path,band,'IC',num_columns=4,save=True,plot=False)
  
    for bandm in bandsm:   
        if d_banda7[d_banda7['M_Band']==bandm]['Cross Frequency'].iloc[0]!=0:
            graphics(d_banda7[d_banda7['M_Band']==bandm],'Cross Frequency',path,band,'IC',id_cross=bandm,num_columns=4,save=True,plot=False)



print('Graficos SL,coherencia,entropia y cross frequency guardados')