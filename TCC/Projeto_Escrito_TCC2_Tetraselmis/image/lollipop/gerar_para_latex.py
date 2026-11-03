from pathlib import Path
import pandas as pd,numpy as np,json,shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import MaxNLocator
from fontTools.ttLib import TTFont
source=Path(__file__).resolve().parents[2]/'graficos_lollipop/matriz_FEB_utilizada.csv'
out=Path(__file__).parent;out.mkdir(exist_ok=True)
fontfile=Path(__file__).resolve().parents[2]/'graficos_lollipop/fonts/Times.TTF';font=FontProperties(fname=str(fontfile),size=12)
plt.rcParams.update({'pdf.fonttype':42,'axes.unicode_minus':False})
colors={'Comercial':'#003B66','Tetraselmis':'#941B35'}
targets={'1GKC':'Gelatinase B humana / MMP-9','1H1B':'Elastase de neutrófilos humanos','1HFC':'Colagenase humana / MMP-1','2PE4':'Hialuronidase humana 1','5M8P':'TYRP1 humana','8H78':'Gelatinase A humana / MMP-2'}
def label(s):
 if s.startswith('D-Gulose'):return 'D-gulose'
 if s.startswith('Dha'):return 'Dha'
 if s.startswith('KDO'):return 'KDO'
 if s.startswith('alpha'):return 'α-Kdo'
 return s.replace('_',' ').replace('Acido','Ácido').replace('Ascorbico','ascórbico').replace('Kojico','kójico').replace('Ferulico','ferúlico').replace('Galico','gálico').replace('Galacturonico','galacturônico').replace('Glucuronico','glucurônico')
df=pd.read_csv(source);assert df.FEB_kcal_mol.notna().sum()==204
for receptor,rows in df.groupby('Receptor'):
 code=receptor[:4];rows=rows.sort_values(['FEB_kcal_mol','Ligante'],kind='stable').copy();assert len(rows)==34
 rows['Nome_no_grafico']=rows.Ligante.map(label);x=rows.FEB_kcal_mol.to_numpy();y=np.arange(34);cs=[colors[g] for g in rows.Grupo]
 fig=plt.figure(figsize=(16/2.54,20.5/2.54));ax=fig.add_axes([.285,.075,.685,.91]);ax.set_axisbelow(True)
 ax.hlines(y,x,0,color=cs,lw=1.4,alpha=.85);ax.scatter(x,y,c=cs,s=34,zorder=3)
 ax.set_ylim(33.8,-.8);limit=np.floor(x.min())-max(.3,(0-x.min())*.04);ax.set_xlim(max(.3,(0-x.min())*.03),np.floor(x.min())-max(.5,(0-x.min())*.15));ax.set_yticks(y,list(rows.Nome_no_grafico));ax.tick_params(axis='y',length=0,pad=5)
 ax.xaxis.set_major_locator(MaxNLocator(nbins=8,integer=True));ax.grid(axis='x',color='#dddddd',lw=.7);ax.grid(axis='y',color='#e4e4e4',lw=.6);ax.axvline(0,color='#777777',lw=1)
 for side in ['left','top','right']:ax.spines[side].set_visible(False)
 ax.spines['bottom'].set_color('#bbbbbb')
 for t in ax.get_xticklabels()+ax.get_yticklabels():t.set_fontproperties(font)
 for yi,xi in zip(y,x):ax.annotate(f'{xi:.3f}'.replace('.',','),(xi,yi),xytext=(6,0),textcoords='offset points',va='center',fontproperties=font)
 ax.set_xlabel('FEB (kcal/mol)',fontproperties=font,labelpad=8)
 handles=[Line2D([0],[0],color=colors['Comercial'],marker='o',lw=1.4,label='Comerciais'),Line2D([0],[0],color=colors['Tetraselmis'],marker='o',lw=1.4,label='SPE da Tetraselmis')]
 fig.canvas.draw();renderer=fig.canvas.get_renderer()
 for text in ax.get_yticklabels():
  bbox=text.get_window_extent(renderer);assert bbox.x0>=0,(code,text.get_text())
 for ext in ['pdf','png']:
  fig.savefig(out/f'lollipop_{code}.{ext}',dpi=300,facecolor='white')
 plt.close(fig);rows[['Receptor','Grupo','Ligante','Nome_no_grafico','FEB_kcal_mol','Origem_FEB']].to_csv(out/f'dados_lollipop_{code}.csv',index=False,encoding='utf-8-sig')
 print(code,len(rows),'ligantes',flush=True)
(out/'fonts').mkdir(exist_ok=True)
if fontfile.resolve()!=(out/'fonts/Times.TTF').resolve():shutil.copy2(fontfile,out/'fonts/Times.TTF')
if source.resolve()!=(out/'matriz_FEB_utilizada.csv').resolve():shutil.copy2(source,out/'matriz_FEB_utilizada.csv')
(out/'LEIA_ME.md').write_text('''# Gráficos lollipop de FEB

Seis receptores, 34 ligantes por receptor, menor FEB por combinação conforme a consolidação atual do trabalho. L2U/2PE4: valor preservado −2,427 kcal/mol. 1H1B comercial: resultados com coordenadas corrigidas. 2PE4, SPE e demais receptores: valores preservados.

Cores do trabalho escrito: comerciais #003B66; SPE da Tetraselmis #941B35. Ordenação pela FEB crescente, da mais negativa para a menos negativa. Empates: nome do ligante. Valores apresentados com três casas decimais. Nomes longos abreviados, com correspondência nos CSVs. PDFs vetoriais e PNGs a 300 dpi, fonte Times New Roman. FEB é pontuação de docking; diferenças nos protocolos limitam comparações diretas entre grupos.

Os gráficos também integram o documento escrito. O visual acompanha os lollipops de interações: hastes partem do zero à esquerda, com valores negativos de FEB à direita; os valores e a ordenação foram preservados.
''')
