
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
            plt.savefig('{path}\Graficos_{type}\{id}\{name_band}_{type}_{id}.png'.format(path=path,name_band=name_band,id=id,type=type))
            plt.close()
        else:
            plt.savefig('{path}\Graficos_{type}\{id}\{name_band}_{id_cross}_{type}_{id}.png'.format(path=path,name_band=name_band,id=id,type=type,id_cross=id_cross))
            plt.close()
    print('Done!')
    return

def fig2img(fig):
      """
  Convert a Matplotlib figure to a PIL Image and return it
  """
  buf = io.BytesIO()
  fig.savefig(buf)
  buf.seek(0)
  img = Image.open(buf)
  return img

def createCollage(imageList, frame_width, images_per_row,save_path,name_graphic,carpeta,tipo,grupo,show=False):
    try:
        path="{save_path}\{carpeta}\{tipo}".format(save_path=save_path,carpeta=carpeta,tipo=tipo).replace('\\','/')
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    imageList=[fig2img(x) for x in imageList] 
    img_width, img_height = getSize(imageList)
    #scaling factor
    sf = (frame_width-(images_per_row-1))/(images_per_row*img_width)

    scaled_img_width =int(ceil(img_width*sf))
    scaled_img_height =int(ceil(img_height*sf))

    number_of_rows = int(ceil(len(imageList)/images_per_row))
    frame_height = int(ceil(sf*img_height*number_of_rows))

    new_im = Image.new('RGB', (frame_width, frame_height),'white')

    i,j=0,0
    for num, im in enumerate(imageList):
        if num%images_per_row==0:
            i=0
        
        #resizing opened image
        im.thumbnail((scaled_img_width,scaled_img_height))
        #Iterate through a 3 x 3 grid
        y_cord = (j//images_per_row)*scaled_img_height
        y_cord=int(y_cord)
        new_im.paste(im, (i,y_cord))
        # print(i, y_cord)
        i=(i+scaled_img_width)
        j+=1
    if show:
        new_im.show()
    new_im.save('{save_path}\{carpeta}\{tipo}\{name_graphic}_{tipo}_{grupo}.png'.format(save_path=save_path,name_graphic=name_graphic,carpeta=carpeta,tipo=tipo,grupo=grupo), "PNG")
    return new_im


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