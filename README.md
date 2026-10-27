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
index.html                 site do glossário (página única, sem dependências)
data/
  glossario.json           verbetes do glossário (lido pelo site)
  raw/                     dados originais permitidos (ver data/raw/README.md)
  processed/               dados tratados e agregados, sem informação pessoal
notebooks/                 aquisição, tratamento e análise (scripts em Python)
docs/                      plano de dados, questionário, histórico e tarefas
outputs/                   tabelas, gráficos e produtos finais
```

## Documentação

| Documento | Conteúdo |
|---|---|
| [`docs/plano-de-dados.md`](docs/plano-de-dados.md) | Inventário de fontes, unidades e chaves, dicionário de variáveis, plano de aquisição e segurança (Entrega 4) |
| [`docs/questionario.md`](docs/questionario.md) | Questionário, termo de consentimento, indicadores e plano de análise |
| [`docs/entregas.md`](docs/entregas.md) | Histórico das entregas 1 a 4 e decisões da equipe |
| [`docs/tarefas.md`](docs/tarefas.md) | Tarefas com responsável, prazo e situação |

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

## Segurança e ética

- Nunca versionar senhas, tokens, chaves, dados pessoais, documentos internos ou bases restritas.
- As respostas individuais do questionário ficam **fora do repositório** (`data/raw/` é ignorado pelo Git). Só entram em `data/processed/` tabelas agregadas, sem identificação.
- O questionário é anônimo e voluntário, com consentimento no início. Não coleta nome, e-mail, CPF nem matrícula.

## Status

Em andamento. Entrega final com banca no CORECON-PB em **15/12/2026**.
