# applied-computational-intelligence

Homework 2 de Inteligência Computacional Aplicada (ICA), Departamento de
Engenharia de Teleinformática da UFC, disciplina ministrada pela Profa. Michela
Mulas.

Predição da solubilidade de 1.267 compostos químicos (951 de treino e 316 de
teste) a partir de 228 descritores moleculares. Após a análise exploratória e o
pré-processamento com Yeo-Johnson, são comparados quatro modelos de regressão:
OLS, ridge e PLS (NIPALS), implementados do zero, e um ensemble de redes neurais
em PyTorch. A comparação estatística usa bootstrap pareado no conjunto de teste.

## Conteúdo do repositório

O repositório principal do trabalho no github está hospedado no endereço https://github.com/alissonjsb4/applied-computational-intelligence

| Caminho | Descrição |
|---|---|
| `homework2.ipynb` | Notebook com a análise exploratória e os quatro modelos, já executado |
| `paper/main.pdf` | Relatório final, formato de artigo de conferência IEEE |
| `paper/main.tex` | Fonte LaTeX do relatório |
| `paper/refs.bib` | Referências bibliográficas do artigo |
| `figuras/` | Figuras geradas pelo notebook, incluindo as usadas no artigo |
| `dataset/` | Conjunto de dados de solubilidade (`solTrainX`, `solTrainY`, `solTestX`, `solTestY`) |
| `USO_DE_IA.md` | Apêndice de uso de ferramentas de IA |
| `dataset/TI0175_HW2_assignment.zip` | Enunciado |

## Como rodar

### Notebook

Python 3 com numpy, pandas, matplotlib, scipy, scikit-learn e PyTorch:

```
pip install numpy pandas matplotlib scipy scikit-learn torch
```

Abra `homework2.ipynb` no Jupyter e execute as células em ordem, a partir da
pasta `homework02/`: o notebook lê `dataset/` e grava `figuras/` por caminho
relativo. O dataset já está no repositório, não é preciso baixar nada. No Colab,
clone o repositório e mude para `homework02/` antes de executar.

O notebook do repositório já vem com todas as saídas salvas, de uma execução com
Python 3.13 e PyTorch 2.15 em CPU. A busca de hiperparâmetros da rede neural é a
etapa mais demorada, cerca de 6 minutos nessa execução.

### Artigo

Para compilar o artigo é preciso uma distribuição LaTeX com a classe `IEEEtran`:

```
cd paper
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

## Resultados

Desempenho dos quatro modelos, com hiperparâmetros escolhidos por validação
cruzada (CV) só no treino. A CV tem 10 folds nos modelos lineares e 5 folds na
rede neural. O intervalo é o IC de 95% por bootstrap do RMSE de teste.

| Modelo | Configuração | RMSE CV | RMSE teste | IC 95% | R² teste |
|---|---|---|---|---|---|
| OLS | Pseudoinversa via SVD | 0,7279 | 0,7430 | [0,6645; 0,8243] | 0,8718 |
| Ridge | λ ≈ 31,6 | 0,6862 | 0,7175 | [0,6457; 0,7898] | 0,8805 |
| PLS | 19 componentes | 0,7060 | 0,7337 | [0,6595; 0,8061] | 0,8750 |
| Rede neural | Ensemble de 5 redes, camada oculta `(64,)`, weight decay 1,0, dropout 0,3, 100 épocas | 0,6289 | 0,6407 | [0,5729; 0,7066] | 0,9047 |

No bootstrap pareado, nenhuma diferença entre os três modelos lineares é
significativa. A rede neural é significativamente melhor que cada um deles,
mesmo com correção de Bonferroni.

## Autores e contribuições

| Autor | Matrícula | Contribuição |
|---|---|---|
| Ícaro Adriano | 609310 | EDA, pré-processamento Yeo-Johnson, PLS via NIPALS, Rede Neural em PyTorch e figuras correspondentes. |
| Alisson Jaime | 555083 | OLS e Ridge implementados do zero, validação cruzada comparada ao scikit-learn, bootstrap pareado estendido aos 4 modelos e redação das seções correspondentes no artigo. |
| Matheus Reis | 571954 | — |
| Vinícius A. G. do Nascimento | 568594 | — |

## Uso de IA

Ferramentas de IA foram utilizadas no desenvolvimento deste trabalho. Os
prompts, as respostas e o destino de cada uma estão registrados em
[`USO_DE_IA.md`](USO_DE_IA.md), conforme exigido pelo enunciado.
