# TPAEII_equipe01

Projeto aplicado de extensão da disciplina **PSAE00320 – Técnicas de Pesquisa e Análise Econômica II** (Turma 01, 2026.2, UFPB), em parceria com o **CORECON-PB** (Conselho Regional de Economia da Paraíba).

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

1. **Glossário da Economia** (site): termos da economia explicados em linguagem simples, para a população em geral.
2. **Pesquisa com estudantes de graduação** (questionário): diagnóstico de quanto os graduandos sabem e praticam de educação financeira (em especial reserva de emergência) e qual é o contexto financeiro e o nível de conhecimento de suas famílias. Os resultados orientam quais termos e temas o glossário deve priorizar.

> **Histórico:** o projeto começou como educação financeira em escolas de João Pessoa (Entregas 1 a 3) e, em 22/10/2026, passou a ser o glossário. A pesquisa com graduandos foi incorporada em 27/10/2026. Veja [`docs/entregas.md`](docs/entregas.md).

### Pergunta da pesquisa

> Quanto os estudantes de graduação sabem e aplicam de educação financeira (em especial reserva de emergência), e qual o contexto e o nível de conhecimento financeiro de suas famílias?

Detalhes do instrumento: [`docs/questionario.md`](docs/questionario.md).

## Estrutura do repositório

```
README.md                  este arquivo
.gitignore                 bloqueia dados brutos, credenciais e arquivos temporários
requirements.txt           dependências dos scripts (pandas)
index.html                 site do glossário (página única, sem dependências)
data/
  glossario.json           verbetes do glossário (lido pelo site)
  raw/                     dados originais permitidos (ver data/raw/README.md)
  processed/               dados tratados e agregados, sem informação pessoal
notebooks/
  01_validar_glossario.py        valida o glossário
  02_tratamento_questionario.py  funções de agregação do questionário (usadas pelo notebook 03)
  03_obtencao_limpeza_tratamento.ipynb  Entrega 5: obtenção, limpeza, validação e exportação
  arquivo/                       script do projeto anterior (escolas)
docs/                      plano de dados, questionário, histórico e tarefas
  arquivo/escolas/         material do projeto anterior, preservado
outputs/                   relatório de qualidade, funil, testes, livro de códigos
  sintetico_teste/         teste das regras com dados SINTÉTICOS (não é resultado)
```

## Documentação

| Documento | Conteúdo |
|---|---|
| [`docs/plano-de-dados.md`](docs/plano-de-dados.md) | Inventário de fontes, unidades e chaves, dicionário de variáveis, plano de aquisição e segurança (Entrega 4) |
| [`docs/questionario.md`](docs/questionario.md) | Questionário, termo de consentimento, indicadores e plano de análise |
| [`docs/E04_equipe01_plano_dados.pdf`](docs/E04_equipe01_plano_dados.pdf) | PDF de síntese do plano de dados, no formato pedido para a submissão da Entrega 4 |
| [`docs/E05_equipe01_qualidade_dados.pdf`](docs/E05_equipe01_qualidade_dados.pdf) | Relatório de qualidade dos dados (Entrega 5) |
| [`docs/entregas.md`](docs/entregas.md) | Histórico das entregas 1 a 4 e decisões da equipe |
| [`docs/tarefas.md`](docs/tarefas.md) | Tarefas com responsável, prazo e situação |
| [`docs/arquivo/escolas/`](docs/arquivo/escolas/README.md) | Projeto anterior (educação financeira em escolas): E03, inventário, chaves, aquisição e dicionário, preservados para histórico |

## Como rodar

**Site do glossário.** O site lê `data/glossario.json` com `fetch`, então precisa de um servidor local (abrir o arquivo direto no navegador não funciona):

```bash
python3 -m http.server 8000
# abra http://localhost:8000
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
- Para o **questionário**, coloque o CSV exportado do formulário em `data/raw/respostas_questionario.csv` (fica fora do Git) e reexecute. **Sem esse arquivo, o notebook usa uma base sintética só para testar as regras** e grava em `outputs/sintetico_teste/`. Quando for usar dados reais, apague essa pasta para não confundir.
- Os códigos de resposta que o formulário deve exportar estão em `outputs/livro_de_codigos.csv`.
- As tabelas agregadas só entram em `data/processed/` com dados reais; células com menos de 5 respondentes aparecem como `<5`.

## Segurança e ética

- Nunca versionar senhas, tokens, chaves, dados pessoais, documentos internos ou bases restritas.
- As respostas individuais do questionário ficam **fora do repositório** (`data/raw/` é ignorado pelo Git). Só entram em `data/processed/` tabelas agregadas, sem identificação.
- O questionário é anônimo e voluntário, com consentimento no início. Não coleta nome, e-mail, CPF nem matrícula.

## Status

Em andamento. Entrega final com banca no CORECON-PB em **15/12/2026**.

| Parte | Situação |
|---|---|
| Estrutura do repositório e plano de dados (Entrega 4) | Pronta, com o PDF `docs/E04_equipe01_plano_dados.pdf`; faltam o acesso do professor e o envio |
| Glossário (site) | Funcionando, com 6 verbetes de rascunho; faltam os demais termos |
| Questionário | Rascunho em `docs/questionario.md`; ainda não aplicado |
| Tratamento dos dados (Entrega 5) | Notebook executável e reprodutível; glossário tratado (dado real); regras do questionário testadas só com dados sintéticos |

## Contato acadêmico

Prof. Alessio · Curso de Ciências Econômicas, Universidade Federal da Paraíba (UFPB). 
Email abeatriz.laurentino@gmail.com
