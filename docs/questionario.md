# Questionário: educação financeira entre graduandos e suas famílias

**Versão:** 2, alinhada ao formulário publicado no Google Forms · 05/11/2026 · **Status:** formulário publicado; nenhuma resposta tratada neste repositório (as respostas ficam fora do Git).

**Formulário:** "Educação financeira entre estudantes de graduação (UFPB / CORECON-PB)" · <https://docs.google.com/forms/d/e/1FAIpQLSel8h8rKd4svyMe79V1ME_7TQSW466HPaT5WGMpb-kU3PNWgg/viewform>

## 1. Objetivo e pergunta

Diagnosticar quanto estudantes de graduação sabem e praticam de educação financeira, em especial **reserva de emergência**, e qual é o contexto financeiro e o nível de conhecimento percebido em suas famílias.

**Perguntas específicas**

1. Quantos estudantes sabem o que é reserva de emergência e quantos acertam os conceitos básicos (inflação, juros compostos, diversificação)?
2. Quantos estudantes têm reserva de emergência, de quantos meses e onde a guardam?
3. Como é a situação financeira da família, segundo o estudante (renda em faixas, dívidas, orçamento, reserva)?
4. Que nível de conhecimento financeiro o estudante percebe na família, e as famílias conversam sobre dinheiro?
5. Quais temas e termos os estudantes gostariam de ver no glossário?

**Expectativas iniciais** (hipóteses de trabalho, a validar pela equipe):

- H1: a minoria dos estudantes tem reserva de emergência.
- H2: mais estudantes reconhecem o conceito do que o praticam.
- H3: o escore de conhecimento é maior entre estudantes de Economia do que entre os de outros cursos (o formulário aceita vários cursos, então esta hipótese pode ser examinada).
- H4: estudantes cujas famílias conversam sobre dinheiro têm escore de conhecimento maior.

## 2. Desenho

| Item | Situação |
|---|---|
| População | Graduandos maiores de 18 anos. Em 27/10/2026 a equipe definiu **Ciências Econômicas**; o formulário publicado aceita Ciências Econômicas, Administração, Ciências Contábeis e "Outro" **[a confirmar com a equipe qual é a população]** |
| Amostragem | Por conveniência (divulgação em turmas e canais dos cursos). **Não é representativa**; os resultados descrevem quem respondeu |
| Aplicação | Google Forms, anônimo e voluntário; 8 páginas, 29 perguntas, todas obrigatórias, cerca de 8 minutos. O formulário não tem campo de e-mail |
| Meta de respostas | **[a definir]** |
| Período | 01/11 a 20/11/2026, definido pela equipe em 27/10/2026 |
| Referência metodológica | Estrutura em conhecimento, comportamento e atitude, inspirada no OECD/INFE Toolkit. As perguntas são **redação própria** da equipe |

**Mudanças em relação ao rascunho de 27/10/2026**

- Nova pergunta de conhecimento, **b7** (lugar adequado para a reserva de emergência), que não estava no rascunho. Ela é tabulada, mas **não entra no escore** (decisão pendente, ver seção 5).
- O item de termo (antes **e3**, texto livre) virou **múltipla escolha com 7 termos e "Nenhum deles"** (`e3_termo_prioritario`): não há mais resposta aberta com risco de dado pessoal.
- Curso (a1) é uma lista fechada de 3 cursos mais "Outro" com campo de texto; o texto digitado **não é guardado** no tratamento.
- O limite de 3 temas em e1 passou a ser **imposto pelo formulário**.
- O rascunho dizia que o valor exportado de cada opção seria a letra (a, b, c...). O Google Forms **não permite isso**: ele exporta o texto da opção. A tradução para códigos é feita por `notebooks/02a_formulario_google.py` (ver seção 6).

## 3. Termo de consentimento (primeira página)

O texto de abertura do formulário informa: pesquisa feita por estudantes da UFPB na disciplina Técnicas de Pesquisa e Análise Econômica II, em parceria com o CORECON-PB, para orientar um glossário de economia aberto ao público; participação **voluntária**; pesquisa **anônima** (não pede nome, e-mail, CPF nem matrícula); perguntas sobre renda e dívidas com a opção "Prefiro não responder"; resultados divulgados **somente de forma agregada**; participação só de maiores de 18 anos; duração de cerca de 8 minutos; contato da equipe indicado no próprio formulário.

Pergunta obrigatória "Consentimento":

- ( ) Tenho 18 anos ou mais, li as informações acima e aceito participar.
- ( ) Não aceito participar. *(o formulário é enviado sem as demais perguntas; essas linhas são excluídas no tratamento)*

## 4. Perguntas

Estrutura em páginas: 1 consentimento · 2 Bloco A (perfil) · 3 Bloco B (conhecimento) · 4 Bloco C (prática: c1 e c2) · 5 "Sobre a sua reserva de emergência" (c3 e c4, **só para quem responde Sim ou Parcialmente em c2**; "Não" pula para a página 6) · 6 "Dívidas e poupança" (c5 e c6) · 7 Bloco D (família) · 8 Bloco E (glossário).

Todas as perguntas são obrigatórias. A coluna **Código** é o nome da variável no tratamento. A redação exata das opções, como o Google Forms as exporta, está em [`../outputs/mapa_formulario.csv`](../outputs/mapa_formulario.csv).

### Bloco A: perfil

| Código | Pergunta | Opções |
|---|---|---|
| a1_curso | Qual é o seu curso de graduação? *(Se diferente das opções, por favor informar)* | Ciências Econômicas · Administração · Ciências Contábeis · Outro (texto livre) |
| a2_periodo | Em que período você está? | 1º ao 4º · 5º ao 8º · 9º ou mais |
| a3_idade | Qual é a sua faixa de idade? | 18 a 20 · 21 a 23 · 24 a 26 · 27 ou mais |
| a4_ocupacao | Qual é a sua situação atual? | Só estudo · Estudo e trabalho ou estágio · Outra |
| a5_renda_propria | Qual é a sua renda própria mensal (trabalho, estágio, bolsa)? | Nenhuma · Até 1 salário mínimo · Mais de 1 até 2 salários mínimos · Mais de 2 salários mínimos · Prefiro não responder |

### Bloco B: conhecimento

Instrução do formulário: *"Responda sem consultar nada. Se não souber, marque 'Não sei': isso nos ajuda a entender onde falta informação."*

Itens b1, b3, b4 e b5 têm **uma resposta correta** (✔), que vale 1 ponto. b2 e b6 não pontuam. **b7 não pontua** por decisão provisória (abaixo). As opções de b1, b3, b4, b5 e b7 vêm com letra no próprio texto no formulário (a, b, c...), e é essa letra que vira o código.

**b1_reserva_def.** Qual alternativa melhor descreve uma reserva de emergência?
- a) Dinheiro guardado para comprar algo que você quer muito, como uma viagem.
- b) Dinheiro guardado e de fácil acesso para cobrir imprevistos ou perda de renda. **✔**
- c) Dinheiro investido em ações para ganhar o máximo possível.
- d) Limite do cartão de crédito ou do cheque especial.
- e) Não sei

**b2_reserva_meses.** Na sua opinião, quantos meses de despesas seria adequado guardar como reserva de emergência?
- Menos de 1 mês · De 1 a 3 meses · De 3 a 6 meses · Mais de 6 meses · Não sei
- **Não pontua.** As fontes oficiais consultadas em 27/10/2026 não trazem um número único de meses, então a pergunta é de **opinião**: só se mostra a distribuição das respostas.

**b7_reserva_local.** Qual destes lugares é mais adequado para a reserva de emergência? *(pergunta nova)*
- a) Um investimento de longo prazo, sem possibilidade de resgate por anos.
- b) Ações da bolsa, que podem render muito.
- c) Uma aplicação segura, que possa ser resgatada rapidamente quando necessário. **(opção adequada)**
- d) Um limite de crédito pré-aprovado no banco.
- e) Não sei
- **Não pontua por enquanto.** Pontuar mudaria o escore de 0 a 4 para 0 a 5 e exigiria redefinir os cortes dos níveis. **[decisão da equipe]**

**b3_inflacao.** Você tem R$ 100 guardados e eles rendem 2% em um ano. Nesse mesmo ano, os preços sobem 5%. Depois de um ano, com esse dinheiro você poderá comprar:
- a) Mais do que hoje. b) Exatamente o mesmo. c) Menos do que hoje. **✔** d) Não sei

**b4_juros_compostos.** Você deve R$ 1.000 em uma dívida com juros de 10% ao mês e não paga nada por 2 meses. Quanto você deverá no fim do segundo mês?
- a) R$ 1.200 b) R$ 1.210 **✔** c) R$ 1.100 d) Não sei

**b5_diversificacao.** Colocar todo o seu dinheiro em um único investimento, em vez de dividi-lo em vários, em geral significa:
- a) Risco maior. **✔** b) Risco menor. c) O mesmo risco. d) Não sei

**b6_autoavaliacao.** De 1 (nenhum) a 5 (muito alto), como você avalia o seu conhecimento sobre finanças pessoais? *(escala linear 1 a 5; não pontua)*

### Bloco C: prática

| Código | Pergunta | Opções |
|---|---|---|
| c1_orcamento | Você anota ou planeja seus gastos e receitas do mês? | Nunca · Às vezes · Sempre |
| c2_tem_reserva | Você tem uma reserva de emergência? | Sim · Parcialmente · Não |
| c3_reserva_cobertura | *(página própria; só se c2 = Sim ou Parcialmente)* Sua reserva cobre aproximadamente quantos meses das suas despesas? | Menos de 1 mês · De 1 a 3 meses · De 3 a 6 meses · Mais de 6 meses |
| c4_onde_guarda | *(mesma página; marque todas)* Onde você guarda esse dinheiro? | Poupança · Renda fixa (CDB, Tesouro etc.) · Conta corrente · Dinheiro em casa · Outro |
| c5_dividas | Você tem alguma dessas dívidas hoje? *(marque todas)* | Cartão de crédito · Empréstimo ou financiamento · Parcelas atrasadas · Nenhuma · Prefiro não responder |
| c6_poupa_regular | Você guarda uma parte do que recebe todo mês? | Sim · Às vezes · Não |

### Bloco D: família

Instrução do formulário: *"Estas perguntas pedem o seu relato sobre a sua família. Pode responder 'Não sei' ou 'Prefiro não responder'."*

| Código | Pergunta | Opções |
|---|---|---|
| d1_renda_familiar | Qual é, aproximadamente, a renda mensal total da sua família? | Até 1 salário mínimo · Mais de 1 até 3 · Mais de 3 até 6 · Mais de 6 · Não sei · Prefiro não responder |
| d2_fam_conversa | Na sua casa, vocês conversam sobre dinheiro e contas? | Nunca · Às vezes · Frequentemente |
| d3_fam_orcamento | Sua família controla o orçamento (anota ou planeja os gastos)? | Sim · Não · Não sei |
| d4_fam_reserva | Sua família tem dinheiro guardado para emergências? | Sim · Não · Não sei |
| d5_fam_dividas | Sua família tem dívidas em atraso? | Sim · Não · Não sei · Prefiro não responder |
| d6_fam_conhecimento | De 1 (nenhum) a 5 (muito alto), como você avalia o conhecimento da sua família sobre finanças? | 1 – Nenhum · 2 · 3 · 4 · 5 – Muito alto · Não sei |
| d7_educ_recebida | Onde você já teve contato com educação financeira? *(marque todas)* | Escola · Família · Curso ou faculdade · Internet e redes sociais · Nunca tive |

### Bloco E: glossário

| Código | Pergunta | Opções |
|---|---|---|
| e1_temas_interesse | Que temas você gostaria de ver explicados no glossário? *(no máximo 3, imposto pelo formulário)* | Orçamento · Reserva de emergência · Crédito e juros · Dívidas e renegociação · Investimentos · Inflação e Selic · Impostos · Outro |
| e3_termo_prioritario | Qual destes termos você mais gostaria de ver explicado? | Juros compostos · Inflação · Taxa Selic · Renda fixa · Diversificação · Endividamento · Orçamento pessoal · Nenhum deles |
| e2_usaria_glossario | Você usaria um glossário online de termos da economia? *(o formulário descreve o site como interativo, para ampliar o conhecimento comum sobre termos econômicos, educação financeira e macroeconomia)* | Sim · Talvez · Não |

## 5. Indicadores e análise

**Pontuação.** `escore_conhecimento` = acertos em b1, b3, b4 e b5 (0 a 4). "Não sei" conta como erro, e resposta ausente ou inválida também. b2, b6 e b7 não entram no escore.

**Níveis (proposta, a confirmar):** baixo = 0 a 1 · médio = 2 a 3 · alto = 4.

| Pergunta | Indicador | Cruzamento previsto |
|---|---|---|
| Conhecimento do conceito | % que acerta b1; distribuição do escore; % que escolhe a opção adequada em b7 (não pontua) | Curso, período |
| Prática | % com reserva (c2); distribuição de c3; % que faz orçamento (c1) | Curso, período, renda própria |
| Conhecimento × prática | % com reserva entre quem acerta b1 e entre quem não acerta | — |
| Família | % de famílias com reserva (d4), com orçamento (d3), com dívidas em atraso (d5); média de d6 | Faixa de renda familiar (d1) |
| Família × estudante | Escore médio segundo d2 (conversa em casa); reserva do estudante × reserva da família | — |
| Glossário | Temas mais marcados (e1); termo mais pedido (e3) | — |

Regras de apresentação: percentuais com o **n** de cada base; "Não sei" e "Prefiro não responder" mostrados à parte; nenhuma célula com menos de 5 respondentes.

## 6. Do formulário às tabelas

1. Exportar as respostas do Google Forms em CSV para `data/raw/respostas_questionario.csv` (fora do Git).
2. O notebook [`03_obtencao_limpeza_tratamento.ipynb`](../notebooks/03_obtencao_limpeza_tratamento.ipynb) traduz o texto das opções para códigos com [`02a_formulario_google.py`](../notebooks/02a_formulario_google.py), descarta identificação e qualquer coluna fora do livro de códigos, trata os dados e grava só tabelas agregadas em `data/processed/`.
3. O mapa pergunta/opção → variável/código está em [`outputs/mapa_formulario.csv`](../outputs/mapa_formulario.csv); os códigos válidos, em [`outputs/livro_de_codigos.csv`](../outputs/livro_de_codigos.csv). Se o formulário mudar, atualize `QUESTOES` em `02a_formulario_google.py`: os testes do notebook apontam o que ficou fora.

O mapa foi conferido contra o formulário publicado em 05/11/2026 (29 perguntas, títulos, tipos e todas as opções idênticos). Falta conferir com a exportação real das primeiras respostas.

## 7. Limitações a declarar no relatório

- Amostra por conveniência: não permite generalizar para todos os graduandos.
- Respostas autodeclaradas, sujeitas a viés de desejabilidade.
- Dados sobre a família são o **relato do estudante**; "o que as famílias sabem" é a percepção dele, não uma medida feita com a família.
- Sem seguimento no tempo: mostra um retrato, não mudança.

## 8. Conexão com o glossário

Cada item de conhecimento corresponde a verbetes do glossário, o que permite priorizar os mais necessários. Situação em 05/11/2026 (o glossário tem 6 verbetes):

| Item | Verbetes | Existem hoje? |
|---|---|---|
| b1, b2, b7, c2–c4 | Reserva de emergência | Sim |
| b3 | Inflação, Taxa Selic | Sim |
| b4, c5 | Juros, Endividamento | Sim |
| c1, c6 | Orçamento pessoal | Sim |
| b5 | Investimentos | **Não** |
| e3 (termos oferecidos) | Juros compostos, Inflação, Taxa Selic, Renda fixa, Diversificação, Endividamento, Orçamento pessoal | Faltam **Juros compostos, Renda fixa e Diversificação** |
