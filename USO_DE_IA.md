# Apêndice: uso de ferramentas de IA

O enunciado do Homework 1 permite o uso de ferramentas de IA e exige que ele seja
declarado, com os prompts e as respostas registrados em apêndice ou em arquivo
separado do repositório. Este é esse arquivo.

Ferramenta utilizada: **Claude** (Anthropic), nas versões Sonnet 5 e Opus 5,
através do Claude Code.

Cada entrada abaixo registra o que foi pedido, o que a ferramenta devolveu e o
que os autores fizeram com aquilo. Os prompts estão transcritos com correção de
digitação e pontuação, mantendo o conteúdo do que foi pedido. As respostas eram
longas, então estão resumidas, com indicação de onde o resultado foi parar no
repositório, que é o registro verificável.

---

## Matheus Reis

Uso registrado no próprio histórico do repositório: o commit `abb04e0`, de
20/09/2026, está assinado com `Co-Authored-By: Claude Sonnet 5`.

**Escopo:** redação do código das questões 4 (análise bivariada) e 5 (PCA
implementado sem bibliotecas prontas), e preenchimento do README.

> **A PREENCHER PELO MATHEUS:** transcrever aqui os prompts efetivamente usados
> na sessão da madrugada de 20/09 e um resumo do que a ferramenta devolveu.

---

## Alisson Jaime

Sessão de 20/09/2026, Claude Opus 5 via Claude Code, com acesso de leitura ao
repositório local e ao dataset.

### 1. Levantamento do estado do trabalho

**Prompt:** "Procura no meu computador o repositório do trabalho de ICA,
`applied-computational-intelligence`. Vê o que está faltando do trabalho que eu
possa fazer."

**Resposta:** a ferramenta localizou o repositório no GitHub, clonou, leu o PDF
do enunciado e o notebook, e listou as pendências: ausência do artigo em PDF,
células sem saída salva, ausência do apêndice de uso de IA e matrícula pendente
no README. Apontou também que as análises condicional, bivariada e de PCA
estavam agrupadas por `Gender` e `Country`, e não pela coluna de rótulo.

**O que foi feito:** a lista virou o plano de trabalho da noite e foi levada ao
grupo por WhatsApp.

### 2. Leitura do histórico de commits

**Prompt:** "O Matheus disse que fez coisas às duas da manhã. O que ele fez?
O que são esses commits?"

**Resposta:** resumo dos dois commits, incluindo a correção do erro de digitação
`Conutry` para `Country`, que impedia a análise condicional por país de
executar.

**O que foi feito:** serviu para dividir o trabalho restante sem sobreposição.

### 3. Verificação da escolha da variável de classe

**Prompt:** "Não entendi a necessidade da troca da classe. Me explica melhor o
que está faltando e o que a gente já tem pronto."

**Resposta:** explicação de que a classe pedida pelo enunciado é uma coluna de
rótulo, e não o conjunto de valores distintos das colunas qualitativas; e de que
a coluna `Diabetes_Risk` havia sido descartada junto com as demais qualitativas.

**O que foi feito:** fundamentou a decisão de adotar `Diabetes_Risk` como
rótulo, discutida e acordada no grupo.

### 4. Quantificação do poder discriminativo

**Prompt:** "Compara o quanto cada preditor separa as classes quando se agrupa
por gênero e quando se agrupa por risco de diabetes."

**Resposta:** execução de um script sobre o dataset, retornando a amplitude
entre médias de classe normalizada pelo desvio padrão de cada preditor. Por
gênero, todos os valores ficaram próximos de zero; por `Diabetes_Risk`, glicemia
de jejum e HbA1c se destacaram.

**O que foi feito:** os números sustentaram a decisão no grupo e estão na
Tabela de poder discriminativo do artigo, regerada pelo script
`paper/gerar_tabelas.py`.

### 5. Correção e execução do notebook

**Prompt:** "Troca a classe para `Diabetes_Risk` nas questões 3, 4 e 5, roda o
notebook inteiro e sobe numa branch."

**Resposta:** edição das células, correção de um erro no vetor de cores da
scatter matrix (o pandas descarta linhas com valores ausentes internamente),
acréscimo das tabulações exigidas pelo enunciado, execução completa e commit.

**O que foi feito:** é o commit `41e77e1`. O diagnóstico da estrutura do dataset
que aparece nos Resultados partiu da leitura dos autovalores produzidos nessa
execução.

### 6. Estrutura do artigo

**Prompt:** "Faz o esqueleto do que o artigo precisa ter e do que eu posso falar
em cada seção."

**Resposta:** esqueleto por seção, com a distribuição de pontos do enunciado, os
números disponíveis para cada bloco de resultados e alternativas de título.

**O que foi feito:** o esqueleto virou a estrutura de `paper/main.tex`. A prosa
das seções foi escrita pelos autores.

### 7. Referências bibliográficas

**Prompt:** "Busca e confirma os dados corretos das referências da ADA e do IDF
Atlas."

**Resposta:** busca nas fontes e devolução das referências conferidas, que estão
em `paper/refs.bib`.

---

## Ícaro Adriano

> **A PREENCHER PELO ÍCARO:** registrar aqui o uso de IA, se houve, na redação
> do esqueleto do artigo e do abstract inicial. Se não houve, declarar
> explicitamente que a seção foi escrita sem auxílio de ferramentas de IA.

---

## Vinícius Alexandre Gomes do Nascimento

> **A PREENCHER PELO VINÍCIUS:** mesma orientação acima.

---

## Declaração

As decisões de método deste trabalho, a escolha da variável de classe, a
interpretação dos resultados e a redação do artigo são dos autores. As
ferramentas de IA foram usadas para localizar erros no código, executar
verificações sobre o dataset, organizar a estrutura do texto e conferir
referências. Os resultados numéricos apresentados no artigo são reproduzíveis a
partir do repositório: `paper/gerar_tabelas.py` regenera todas as tabelas
a partir do dataset original.
