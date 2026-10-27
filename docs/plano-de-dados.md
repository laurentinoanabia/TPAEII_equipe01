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

Status geral: os links abaixo foram **localizados por busca em 27/10/2026**. A leitura integral e a verificação da licença de uso ainda estão pendentes, por isso a coluna "Licença" traz "a verificar" onde não há confirmação.

| # | Base | Instituição / link | Cobertura | Formato | Acesso | Licença | Data de acesso | Uso no projeto |
|---|---|---|---|---|---|---|---|---|
| F1 | Questionário próprio | Equipe 01 · plataforma **[a confirmar]** (ex.: formulário online) | Graduandos **[a confirmar: UFPB inteira ou só Economia]** · coleta em nov/2026 (proposta) | CSV exportado | Coleta própria, anônima e voluntária | Dados da equipe; divulgação **somente agregada** | — (coleta ainda não iniciada) | Base da pesquisa |
| F2 | Verbetes do glossário | Elaboração da equipe · `data/glossario.json` | Termos escolhidos a partir da lista de demandas do CORECON-PB **[a confirmar a lista]** | JSON | Repositório | Autoria da equipe | 27/10/2026 | Conteúdo do site |
| F3 | Lista de demandas do CORECON-PB | CORECON-PB (documento recebido pela equipe) | **[a registrar]** | **[a registrar]** | Documento institucional | **[a verificar]** se pode ser versionado; por padrão **não** vai ao repositório | **[a registrar]** | Origem dos termos do glossário |
| F4 | Caderno de Cidadania Financeira | Banco Central do Brasil · <https://www.bcb.gov.br/pre/pef/port/caderno_cidadania_financeira.pdf> | Nacional · conceitos de educação e cidadania financeira | PDF | Público (web) | A verificar | 27/10/2026 (link localizado) | Conferência de conceitos dos verbetes |
| F5 | Estratégia Nacional de Educação Financeira (ENEF) | Banco Central · <https://www.bcb.gov.br/pre/pef/PORT/enef.asp?frame=1> | Nacional | Página web | Público (web) | A verificar | 27/10/2026 (link localizado) | Contexto e referência institucional |
| F6 | Plano Diretor da ENEF | gov.br/investidor · <https://www.gov.br/investidor/pt-br/educacional/plano-diretor-enef-estrategia-nacional-de-educacao-financeira.pdf/@@display-file/file> | Nacional | PDF | Público (web) | A verificar | 27/10/2026 (link localizado) | Referência de temas e conteúdos |
| F7 | OECD/INFE Toolkit for Measuring Financial Literacy and Financial Inclusion (edição 2022) | OCDE · <https://www.oecd.org/en/publications/oecd-infe-toolkit-for-measuring-financial-literacy-and-financial-inclusion-2022_cbc4114f-en.html> | Internacional · metodologia | PDF / web | Público (web) | A verificar | 27/10/2026 (link localizado) | Referência metodológica para os blocos de conhecimento, comportamento e atitude do questionário. Existe uma edição mais recente (2026), a conferir |
| F8 | PISA 2022 – letramento financeiro | OCDE / Inep | Internacional, jovens de 15 anos | **[a registrar]** | Público | A verificar | **[a registrar]** | Contexto (já citado na Entrega 3) |

**Referência normativa (não é base de dados):** Resolução CNS nº 510/2016 e Ofício Circular CONEP nº 17/2022 (orientações sobre o art. 1º), usados para decidir o enquadramento ético da pesquisa: <https://fcfrp.usp.br/wp-content/uploads/sites/528/2024/12/Oficio-Circular-17-2022.pdf>. A equipe deve **confirmar com o professor** se o enquadramento como pesquisa de opinião com participantes não identificados dispensa análise do sistema CEP/CONEP no contexto da disciplina.

## 3. Unidades, chaves e junções

| Tabela | Unidade de análise | Chave | Periodicidade | Junções possíveis |
|---|---|---|---|---|
| `data/glossario.json` | Um verbete | `slug(termo)` (termo sem acentos, em minúsculas, com hífens) | Contínua: atualizada a cada novo verbete | `relacionados` aponta para outros `termo` da própria tabela. `tema` agrupa verbetes |
| Respostas do questionário (`data/raw/`, não versionado) | Um respondente anônimo | `id_resposta` (número sequencial gerado no tratamento; **sem** vínculo com pessoa) | Coleta única, em janela de datas **[a confirmar]** | Não há junção entre respondentes e outras bases. Cada resposta é independente |
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
| `b2_reserva_meses` | Meses de despesas recomendados como reserva | Categórica | Faixas; gabarito **[a confirmar nas fontes F4–F6]** | F1 |
| `b3_inflacao` | Item sobre inflação e poder de compra | Categórica | Correta / incorreta / não sei | F1 |
| `b4_juros_compostos` | Item sobre dívida com juros compostos | Categórica | Correta / incorreta / não sei | F1 |
| `b5_diversificacao` | Item sobre risco e diversificação | Categórica | Correta / incorreta / não sei | F1 |
| `b6_autoavaliacao` | Autoavaliação do conhecimento financeiro | Ordinal | 1 a 5 | F1 |
| `escore_conhecimento` | Soma dos acertos em b1, b3, b4 e b5 (e b2, se confirmado) | Numérica | Pontos, 0 a 4 (ou 5) | Calculada |
| `nivel_conhecimento` | Faixa do escore | Ordinal | Baixo / médio / alto (cortes **[a confirmar]**) | Calculada |
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

**Limite importante:** as variáveis `d3` a `d6` são o **relato do estudante** sobre a família, não uma medida feita com a própria família. As conclusões sobre "o que as famílias sabem" devem dizer isso.

## 5. Plano de aquisição

| Fonte | Método de obtenção | Arquivo / endpoint | Frequência | Parâmetros | Responsável | Data prevista | Atualização |
|---|---|---|---|---|---|---|---|
| F1 Questionário | Aplicação online anônima, divulgada por turmas e canais dos cursos **[a confirmar]**; exportar CSV ao fechar | `data/raw/respostas_questionario.csv` (local, não versionado) | Coleta única | Público: graduandos maiores de 18 anos; janela de coleta **[a confirmar]**; meta de respostas **[a confirmar]** | **[a definir]** | Aplicação a partir de 04/11/2026 (proposta) | Sem atualização após o fechamento; nova rodada só com decisão da equipe |
| F1 Tratamento | Script que remove carimbo de data/hora, gera `id_resposta`, calcula escore e nível e produz tabelas agregadas | `notebooks/02_tratamento_questionario.py` **[a criar]** → `data/processed/` | Uma vez, após o fechamento | Células com menos de 5 respondentes são agrupadas ou omitidas | **[a definir]** | 18/11/2026 (proposta) | Reexecutar o script se o CSV mudar |
| F2 Glossário | Redação dos verbetes e conferência em F4–F6 | `data/glossario.json` | Contínua até a entrega final | Validação com `notebooks/01_validar_glossario.py` | **[a definir]** | Versão revisada em 05/12/2026 (proposta) | Ao incluir ou alterar verbete, rodar a validação |
| F3 Lista de demandas | Solicitar ou confirmar a lista com o CORECON-PB | Documento institucional (não versionado por padrão) | Única | — | **[a definir]** | **[a definir]** | Pedir nova versão se o CORECON atualizar |
| F4–F8 Referências | Acesso manual aos links do inventário; registrar data de acesso e licença | Links da seção 2 | Única, com releitura antes da banca | — | **[a definir]** | 03/11/2026 (proposta) | Conferir se os links continuam ativos antes de 15/12/2026 |

## 6. Segurança e proteção de dados

- **Não versionar:** respostas individuais, carimbos de data/hora, e-mails, nomes, matrículas, documentos internos do CORECON-PB, senhas, tokens e chaves. O `.gitignore` bloqueia `data/raw/*`, `respostas*.csv`, `.env*`, chaves e credenciais.
- O questionário **não pergunta** nome, e-mail, CPF nem matrícula. Perguntas sensíveis (renda, dívidas da família) são **opcionais**, com "prefiro não responder".
- Só entram no repositório tabelas **agregadas**, sem células com menos de 5 respondentes.
- Respostas abertas (`e3_termo_dificil`) devem ser revisadas manualmente e qualquer dado pessoal removido antes de qualquer publicação.
- Participação restrita a maiores de 18 anos, voluntária, com consentimento no início do formulário.

## 7. Pendências

1. Definir a população (UFPB inteira ou só Economia) e a meta de respostas.
2. Confirmar com o professor o enquadramento ético e a plataforma do formulário.
3. Receber ou confirmar a lista de demandas do CORECON-PB e escolher os termos do glossário.
4. Definir responsáveis e prazos (ver [`tarefas.md`](tarefas.md)).
5. Verificar licença de uso e ler integralmente as fontes F4–F8.
6. Confirmar o gabarito do item `b2_reserva_meses` nas fontes oficiais.
