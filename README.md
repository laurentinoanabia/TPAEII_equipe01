# TPAEII_equipe01

Projeto aplicado de extensão da disciplina **PSAE00320 – Técnicas de Pesquisa e Análise Econômica II** (Turma 01, 2026.2, UFPB), desenvolvido a partir de uma demanda apresentada pelo **CORECON-PB** (Conselho Regional de Economia da Paraíba).

> **Autoria e vínculo.** O CORECON-PB apresentou a demanda. A pesquisa, o site e todo o conteúdo são de autoria da equipe; o site não é material oficial do Conselho, não usa a sua identidade visual e não tem a sua chancela.

## Equipe

| Integrante | Papel |
|---|---|
| Ana Beatriz Laurentino | Equipe 01 |
| Arthur Almeida | Equipe 01 |
| Gabriel Pinheiro | Equipe 01 |
| Alessio | Orientador |

## Problema e demandante

O CORECON-PB apoia o programa **"PB sem dívidas"** e precisa de materiais que levem conhecimento econômico e educação financeira à população, com acessibilidade.

O projeto tem **dois produtos complementares**:

1. **Glossário da Economia** (site): plataforma de educação econômica e financeira em linguagem simples, com prioridade para orçamento, dívidas e reserva de emergência (os temas da pesquisa), e aprofundamento em juros, inflação, Selic, macroeconomia e investimentos. Tem enciclopédia, glossário A–Z, 10 simuladores, 9 trilhas e quiz.
2. **Pesquisa com estudantes de graduação** (questionário publicado no [Google Forms](https://docs.google.com/forms/d/e/1FAIpQLSel8h8rKd4svyMe79V1ME_7TQSW466HPaT5WGMpb-kU3PNWgg/viewform)): diagnóstico de quanto os graduandos sabem e praticam de educação financeira (em especial reserva de emergência) e qual é o contexto financeiro e o nível de conhecimento de suas famílias. Os resultados orientam quais termos e temas o glossário deve priorizar.

> **Histórico:** o projeto começou como educação financeira em escolas de João Pessoa (Entregas 1 a 3) e, em 22/10/2026, passou a ser o glossário. A pesquisa com graduandos foi incorporada em 27/10/2026. Veja [`docs/entregas.md`](docs/entregas.md).

### Pergunta da pesquisa

> Quanto os estudantes de graduação sabem e aplicam de educação financeira (em especial reserva de emergência), e qual o contexto e o nível de conhecimento financeiro de suas famílias?

Detalhes do instrumento: [`docs/questionario.md`](docs/questionario.md).

## Estrutura do repositório

```
README.md                  este arquivo
.gitignore                 bloqueia dados brutos, credenciais e arquivos temporários
requirements.txt           dependências dos scripts (pandas, matplotlib, scipy)
index.html                 site do glossário (página única, sem dependências; lê data/*.json)
site_unico/               versão do site em um único arquivo, com os dados embutidos (gerada; abre sem servidor)
scripts/montar_site_unico.py  gera site_unico/ a partir de index.html e data/
data/
  glossario.json           verbetes do glossário (lido pelo site e pelo notebook 03)
  trilhas.json, quiz.json  trilhas de aprendizagem e perguntas do quiz do site
  indicadores.json         faixa de indicadores do site (valores com data e fonte; atualizar à mão)
  projeto.json             dados institucionais exibidos no site (equipe, repositório)
  raw/                     dados originais permitidos (ver data/raw/README.md)
  processed/               dados tratados e agregados, sem informação pessoal
notebooks/
  01_validar_glossario.py        valida o glossário
  02_tratamento_questionario.py  funções de agregação do questionário (usadas pelo notebook 03)
  02a_formulario_google.py       traduz a exportação do Google Forms (texto das opções) para os códigos do tratamento
  03_obtencao_limpeza_tratamento.ipynb  Entrega 5: obtenção, limpeza, validação e exportação
  04_analise_e06.py              Entrega 6: análise descritiva preliminar (tabelas e figuras agregadas)
  arquivo/                       script do projeto anterior (escolas)
docs/                      plano de dados, questionário, histórico e tarefas
  arquivo/escolas/         material do projeto anterior, preservado
outputs/                   relatório de qualidade, funil, testes, livro de códigos e mapa do formulário
  e06/                     tabelas (CSV) e figuras (PNG) agregadas da Entrega 6, geradas por notebooks/04_analise_e06.py
```

## Documentação

| Documento | Conteúdo |
|---|---|
| [`docs/plano-de-dados.md`](docs/plano-de-dados.md) | Inventário de fontes, unidades e chaves, dicionário de variáveis, plano de aquisição e segurança (Entrega 4) |
| [`docs/questionario.md`](docs/questionario.md) | Questionário publicado no Google Forms, termo de consentimento, indicadores e plano de análise |
| [`docs/E04_equipe01_plano_dados.pdf`](docs/E04_equipe01_plano_dados.pdf) | PDF de síntese do plano de dados, no formato pedido para a submissão da Entrega 4 |
| [`docs/E05_equipe01_qualidade_dados.pdf`](docs/E05_equipe01_qualidade_dados.pdf) | Relatório de qualidade dos dados (Entrega 5). Gerado a partir dos CSV de `outputs/` por `docs/gerar_e05_relatorio.py` (opcional; exige `python-docx` e `wkhtmltopdf`); há também a versão `.docx` |
| [`docs/entregas.md`](docs/entregas.md) | Histórico das entregas 1 a 4 e decisões da equipe |
| [`docs/tarefas.md`](docs/tarefas.md) | Tarefas com responsável, prazo e situação |
| [`docs/arquivo/escolas/`](docs/arquivo/escolas/README.md) | Projeto anterior (educação financeira em escolas): E03, inventário, chaves, aquisição e dicionário, preservados para histórico |

## Como rodar

**Site do glossário.** O `index.html` lê os arquivos de `data/` com `fetch`, então precisa de um servidor local ou do GitHub Pages (abrir o arquivo direto no navegador não funciona):

```bash
python3 -m http.server 8000
# abra http://localhost:8000
```

Para uma versão que abre com dois cliques (sem servidor), gere o arquivo único depois de mudar `index.html` ou `data/`:

```bash
python3 scripts/montar_site_unico.py   # cria site_unico/glossario-da-economia.html
```

**Validar o glossário** (campos obrigatórios, termos duplicados, links "Veja também" quebrados):

```bash
python3 notebooks/01_validar_glossario.py
```

**Obter, limpar e tratar os dados (Entrega 5).** Exige `pip install -r requirements.txt`. Executa do início ao fim, sem intervenção manual:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/03_obtencao_limpeza_tratamento.ipynb
```

- O **glossário** é sempre tratado (dado real) e gera 3 tabelas em `data/processed/`.
- Para o **questionário**, baixe as respostas do Google Forms em CSV (aba *Respostas*), salve em `data/raw/respostas_questionario.csv` (fica fora do Git), sem editar, e reexecute. O notebook traduz o texto das opções para códigos (as caixas de seleção vêm separadas por `;` e as duas redações do formulário são reconhecidas). **Sem esse arquivo, o notebook usa uma base sintética só para testar as regras** e grava em `outputs/sintetico_teste/` (pasta removida do repositório desde que os dados reais foram tratados).
- A tradução pergunta/opção do formulário → variável/código está em `outputs/mapa_formulario.csv`; os códigos válidos, em `outputs/livro_de_codigos.csv`. Se o formulário mudar, atualize `QUESTOES` em `notebooks/02a_formulario_google.py`.
- As tabelas agregadas só entram em `data/processed/` com dados reais; células com menos de 5 respondentes aparecem como `<5`.

**Análise preliminar (Entrega 6).** Com o arquivo real em `data/raw/respostas_questionario.csv`:

```bash
python3 notebooks/04_analise_e06.py
```

Grava em `outputs/e06/tabelas/` (CSV agregados, contagens menores que 5 como `<5`) e `outputs/e06/figuras/` (PNG usados no relatório). O escore principal soma os acertos em b1, b3, b4 e b5 (0 a 4); o Big Three (b3, b4, b5) e a nota de 0 a 6 aparecem como medidas de apoio. Os testes estatísticos são exploratórios.

## Segurança e ética

- Nunca versionar senhas, tokens, chaves, dados pessoais, documentos internos ou bases restritas.
- As respostas individuais do questionário ficam **fora do repositório** (`data/raw/` é ignorado pelo Git). Só entram em `data/processed/` tabelas agregadas, sem identificação.
- O questionário é anônimo e voluntário, com consentimento no início. Não coleta nome, e-mail, CPF nem matrícula.

## Status

Em andamento. Entrega final com banca no CORECON-PB em **15/12/2026**.

| Parte | Situação |
|---|---|
| Estrutura do repositório e plano de dados (Entrega 4) | Pronta, com o PDF `docs/E04_equipe01_plano_dados.pdf`; faltam o acesso do professor e o envio |
| Glossário (site) | Versão atual no repositório desde 25/11/2026: 121 verbetes, todos com fonte; 12 de dívidas e 6 de planejamento financeiro; trilha "Dívidas sob controle". **Falta a revisão da equipe**: os verbetes aparecem como "Em revisão" até receberem `revisado` |
| Questionário | Coleta encerrada: **60 respostas, de 28/10 a 15/11/2026** (a coleta estava prevista até 20/11, mas a última resposta é de 15/11; base final conferida em 25/11/2026). O formulário foi editado durante a coleta (entre 02/11 e 05/11): 8 respostas na versão 1 e 52 na versão 2. Detalhes em `docs/questionario.md` |
| Tratamento dos dados (Entregas 5 e 6) | Notebook 03 executado com as respostas reais em 25/11/2026: 60 → 60 linhas, 0 códigos inválidos, todos os testes de integridade OK; tabelas agregadas em `data/processed/`. Análise preliminar da Entrega 6 em `notebooks/04_analise_e06.py` → `outputs/e06/` (escore principal de 0 a 4, decisão da equipe em 25/11/2026) |

## Uso de inteligência artificial

Parte dos textos e do código do site foi produzida com apoio de ferramentas de inteligência artificial generativa, a partir de instruções escritas pela equipe, e o reposicionamento de 25/11/2026 também. As fontes de cada verbete estão no próprio verbete. Nenhum verbete está marcado como revisado: a revisão do conteúdo pela equipe é uma pendência (tarefa 12).

## Contato acadêmico

Prof. Alessio · Curso de Ciências Econômicas, Universidade Federal da Paraíba (UFPB). 
Email abeatriz.laurentino@gmail.com
