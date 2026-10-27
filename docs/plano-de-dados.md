# Plano de dados (Entrega 4)

**TPAE II – PSAE00320 · Equipe 01** · Ana Beatriz Laurentino, Arthur Almeida e Gabriel Pinheiro · Orientador: Alessio
Demandante: CORECON-PB · Última atualização: 27/10/2026

> Este plano cobre os **dois produtos** do projeto: (1) o glossário da economia (site) e (2) a pesquisa com estudantes de graduação sobre educação financeira. Itens marcados **[a confirmar]** dependem de decisão da equipe, do professor ou do CORECON-PB e não foram preenchidos por suposição.

## 1. Visão geral

| Produto | Dados | Natureza |
|---|---|---|
| Glossário da Economia | Verbetes (termo, definição, exemplo, relações, fonte) | Texto elaborado pela equipe, conferido em fontes oficiais |
| Pesquisa com graduandos | Respostas anônimas a um questionário | Dado primário coletado pela equipe |

Os resultados da pesquisa orientam quais termos e temas o glossário prioriza (por exemplo, os conceitos que menos respondentes dominam).

## 2. Inventário de fontes

Status geral (27/10/2026): as páginas de F5, F6 e F7 foram abertas e **nenhuma traz aviso de licença**; por isso o uso se limita a **citar a fonte, sem versionar os arquivos**. F4 e F8 foram apenas localizados e ainda não foram abertos. O inventário do projeto anterior (escolas) está arquivado em [`arquivo/escolas/inventario_fontes.md`](arquivo/escolas/inventario_fontes.md).

| # | Base | Instituição / link | Cobertura | Formato | Acesso | Licença | Data de acesso | Uso no projeto |
|---|---|---|---|---|---|---|---|---|
| F1 | Questionário próprio | Equipe 01 · Google Forms | Graduandos do curso de Ciências Econômicas · coleta de 01/11 a 20/11/2026 | CSV exportado | Coleta própria, anônima e voluntária | Dados da equipe; divulgação **somente agregada** | — (coleta ainda não iniciada) | Base da pesquisa |
| F2 | Verbetes do glossário | Elaboração da equipe · `data/glossario.json` | Termos escolhidos a partir da lista de demandas do CORECON-PB **[a confirmar a lista]** | JSON | Repositório | Autoria da equipe | 27/10/2026 | Conteúdo do site |
| F3 | Lista de demandas do CORECON-PB | CORECON-PB (documento recebido pela equipe) | **[a registrar]** | **[a registrar]** | Documento institucional | **[a verificar]** se pode ser versionado; por padrão **não** vai ao repositório | **[a registrar]** | Origem dos termos do glossário |
| F4 | Caderno de Cidadania Financeira | Banco Central do Brasil · <https://www.bcb.gov.br/pre/pef/port/caderno_cidadania_financeira.pdf> | Nacional · conceitos de educação e cidadania financeira | PDF | Público (web) | A verificar (documento ainda não aberto) | 27/10/2026 (link localizado, não aberto) | Conferência de conceitos dos verbetes |
| F5 | Estratégia Nacional de Educação Financeira (ENEF) | Banco Central · <https://www.bcb.gov.br/pre/pef/PORT/enef.asp?frame=1> | Nacional | Página web | Público (web) | Sem aviso de licença na página; citar a fonte, não versionar | 27/10/2026 (página aberta) | Contexto institucional. A página descreve a ENEF (criada por decreto, ações gratuitas e de interesse público) e **não menciona reserva de emergência** |
| F6 | Proposta da Estratégia Nacional de Educação Financeira (Coremec) | gov.br/investidor · <https://www.gov.br/investidor/pt-br/educacional/plano-diretor-enef-estrategia-nacional-de-educacao-financeira.pdf/@@display-file/file> | Nacional · documento histórico (dados de cerca de 2008); **não é o plano vigente** | PDF | Público (web) | Sem aviso de licença no trecho lido; citar a fonte, não versionar | 27/10/2026 (aberto, leitura parcial) | Referência histórica de temas. O trecho lido fala em poupar para imprevistos, **sem indicar número de meses** |
| F7 | OECD/INFE Toolkit for Measuring Financial Literacy and Financial Inclusion (edição 2022, publicada em 27/03/2022) | OCDE · <https://www.oecd.org/en/publications/oecd-infe-toolkit-for-measuring-financial-literacy-and-financial-inclusion-2022_cbc4114f-en.html> | Internacional · metodologia | PDF / web | Público (web) | Página sem informação de licença; consultar os termos da OCDE antes de reproduzir itens | 27/10/2026 (página aberta) | Referência metodológica (conhecimento, comportamento e atitude). As perguntas do questionário são de redação própria. Existe uma edição mais recente (2026), a conferir |
| F8 | PISA 2022, Vol. IV (letramento financeiro) | OCDE · <https://www.oecd.org/en/publications/pisa-2022-results-volume-iv_5a849c2a-en.html> (link do inventário anterior da equipe) | Internacional, jovens de 15 anos. Brasil: 45,1% abaixo do nível 2 (valor do inventário anterior, **a reconferir**) | Relatório HTML/PDF | Público | Direitos da OCDE: citar; não versionar o PDF, só os valores usados (conforme inventário anterior) | Não reaberto em 27/10/2026 | Contexto (já citado na Entrega 3) |

**Referência normativa (não é base de dados):** Resolução CNS nº 510/2016 e Ofício Circular CONEP nº 17/2022 (orientações sobre o art. 1º), usados para decidir o enquadramento ético da pesquisa: <https://fcfrp.usp.br/wp-content/uploads/sites/528/2024/12/Oficio-Circular-17-2022.pdf>. A equipe deve **confirmar com o professor** se o enquadramento como pesquisa de opinião com participantes não identificados dispensa análise do sistema CEP/CONEP no contexto da disciplina.

## 3. Unidades, chaves e junções

| Tabela | Unidade de análise | Chave | Periodicidade | Junções possíveis |
|---|---|---|---|---|
| `data/glossario.json` | Um verbete | `slug(termo)` (termo sem acentos, em minúsculas, com hífens) | Contínua: atualizada a cada novo verbete | `relacionados` aponta para outros `termo` da própria tabela. `tema` agrupa verbetes |
| Respostas do questionário (`data/raw/`, não versionado) | Um respondente anônimo | `id_resposta` (número sequencial gerado no tratamento; **sem** vínculo com pessoa) | Coleta única, de 01/11 a 20/11/2026 | Não há junção entre respondentes e outras bases. Cada resposta é independente |
| Tabelas agregadas (`data/processed/`) | Pergunta × categoria de resposta (e grupo, quando houver) | `variavel` + `categoria` (+ `grupo`) | Gerada após o fechamento da coleta | Junção **analítica** com o glossário pelo campo `tema`: o conceito avaliado em cada pergunta corresponde a um tema/termo do glossário (ver `docs/questionario.md`) |

## 4. Dicionário preliminar de variáveis

### 4.1 Glossário (`data/glossario.json`)

| Variável | Descrição | Tipo | Unidade | Fonte / cobertura |
|---|---|---|---|---|
| `termo` | Nome do verbete (obrigatório) | Texto | — | Equipe / lista de demandas do CORECON-PB |
| `tema` | Grupo temático, usado no filtro do site | Texto (categórica) | — | Equipe |
| `definicao` | Explicação em linguagem simples | Texto | — | Equipe, conferida em F4–F6 |
| `exemplo` | Exemplo do cotidiano | Texto | — | Equipe |
| `importa` | Por que o conceito é relevante | Texto | — | Equipe |
| `relacionados` | Lista de termos relacionados | Lista de texto | — | Equipe |
| `fonte` | Fonte usada para conferir o verbete (opcional) | Texto | — | Equipe |

### 4.2 Questionário (variáveis essenciais)

Redação exata das perguntas e opções: [`questionario.md`](questionario.md).

| Variável | Descrição | Tipo | Unidade / categorias | Fonte / cobertura |
|---|---|---|---|---|
| `a1_curso` | Curso de graduação | Categórica | Lista de cursos | F1 |
| `a2_periodo` | Faixa de período cursado | Categórica | 1º–4º, 5º–8º, 9º ou mais | F1 |
| `a3_idade` | Faixa etária | Categórica | 18–20, 21–23, 24–26, 27 ou mais | F1 |
| `a4_ocupacao` | Situação de estudo e trabalho | Categórica | Só estuda; estuda e trabalha ou estagia; outra | F1 |
| `a5_renda_propria` | Renda própria mensal (opcional) | Categórica ordinal | Faixas em salários mínimos; "prefiro não responder" | F1 |
| `b1_reserva_def` | Escolha da definição de reserva de emergência | Categórica | Correta / incorreta / não sei | F1 |
| `b2_reserva_meses` | Quantos meses de despesas o respondente acha adequado guardar como reserva | Categórica | Faixas de meses; **não pontuada** (nenhuma fonte oficial consultada traz um número único). Só distribuição | F1 |
| `b3_inflacao` | Item sobre inflação e poder de compra | Categórica | Correta / incorreta / não sei | F1 |
| `b4_juros_compostos` | Item sobre dívida com juros compostos | Categórica | Correta / incorreta / não sei | F1 |
| `b5_diversificacao` | Item sobre risco e diversificação | Categórica | Correta / incorreta / não sei | F1 |
| `b6_autoavaliacao` | Autoavaliação do conhecimento financeiro | Ordinal | 1 a 5 | F1 |
| `escore_conhecimento` | Soma dos acertos em b1, b3, b4 e b5 | Numérica | Pontos, 0 a 4 | Calculada |
| `nivel_conhecimento` | Faixa do escore | Ordinal | Baixo (0–1) / médio (2–3) / alto (4); cortes propostos, **a confirmar** | Calculada |
| `c1_orcamento` | Frequência com que faz orçamento | Ordinal | Nunca / às vezes / sempre | F1 |
| `c2_tem_reserva` | Possui reserva de emergência | Categórica | Sim / parcial / não | F1 |
| `c3_reserva_cobertura` | Meses de despesas que a reserva cobre | Ordinal | Menos de 1; 1–3; 3–6; mais de 6 (só quem tem reserva) | F1 |
| `c4_onde_guarda` | Onde guarda o dinheiro da reserva | Categórica múltipla | Poupança, renda fixa, conta corrente, dinheiro em casa, outro | F1 |
| `c5_dividas` | Tipos de dívida que possui | Categórica múltipla | Cartão, empréstimo, parcelas atrasadas, nenhuma, prefiro não responder | F1 |
| `c6_poupa_regular` | Guarda parte da renda regularmente | Categórica | Sim / às vezes / não | F1 |
| `d1_renda_familiar` | Renda familiar mensal (opcional) | Categórica ordinal | Faixas em salários mínimos; "não sei"; "prefiro não responder" | F1 |
| `d2_fam_conversa` | Frequência de conversas sobre dinheiro em casa | Ordinal | Nunca / às vezes / frequentemente | F1 |
| `d3_fam_orcamento` | A família controla o orçamento | Categórica | Sim / não / não sei | F1 (relato do estudante) |
| `d4_fam_reserva` | A família tem reserva de emergência | Categórica | Sim / não / não sei | F1 (relato do estudante) |
| `d5_fam_dividas` | Família com dívidas em atraso | Categórica | Sim / não / não sei / prefiro não responder | F1 (relato do estudante) |
| `d6_fam_conhecimento` | Nível de conhecimento financeiro percebido na família | Ordinal | 1 a 5 / não sei | F1 (relato do estudante) |
| `d7_educ_recebida` | Onde já teve contato com educação financeira | Categórica múltipla | Escola, família, curso, internet, nunca | F1 |
| `e1_temas_interesse` | Temas de interesse para o glossário | Categórica múltipla | Lista de temas | F1 |
| `e2_usaria_glossario` | Usaria um glossário online | Categórica | Sim / talvez / não | F1 |
| `e3_termo_dificil` | Termo que gostaria de ver explicado (resposta curta, sem dados pessoais) | Texto | — | F1 |

Os **códigos válidos de cada resposta** (o contrato entre o formulário e o tratamento) estão em [`outputs/livro_de_codigos.csv`](../outputs/livro_de_codigos.csv).

**Limite importante:** as variáveis `d3` a `d6` são o **relato do estudante** sobre a família, não uma medida feita com a própria família. As conclusões sobre "o que as famílias sabem" devem dizer isso.

### 4.3 Tabelas tratadas (Entrega 5)

Geradas por [`notebooks/03_obtencao_limpeza_tratamento.ipynb`](../notebooks/03_obtencao_limpeza_tratamento.ipynb). Cada variável ocupa uma coluna, cada observação uma linha e cada tipo de unidade uma tabela.

| Tabela (`data/processed/`) | Unidade (1 linha =) | Chave | Variáveis |
|---|---|---|---|
| `glossario_verbetes.csv` | Um verbete | `slug` | `termo`, `slug`, `tema`, `definicao`, `exemplo`, `importa`, `fonte` (texto); `n_relacionados`, `n_caracteres_definicao` (inteiro); `tem_exemplo`, `tem_importa`, `tem_fonte` (lógico) |
| `glossario_relacoes.csv` | Uma relação "Veja também" | `slug_origem` + `slug_destino` | `termo_origem`, `termo_destino` (texto); `destino_existe`, `reciproca` (lógico, derivadas) |
| `glossario_cobertura_questionario.csv` | Um par item do questionário × verbete necessário | `item_questionario` + `slug` | `verbete_necessario` (texto); `existe_no_glossario` (lógico) |
| `frequencias.csv`, `escore_distribuicao.csv`, `cruzamentos.csv`, `escore_medio_por_grupo.csv` | Pergunta × categoria (e grupo) | `variavel` + `categoria` (+ grupo) | `n` (inteiro ou `<5`), `pct`, `base`. **Só existem em `data/processed/` depois da coleta real** |

Relatório de qualidade, funil de contagens e testes: `outputs/relatorio_qualidade.csv`, `outputs/funil_contagens.csv`, `outputs/testes_integridade.csv`. Até a aplicação do questionário, o notebook testa as regras com uma base **sintética** e grava o resultado em `outputs/sintetico_teste/` (nunca em `data/processed/`).

## 5. Plano de aquisição

| Fonte | Método de obtenção | Arquivo / endpoint | Frequência | Parâmetros | Responsável | Data prevista | Atualização |
|---|---|---|---|---|---|---|---|
| F1 Questionário | Aplicação online anônima, divulgada por turmas e canais dos cursos **[a confirmar]**; exportar CSV ao fechar | `data/raw/respostas_questionario.csv` (local, não versionado) | Coleta única | Público: graduandos maiores de 18 anos; janela de coleta 01/11 a 20/11/2026; meta de respostas **[a confirmar]** | Gabriel e Arthur | Formulário pronto antes de 01/11/2026 **[a confirmar]**; coleta de 01/11 a 20/11/2026 | Sem atualização após o fechamento; nova rodada só com decisão da equipe |
| F1 Tratamento | Script que remove carimbo de data/hora, gera `id_resposta`, calcula escore e nível e produz tabelas agregadas | `notebooks/03_obtencao_limpeza_tratamento.ipynb` (limpeza e validação; reutiliza as funções de agregação de `notebooks/02_tratamento_questionario.py`) → `data/processed/` (testado só com dados sintéticos) | Uma vez, após o fechamento | Células com menos de 5 respondentes são suprimidas ("<5") | Gabriel e Arthur | 01/12 a 04/12/2026 | Reexecutar o script se o CSV mudar |
| F2 Glossário | Redação dos verbetes e conferência em F4–F6 | `data/glossario.json` | Contínua até a entrega final | Validação com `notebooks/01_validar_glossario.py` | Todos | Versão revisada em 05/12/2026 | Ao incluir ou alterar verbete, rodar a validação |
| F3 Lista de demandas | Solicitar ou confirmar a lista com o CORECON-PB | Documento institucional (não versionado por padrão) | Única | — | Ana | 03/11/2026 | Pedir nova versão se o CORECON atualizar |
| F4–F8 Referências | Acesso manual aos links do inventário; registrar data de acesso e licença | Links da seção 2 | Única, com releitura antes da banca | — | Todos | 03/11/2026 | Conferir se os links continuam ativos antes de 15/12/2026 |

## 6. Segurança e proteção de dados

- **Não versionar:** respostas individuais, carimbos de data/hora, e-mails, nomes, matrículas, documentos internos do CORECON-PB, senhas, tokens e chaves. O `.gitignore` bloqueia `data/raw/*`, `respostas*.csv`, `.env*`, chaves e credenciais.
- O questionário **não pergunta** nome, e-mail, CPF nem matrícula. Perguntas sensíveis (renda, dívidas da família) são **opcionais**, com "prefiro não responder".
- Só entram no repositório tabelas **agregadas**, sem células com menos de 5 respondentes.
- Respostas abertas (`e3_termo_dificil`) devem ser revisadas manualmente e qualquer dado pessoal removido antes de qualquer publicação.
- Participação restrita a maiores de 18 anos, voluntária, com consentimento no início do formulário.

## 7. Pendências

1. Definir a meta de respostas (população definida pela equipe: graduandos de Ciências Econômicas; coleta de 01/11 a 20/11/2026).
2. Confirmar com o professor o enquadramento ético (plataforma: Google Forms).
3. Receber ou confirmar a lista de demandas do CORECON-PB e escolher os termos do glossário.
4. Confirmar os responsáveis e prazos propostos (ver [`tarefas.md`](tarefas.md)).
5. Abrir e ler integralmente F4 e F8 e reconferir os valores do PISA; checar os termos de uso da OCDE antes de reproduzir qualquer item.
6. Se a equipe quiser pontuar `b2_reserva_meses`, encontrar uma fonte oficial com número de meses (as consultadas em 27/10/2026 não trazem).
