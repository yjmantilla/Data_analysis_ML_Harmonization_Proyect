import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

path=r'C:\Users\valec\OneDrive - Universidad de Antioquia\Resultados_Armonizacion_BD' 

def graphic_roi(data,path,name_band,id,num_columns=4,save=True,plot=True):
    '''Function to make the graphs of the powers by ROIs'''
    max=data['Power'].max()
    sns.set(rc={'figure.figsize':(15,12)})
    sns.set_theme(style="white")
    axs=sns.catplot(x='group',y="Power",data=data,hue='database',dodge=True, kind="box",col='ROI',col_wrap=num_columns,palette='winter_r',fliersize=1.5,linewidth=0.5,legend=False)
    plt.yticks(np.arange(0,round(max),0.1))
    axs.set(xlabel=None)
    axs.set(ylabel=None)
    axs.fig.suptitle('Relative '+r'$\bf{'+name_band+r'}$'+ ' power in the ROIs of normalized data given by the databases ')
    axs.add_legend(loc='upper right',bbox_to_anchor=(.7,.95),ncol=4,title="Database")

    axs.fig.subplots_adjust(top=0.85,bottom=0.121, right=0.986,left=0.06, hspace=0.138, wspace=0.062) # adjust the Figure in rp
    axs.fig.text(0.5, 0.04, 'Group', ha='center', va='center')
    axs.fig.text(0.015, 0.5,  'Relative powers', ha='center', va='center',rotation='vertical')
    if plot:
        plt.show()
    if save==True:
        plt.savefig('{path}\Graficos_Potencia_Rois\{name_band}_Rois_{id}.png'.format(name_band=name_band,id=id,path=path))
        plt.close()
    
    return 


def graphic_component(data,path,name_band,id,num_columns=4,save=True,plot=True):
    '''Function to make the graphs of the powers by independent components'''
    max=data['Power'].max()
    sns.set(rc={'figure.figsize':(15,12)})
    sns.set_theme(style="white")
    axs=sns.catplot(x='group',y="Power",data=data,hue='database',dodge=True, kind="box",col='Component',col_wrap=num_columns,palette='winter_r',fliersize=1.5,linewidth=0.5,legend=False)
    plt.yticks(np.arange(0,round(max),0.1))
    axs.set(xlabel=None)
    axs.set(ylabel=None)
    axs.fig.suptitle('Relative '+r'$\bf{'+name_band+r'}$'+ ' power in the components of normalized data given by the databases ')
    axs.add_legend(loc='upper right',bbox_to_anchor=(.59,.95),ncol=4,title="Database")

    axs.fig.subplots_adjust(top=0.85,bottom=0.121, right=0.986,left=0.05, hspace=0.138, wspace=0.062) # adjust the Figure in rp
    axs.fig.text(0.5, 0.04, 'Group', ha='center', va='center')
    axs.fig.text(0.01, 0.5,  'Relative powers', ha='center', va='center',rotation='vertical')
    if plot:
        plt.show()
    if save==True:
        plt.savefig('{path}\Graficos_Potencia_Componentes\{name_band}_Components_{id}.png'.format(name_band=name_band,id=id,path=path))
        plt.close()
    
    return 


#data loading
data_Comp=pd.read_feather(r"{path}\Datosparaorganizardataframes\Datos_componentes_formatolargo_filtrados.feather".format(path=path))#Datos con sujetos sin datos vacios
data_Comp1=pd.read_feather(r"{path}\Datosparaorganizardataframes\Datos_componentes_formatolargo_filtrados_sin_atipicos.feather".format(path=path))#Datos con sujetos sin datos vacios

bands= data_Comp['Band'].unique()

#graphs by frequency bands
for band in bands:
    d_banda=data_Comp[data_Comp['Band']==band]
    d_banda1=data_Comp1[data_Comp1['Band']==band]
    graphic_component(d_banda,path,band,'con datos atipicos',num_columns=4,save=True,plot=False)
    #graphic_component(d_banda1,path,band,'sin datos atipicos',num_columns=4,save=True,plot=False)

print('Graficos Componentes guardados')

#data loading
data_roi=pd.read_feather(r'{path}\Datosparaorganizardataframes\Datos_ROI_formatolargo_filtrados.feather'.format(path=path))
data_roi1=pd.read_feather(r'{path}\Datosparaorganizardataframes\Datos_ROI_formatolargo_filtrados_sin_atipicos.feather'.format(path=path))

bands= data_roi['Band'].unique()

#graphs by frequency bands
for band in bands:
    d_banda=data_roi[data_roi['Band']==band]
    d_banda1=data_roi1[data_roi1['Band']==band]
    graphic_roi(d_banda,path,band,'condatosatipicos',num_columns=2,save=True,plot=False)
    #graphic_roi(d_banda1,path,band,'sindatosatipicos',num_columns=2,save=True,plot=False)


print('Graficos Rois guardados')