"""Gera as tabelas LaTeX e as figuras que faltavam para o artigo.

Reproduz exatamente a logica do homework1.ipynb (mesmas colunas, mesmo
descarte de Patient_ID e Diabetes_Risk_Score, mesmo dropna antes do PCA)
e escreve:

  paper/tabelas/*.tex   fragmentos \\input-aveis pelo main.tex
  figuras/*.png         histogramas e box-plots que o notebook so mostrava

Rodar da raiz do repositorio:  python paper/gerar_tabelas.py
"""

import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_TABELAS = os.path.join(RAIZ, 'paper', 'tabelas')
DIR_FIGURAS = os.path.join(RAIZ, 'figuras')
os.makedirs(DIR_TABELAS, exist_ok=True)
os.makedirs(DIR_FIGURAS, exist_ok=True)

CLASSE = 'Diabetes_Risk'
SAIDA = 'Diabetes_Risk_Score'
ORDEM_CLASSES = ['Low', 'Moderate', 'High']
CORES = {'Low': 'tab:green', 'Moderate': 'tab:orange', 'High': 'tab:red'}


def rotulo(nome):
    """Nome de coluna -> rotulo legivel na tabela."""
    return nome.replace('_', ' ')


def escreve(nome_arquivo, linhas):
    """Grava um fragmento de tabela LaTeX.

    A ultima linha sai SEM o '\\\\' final de propriedade: o \\input do
    LaTeX expande para '\\@@input <arquivo>\\relax', e esse \\relax
    depois de um '\\\\' abre uma celula nova, o que faz o \\midrule ou
    \\bottomrule seguinte virar 'Misplaced \\noalign'. Quem fecha a
    ultima linha e o '\\\\' escrito no main.tex logo apos o \\input.
    """
    caminho = os.path.join(DIR_TABELAS, nome_arquivo)
    corpo = '\n'.join(linhas)
    if corpo.rstrip().endswith('\\\\'):
        corpo = corpo.rstrip()[:-2].rstrip()
    with open(caminho, 'w', encoding='utf-8') as arquivo:
        arquivo.write(corpo + '\n')
    print('  escrito', os.path.relpath(caminho, RAIZ))


# ---------------------------------------------------------------- dados
df = pd.read_csv(os.path.join(RAIZ, 'dataset',
                              'diabetes_risk_prediction_dataset.csv'))

preditores_base = df.drop(columns=[SAIDA])
quantitativos = (preditores_base
                 .select_dtypes(include=['int', 'float'])
                 .drop(columns=['Patient_ID']))
qualitativos = preditores_base[['Country', 'Gender']]
preditores = pd.concat([quantitativos, qualitativos, df[CLASSE]], axis=1)

N = len(preditores)
D = preditores.shape[1] - 1
L = preditores[CLASSE].nunique()
print('N = %d, D = %d, L = %d, quantitativos = %d'
      % (N, D, L, quantitativos.shape[1]))


# -------------------------------------------- Tabela I: classes e faltantes
contagem = preditores[CLASSE].value_counts()
linhas = ['%s & %s & %.2f\\%% \\\\'
          % (c, format(int(contagem[c]), ',d').replace(',', '{,}'),
             100 * contagem[c] / N)
          for c in ['High', 'Moderate', 'Low']]
escreve('classdist.tex', linhas)

faltantes = quantitativos.isna().sum()
faltantes = faltantes[faltantes > 0].sort_values(ascending=False)
linhas = ['%s & %s \\\\' % (rotulo(nome),
                            format(int(qtd), ',d').replace(',', '{,}'))
          for nome, qtd in faltantes.items()]
escreve('missing.tex', linhas)
print('  preditores com faltante:', len(faltantes),
      '| com exatamente 1000:', int((faltantes == 1000).sum()))


# ------------------------------------- Tabela II: estatisticas incondicionais
incondicional = pd.DataFrame({
    'media': quantitativos.mean(),
    'desvio': quantitativos.std(),
    'assimetria': quantitativos.skew(),
    'curtose': quantitativos.kurtosis(),
    'minimo': quantitativos.min(),
    'maximo': quantitativos.max(),
})
linhas = ['%s & %.2f & %.2f & %+.3f & %+.3f & %.1f--%.1f \\\\'
          % (rotulo(nome), linha['media'], linha['desvio'],
             linha['assimetria'], linha['curtose'],
             linha['minimo'], linha['maximo'])
          for nome, linha in incondicional.iterrows()]
escreve('uncond.tex', linhas)

# A curtose excedente de uma uniforme e -6/5 = -1.2. Se quase todos os
# preditores caem nesse valor, eles foram amostrados de uniformes.
proximos_uniforme = (incondicional['curtose'] < -1.15).sum()
print('  preditores com curtose < -1.15 (assinatura de uniforme): %d de %d'
      % (proximos_uniforme, len(incondicional)))
print('  curtose do BMI: %+.3f (unica excecao)'
      % incondicional.loc['BMI', 'curtose'])


# ------------------------ Tabela III: poder discriminativo + medias por classe
estatisticas = preditores.groupby(CLASSE)[list(quantitativos.columns)] \
                         .agg(['mean', 'std', 'skew'])
medias = estatisticas.xs('mean', axis=1, level=1).T[ORDEM_CLASSES]
delta = ((medias.max(axis=1) - medias.min(axis=1)) / quantitativos.std()) \
    .sort_values(ascending=False)

linhas = []
for nome in delta.index:
    valor = delta[nome]
    formato = '%.3f' if valor < 0.1 else '%.2f'
    linhas.append('%s & %.2f & %.2f & %.2f & %s \\\\'
                  % (rotulo(nome), medias.loc[nome, 'Low'],
                     medias.loc[nome, 'Moderate'], medias.loc[nome, 'High'],
                     formato % valor))
escreve('discrim.tex', linhas)

# medias condicionais completas (apendice, se couber)
escreve('cond_full.tex',
        ['%s & %.2f & %.2f & %.2f \\\\'
         % (rotulo(n), medias.loc[n, 'Low'],
            medias.loc[n, 'Moderate'], medias.loc[n, 'High'])
         for n in quantitativos.columns])


# ---------------------------------------------------- correlacoes de interesse
correlacao = quantitativos.corr()
pares = [('BMI', 'Weight_kg'), ('BMI', 'Height_cm'),
         ('HbA1c', 'Fasting_Blood_Sugar'), ('HbA1c', 'Blood_Glucose'),
         ('Fasting_Blood_Sugar', 'Blood_Glucose')]
print('\ncorrelacoes citadas no texto:')
for a, b in pares:
    print('  rho(%s, %s) = %+.3f' % (a, b, correlacao.loc[a, b]))

fora_diagonal = correlacao.where(~np.eye(len(correlacao), dtype=bool))
print('  |rho| maximo fora da diagonal: %.3f'
      % fora_diagonal.abs().max().max())
print('  |rho| mediano fora da diagonal: %.4f'
      % fora_diagonal.abs().stack().median())


# ------------------------------------------------------ Tabela IV: autovalores
dados_pca = quantitativos.dropna()
print('\nPCA: %d linhas antes do dropna, %d depois (%.1f%% descartado)'
      % (len(quantitativos), len(dados_pca),
         100 * (1 - len(dados_pca) / len(quantitativos))))

padronizados = (dados_pca - dados_pca.mean()) / dados_pca.std()
covariancia = (padronizados.T @ padronizados) / (len(padronizados) - 1)
autovalores, autovetores = np.linalg.eigh(covariancia)
ordem = np.argsort(autovalores)[::-1]
autovalores = autovalores[ordem]
autovetores = autovetores[:, ordem]

total = autovalores.sum()
explicada = autovalores / total
acumulada = np.cumsum(explicada)
print('  variancia explicada por PC1+PC2: %.4f' % acumulada[1])
print('  autovalores:', np.round(autovalores, 4))

linhas = []
for i in [0, 1, 2]:
    linhas.append('PC%d & %.4f & %.2f\\%% & %.2f\\%% \\\\'
                  % (i + 1, autovalores[i], 100 * explicada[i],
                     100 * acumulada[i]))
linhas.append('\\midrule')
linhas.append('PC4--PC%d & %.4f--%.4f & --- & --- \\\\'
              % (len(autovalores) - 1, autovalores[-2], autovalores[3]))
linhas.append('\\midrule')
linhas.append('PC%d & %.4f & %.2f\\%% & %.2f\\%% \\\\'
              % (len(autovalores), autovalores[-1],
                 100 * explicada[-1], 100 * acumulada[-1]))
escreve('eigen.tex', linhas)

# loadings de PC1 e da ultima componente
loadings = pd.DataFrame({'PC1': autovetores[:, 0],
                         'PC%d' % len(autovalores): autovetores[:, -1]},
                        index=dados_pca.columns)
destaque = loadings.reindex(['BMI', 'Weight_kg', 'Height_cm'])
escreve('loadings.tex',
        ['%s & %+.3f & %+.3f \\\\'
         % (rotulo(n), r.iloc[0], r.iloc[1])
         for n, r in destaque.iterrows()])
print('\nloadings PC1 (3 maiores em modulo):')
print(loadings['PC1'].abs().sort_values(ascending=False).head(4).round(3))
print('loadings PC%d (3 maiores em modulo):' % len(autovalores))
print(loadings.iloc[:, 1].abs().sort_values(ascending=False).head(4).round(3))


# ------------------------------------------------------------------ figuras
def painel(colunas, nome_arquivo, titulo, condicional=False):
    n_col = 4
    n_lin = int(np.ceil(len(colunas) / n_col))
    fig, eixos = plt.subplots(n_lin, n_col,
                              figsize=(3.0 * n_col, 2.1 * n_lin))
    eixos = np.atleast_1d(eixos).ravel()
    for eixo, coluna in zip(eixos, colunas):
        if condicional:
            for nome_classe in ORDEM_CLASSES:
                serie = preditores.loc[preditores[CLASSE] == nome_classe,
                                       coluna].dropna()
                n_bins = min(30, preditores[coluna].nunique())
                eixo.hist(serie, bins=n_bins, density=True, histtype='step',
                          linewidth=1.3, color=CORES[nome_classe],
                          label=nome_classe)
        else:
            serie = quantitativos[coluna].dropna()
            # Varios preditores sao arredondados (idade inteira, sono em
            # meia hora). Com bins fixos o histograma fica serrilhado por
            # artefato de binning, nao por estrutura dos dados, entao
            # limitamos o numero de bins ao de valores distintos.
            eixo.hist(serie, bins=min(40, serie.nunique()),
                      color='tab:blue', edgecolor='white', linewidth=0.3)
        eixo.set_title(rotulo(coluna), fontsize=8)
        eixo.tick_params(labelsize=6)
    for eixo in eixos[len(colunas):]:
        eixo.axis('off')
    if condicional:
        eixos[0].legend(fontsize=6)
    fig.suptitle(titulo, fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(os.path.join(DIR_FIGURAS, nome_arquivo), dpi=150,
                bbox_inches='tight')
    plt.close(fig)
    print('  figura', nome_arquivo)


def boxplots(colunas, nome_arquivo, titulo):
    fig, eixos = plt.subplots(1, len(colunas),
                              figsize=(2.3 * len(colunas), 3.2))
    for eixo, coluna in zip(np.atleast_1d(eixos), colunas):
        dados = [preditores.loc[preditores[CLASSE] == c, coluna].dropna()
                 for c in ORDEM_CLASSES]
        caixas = eixo.boxplot(dados, tick_labels=ORDEM_CLASSES,
                              patch_artist=True, showfliers=False)
        for caixa, nome_classe in zip(caixas['boxes'], ORDEM_CLASSES):
            caixa.set_facecolor(CORES[nome_classe])
            caixa.set_alpha(0.6)
        eixo.set_title(rotulo(coluna), fontsize=9)
        eixo.tick_params(labelsize=7)
    fig.suptitle(titulo, fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(os.path.join(DIR_FIGURAS, nome_arquivo), dpi=150,
                bbox_inches='tight')
    plt.close(fig)
    print('  figura', nome_arquivo)


print('\ngerando figuras:')
colunas = list(quantitativos.columns)
destaques = ['Fasting_Blood_Sugar', 'HbA1c', 'Age', 'BMI']

painel(colunas, 'histogramas_incondicionais.png',
       'Histogramas incondicionais dos D = 20 preditores quantitativos')
painel(colunas, 'histogramas_condicionais.png',
       'Histogramas condicionais por classe de Diabetes_Risk',
       condicional=True)
boxplots(destaques, 'boxplots_condicionais.png',
         'Box-plots condicionais dos preditores mais discriminativos')

print('\nok')
