from pathlib import Path
import pandas as pd,numpy as np,hashlib,json,shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import MaxNLocator
project=Path('/home/osvaldinojunior/Documents/PFC_1/part_2_PFC/Projeto_Escrito_TCC2_Tetraselmis__')
base=Path('/home/osvaldinojunior/Desktop/tcc_2/resultados_5/resultados_4/análises/tetra_e_comerciais/interacoes');out=Path(__file__).parent;out.mkdir(exist_ok=True)
fontfile=project/'graficos_lollipop/fonts/Times.TTF';font=FontProperties(fname=str(fontfile),size=12)
colors={'Comercial':'#003B66','Tetraselmis':'#941B35'};targets={'1GKC':'Gelatinase B humana / MMP-9','1H1B':'Elastase de neutrófilos humanos','1HFC':'Colagenase humana / MMP-1','2PE4':'Hialuronidase humana 1','5M8P':'TYRP1 humana','8H78':'Gelatinase A humana / MMP-2'}
plt.rcParams.update({'pdf.fonttype':42,'axes.unicode_minus':False})
def label(s):
 if s.startswith('D-Gulose'):return 'D-gulose'
 if s.startswith('Dha'):return 'Dha'
 if s.startswith('KDO'):return 'KDO'
 if s.startswith('alpha'):return 'α-Kdo'
 return s.replace('_',' ').replace('Acido','Ácido').replace('Ascorbico','ascórbico').replace('Kojico','kójico').replace('Ferulico','ferúlico').replace('Galico','gálico').replace('Galacturonico','galacturônico').replace('Glucuronico','glucurônico')
allrows=[];provenance=[]
for code,title in targets.items():
 source=next(base.glob(code+'*/interacoes_*.xlsx'));d=pd.read_excel(source,sheet_name='Matriz_interacoes');assert len(d)==34
 presence=d.iloc[:,4:].eq('X');counts=presence.sum(axis=1)
 rows=pd.DataFrame({'Receptor':code,'Ligante':d.Ligante,'Nome_no_grafico':d.Ligante.map(label),'Grupo':d.Grupo,'Residuos_distintos':counts,'Residuos_com_interacao':['; '.join(presence.columns[row]) for row in presence.to_numpy(bool)]})
 assert rows.Grupo.value_counts().to_dict()=={'Comercial':17,'Tetraselmis':17}
 rows=rows.sort_values(['Residuos_distintos','Ligante'],ascending=[False,True],kind='stable');allrows.append(rows);rows.to_csv(out/f'dados_interacoes_{code}.csv',index=False,encoding='utf-8-sig')
 d.to_csv(out/f'matriz_origem_{code}.csv',index=False,encoding='utf-8-sig');provenance.append({'receptor':code,'arquivo':str(source),'SHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'ligantes':34,'residuos_no_mapa':presence.shape[1],'presencas':int(counts.sum())})
 y=np.arange(34);x=rows.Residuos_distintos.to_numpy();cs=[colors[g] for g in rows.Grupo]
 fig=plt.figure(figsize=(8.27,11.69));ax=fig.add_axes([.285,.075,.685,.80]);ax.set_axisbelow(True);ax.hlines(y,0,x,color=cs,lw=1.4,alpha=.85);ax.scatter(x,y,c=cs,s=34,zorder=3)
 ax.set_ylim(33.8,-.8);ax.set_xlim(-.4,max(1,x.max())*1.15+.5);ax.set_yticks(y,list(rows.Nome_no_grafico));ax.tick_params(axis='y',length=0,pad=5);ax.xaxis.set_major_locator(MaxNLocator(nbins=8,integer=True));ax.grid(axis='x',color='#dddddd',lw=.7);ax.grid(axis='y',color='#e4e4e4',lw=.6);ax.axvline(0,color='#777777',lw=1)
 for side in ['left','top','right']:ax.spines[side].set_visible(False)
 ax.spines['bottom'].set_color('#bbbbbb')
 for t in ax.get_xticklabels()+ax.get_yticklabels():t.set_fontproperties(font)
 for yi,xi in zip(y,x):ax.annotate(str(xi),(xi,yi),xytext=(6,0),textcoords='offset points',va='center',fontproperties=font)
 ax.set_xlabel('Resíduos de aminoácidos distintos com interação',fontproperties=font,labelpad=8)
 fig.text(.5,.96,title+'\n'+code,ha='center',va='top',fontproperties=FontProperties(fname=str(fontfile),size=14))
 handles=[Line2D([0],[0],color=colors['Comercial'],marker='o',lw=1.4,label='Comerciais'),Line2D([0],[0],color=colors['Tetraselmis'],marker='o',lw=1.4,label='SPE da Tetraselmis')];fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.5,.91),ncol=2,frameon=False,prop=font)
 fig.canvas.draw();renderer=fig.canvas.get_renderer()
 for t in ax.get_yticklabels()+[ax.xaxis.label]:
  b=t.get_window_extent(renderer);assert b.x0>=0 and b.x1<=fig.bbox.x1,(code,t.get_text())
 for ext in ['pdf','png']:fig.savefig(out/f'lollipop_interacoes_{code}.{ext}',dpi=300,facecolor='white')
 plt.close(fig);print(code,'contagens',int(x.min()),'a',int(x.max()),flush=True)
pd.concat(allrows).to_excel(out/'residuos_distintos_por_ligante.xlsx',index=False)
(out/'origem_dados.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2))
(out/'LEIA_ME.md').write_text('''# Lollipops de interações por ligante

Seis receptores; 34 ligantes por receptor. Cada ponto indica quantos resíduos de aminoácidos distintos apresentam contato com o ligante na matriz de presença utilizada no trabalho. Um mesmo resíduo é contado uma vez por ligante, independentemente do número ou tipo de contatos. Resíduos com números ou cadeias diferentes permanecem distintos. Não corresponde à soma dos registros individuais de interação do PLIP nem ao número de tipos de aminoácido.

Os seis mapas atuais utilizam as matrizes preservadas, incluindo 1H1B e 2PE4 conforme solicitado. A origem e os hashes estão em origem_dados.json. CSVs incluem a lista dos resíduos de cada ligante; a planilha reúne as 204 contagens.

Ordem decrescente pelo número de resíduos; empates por nome do ligante. Azul #003B66 para comerciais; vinho #941B35 para SPE da Tetraselmis. Fonte Times New Roman, PDFs vetoriais e PNGs a 300 dpi. Contagem maior não demonstra maior afinidade ou potência inibitória. Os gráficos também foram inseridos no documento escrito, nas seções dos respectivos receptores.
''')

