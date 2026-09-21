# applied-computational-intelligence

Homework 1 de Inteligência Computacional Aplicada (ICA), Departamento de
Engenharia de Teleinformática da UFC, disciplina ministrada pela Profa. Michela
Mulas.

Análise exploratória de um conjunto de dados sintético de risco de diabetes com
50.000 pacientes: estatística monovariada incondicional e condicional à classe,
análise bivariada por correlação de Pearson e análise multivariada por PCA
implementado sem bibliotecas prontas.

## Conteúdo do repositório

| Caminho | Descrição |
|---|---|
| `homework1.ipynb` | Notebook com as cinco questões do enunciado, já executado |
| `paper/main.pdf` | Relatório final, formato de artigo de conferência IEEE |
| `paper/main.tex` | Fonte LaTeX do relatório |
| `paper/gerar_tabelas.py` | Gera as tabelas do artigo a partir do dataset |
| `paper/tabelas/` | Fragmentos LaTeX gerados pelo script acima |
| `figuras/` | Figuras referenciadas pelo artigo |
| `dataset/` | Conjunto de dados utilizado |
| `USO_DE_IA.md` | Apêndice de uso de ferramentas de IA |
| `TI0175_HW1_assignment.pdf` | Enunciado |

## Como rodar

### Notebook

Python 3 com pandas, matplotlib e numpy:

```
pip install pandas matplotlib numpy
```

Abra `homework1.ipynb` no Jupyter ou no Colab e execute as células em ordem. O
dataset já está em `dataset/diabetes_risk_prediction_dataset.csv`, não é preciso
baixar nada. O notebook do repositório já vem com todas as saídas salvas.

### Tabelas e artigo

As tabelas do artigo não são digitadas à mão. Para regerá-las a partir do
dataset:

```
python paper/gerar_tabelas.py
```

O script escreve os fragmentos em `paper/tabelas/`, que o `main.tex` inclui com
`\input`. Para compilar o artigo é preciso uma distribuição LaTeX com a classe
`IEEEtran`:

```
cd paper
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

## Autores e contribuições

| Autor | Matrícula | Contribuição |
|---|---|---|
| Ícaro Adriano | 609310 | Questões 1 e 2: descrição do conjunto de dados e análise monovariada incondicional. Estrutura inicial do artigo em LaTeX e primeira versão do resumo. |
| Matheus Reis | 571954 | Questões 4 e 5: análise bivariada, matriz de correlação e PCA implementado do zero. Correção da análise condicional da questão 3. |
| Alisson Jaime | 555083 | Identificação e correção da variável de classe usada nas questões 3, 4 e 5. Análise de poder discriminativo dos preditores. Tabulação das estatísticas e redação dos resultados. |
| Vinícius Alexandre Gomes do Nascimento | 568594 | — |

## Uso de IA

Ferramentas de IA foram utilizadas no desenvolvimento deste trabalho. Os
prompts, as respostas e o destino de cada uma estão registrados em
[`USO_DE_IA.md`](USO_DE_IA.md), conforme exigido pelo enunciado.
