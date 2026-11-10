# Apêndice: uso de ferramentas de IA

O enunciado do Homework 2 permite o uso de ferramentas de IA e exige que ele seja
declarado, com os prompts e as respostas registrados em apêndice ou em arquivo
separado do repositório. Este é esse arquivo.

Ferramenta utilizada: **Claude** (Anthropic).

Cada entrada abaixo registra o que foi pedido, o que a ferramenta devolveu e o
que os autores fizeram com aquilo. Os prompts foram transcritos em registro
uniforme, preservando integralmente o conteúdo de cada solicitação. As respostas
eram extensas e estão resumidas, com indicação de onde o resultado foi
incorporado ao repositório, que é o registro verificável.

---

## Alisson Jaime

Sessões externas no navegador, durante o desenvolvimento do Homework 2. Cada
entrada indica o commit correspondente.

### 1. Ordem das células do notebook

**Prompt:** "Movi as células de pré-processamento, rmse, r2 e folds para antes da seção do OLS. Sem alterar o notebook, confira se alguma célula usa uma variável antes de defini-la."

**Resposta:** verificado que helpers, folds (semente 42) e matrizes padronizadas
são definidos antes dos modelos.

**O que foi feito:** ajustado `.values.copy()` para compatibilidade com pandas 3.
Commit `27439ab`.

### 2. Instabilidade da equação normal

**Prompt:** "Por que a equação normal fica instável com preditores de correlação próxima de 1, como FP134 e NumSulfer? Qual a diferença conceitual entre solve, pseudoinversa e lstsq nesse caso? Explique sem escrever a implementação."

**Resposta:** explicação sobre $\kappa(X) \approx 3,13 \times 10^4$ e uso de SVD
na pseudoinversa para lidar com queda de posto (228 para 227 nos folds 4 e 7).

**O que foi feito:** OLS implementado do zero por pseudoinversa via SVD. Commit
`27439ab`.

### 3. Comparação do OLS com o scikit-learn

**Prompt:** "Meu OLS deu RMSE 0,742978 e R² 0,871814 no teste, e o LinearRegression deu 0,742978 e 0,871814. Essa diferença é compatível com erro numérico? Se não for, o que devo verificar?"

**Resposta:** confirmada a compatibilidade numérica ($10^{-10}$ nos coeficientes
e $10^{-13}$ nas predições) e o cancelamento entre `FP134` (+105,95) e
`NumSulfer` (-106,14).

**O que foi feito:** comparação do OLS com a função pronta no conjunto de teste.
Commit `27439ab`.

### 4. Revisão da validação cruzada

**Prompt:** "Leia minha célula de CV. Sem reescrever, aponte se há vazamento de dados entre as dobras ou erro no cálculo de RMSE e R²."

**Resposta:** confirmado o isolamento por dobra e o uso de `Pipeline` no sklearn
(RMSE CV 0,7279 ± 0,0215, R² CV 0,8654 ± 0,0128).

**O que foi feito:** validação cruzada k-fold própria e com função pronta. Commit
`27439ab`.

### 5. Estimativa de CV e desempenho no teste

**Prompt:** "Minha CV deu RMSE 0,7279 ± 0,0215 e o teste deu 0,7430. Meu comentário relaciona a diferença ao erro padrão e à maior variância do teste para o R² (0,8718 vs 0,8654). O raciocínio está correto? Aponte falhas sem reescrever o texto."

**Resposta:** validada a interpretação do IC da CV ([0,679; 0,777]) e do efeito
do desvio padrão de $y$ no teste (2,078 vs 2,047).

**O que foi feito:** comparação das estimativas de CV com o desempenho no teste.
Commit `27439ab`.

### 6. Intercepto não penalizado no ridge

**Prompt:** "Por que o intercepto não é penalizado no ridge? Com X padronizado e y centrado, o que acontece na estimação? Explique sem escrever código."

**Resposta:** explicado o desacoplamento ortogonal do intercepto
($\hat{\beta}_0 = \bar{y}$) e a estimação de $\hat{\beta}(\lambda)$ via SVD.

**O que foi feito:** regressão ridge implementada do zero. Commit `27439ab`.

### 7. Relação entre `alpha` e $\lambda$

**Prompt:** "Como o alpha do Ridge do sklearn se relaciona com o λ da forma fechada? Meus coeficientes diferem em no máximo 7,4e-9 da função pronta. Isso indica implementação correta?"

**Resposta:** confirmada a equivalência direta entre `alpha` e $\lambda$ e a
concordância numérica nos 29 valores da grade.

**O que foi feito:** comparação do ridge com a função pronta. Commit `27439ab`.

### 8. Grade de $\lambda$ e diferença para o `GridSearchCV`

**Prompt:** "Usei a grade logspace(-3, 4, 29) e o mínimo ficou em λ ≈ 31,62. A faixa é adequada? O que explica a diferença de 3,4e-4 no perfil do GridSearchCV com StandardScaler?"

**Resposta:** confirmado o mínimo interior (RMSE CV 0,6862) e identificada a
diferença de escala por `ddof=0` no `StandardScaler` vs `ddof=1` manual.

**O que foi feito:** seleção de $\lambda$ com perfil de CV. Commit `27439ab`.

### 9. Interpretação dos resultados do ridge

**Prompt:** "Ridge: teste RMSE 0,7175, R² 0,8805. OLS: RMSE 0,7430, R² 0,8718. Comente se minha explicação em termos de viés, variância e encolhimento da norma de β (152,02 para 1,48) está correta."

**Resposta:** validada a discussão sobre o trade-off viés-variância, a
estabilização do par `NumSulfer`/`FP134` (-0,057/-0,056) e o leve otimismo de
seleção da CV.

**O que foi feito:** resultados do ridge no conjunto de teste. Commit `27439ab`.

### 10. Bootstrap pareado com correção de Bonferroni

**Prompt:** "Estendi o bootstrap pareado aos 4 modelos (6 pares). Comparar 6 pares exige algum cuidado? Confira minha interpretação dos ICs com correção de Bonferroni."

**Resposta:** confirmado o uso de Bonferroni ($\alpha/6$), o empate estatístico
entre os modelos lineares (Ridge-PLS [-0,0350; 0,0020]) e a superioridade
significativa da Rede Neural.

**O que foi feito:** comparação estatística estendida aos quatro modelos. Commit
`27439ab`.

### 11. Coerência do notebook re-executado

**Prompt:** "Rodei o notebook do início ao fim e os resultados são OLS 0,7430, Ridge 0,7175, PLS 0,7337 e Rede 0,6407. Sem alterar nada, verifique se a tabela é coerente com os comentários das células."

**Resposta:** verificada a consistência de todas as células e saídas após a
re-execução completa.

**O que foi feito:** notebook re-executado do início ao fim. Commit `27439ab`.

### 12. Revisão das seções do artigo

**Prompt:** "Leia as seções que escrevi em main.tex. Aponte erros conceituais, afirmações sem suporte nos resultados e figuras ou tabelas não discutidas. Não reescreva os parágrafos."

**Resposta:** revisão de consistência entre equações, tabelas e figuras de OLS e
Ridge no manuscrito.

**O que foi feito:** métodos e resultados das partes 1 e 2 no artigo. Registrado no commit final do artigo e documentação.

### 13. Conclusões e referências

**Prompt:** "Confira se as conclusões decorrem dos números da tabela de comparação estatística e se toda referência citada existe em refs.bib. Aponte só os problemas."

**Resposta:** checagem do alinhamento das conclusões com o bootstrap pareado e
validação das chaves bibliográficas.

**O que foi feito:** comparação estatística e conclusões no artigo. Registrado no commit final do artigo e documentação.

### 14. Verificação do README

**Prompt:** "Compare homework02/README.md com as exigências do projeto e liste o que falta: descrição, como rodar, dependências e contribuição de cada coautor."

**Resposta:** verificação final da documentação no README.

**O que foi feito:** registrado no commit final, `README and AI usage log for
homework 2`.

---

## Ícaro Adriano

Foi realizado uso de IA no que tange a pesquisa de funções e métodos da linguagem de programação utilizada, identificação de erros e levantamento de soluções e avaliação de estrutura e argumentos do corpo textual do trabalho escrito bem como correções ortograficas.
---

## Declaração

As decisões de método deste trabalho, a interpretação dos resultados e a redação
do artigo são dos autores. As ferramentas de IA foram usadas para localizar erros
no código, executar verificações sobre a validação cruzada e os resultados dos
modelos, organizar a estrutura do texto e conferir referências. Os resultados
numéricos apresentados no artigo são reproduzíveis a partir do repositório:
`homework2.ipynb` regenera os resultados a partir do dataset original.
