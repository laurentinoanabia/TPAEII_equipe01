# data/processed/

Dados tratados e **agregados**, sem informação pessoal. Aqui podem ser versionados:

- tabelas de frequência por pergunta (contagens e percentuais);
- cruzamentos agregados (por exemplo, nível de conhecimento por grupo);
- versões do glossário já validadas, se necessário.

Regra para publicar uma tabela: células com menos de 5 respondentes devem ser agrupadas ou omitidas, para que ninguém possa ser reconhecido.

## Questionário (`questionario/`)

Tabelas agregadas T1 a T11 da análise da Entrega 6 (n = 60, respostas de 28/10 a 15/11/2026), geradas pelo script de análise da equipe a partir da exportação do Google Forms. Células com menos de 5 respondentes aparecem como `<5`. O site lê uma síntese delas em `data/pesquisa.json` (`scripts/montar_painel_pesquisa.py`).

## Glossário (regenerado em 25/11/2026)

| Arquivo | Origem | Dado |
|---|---|---|
| `glossario_verbetes.csv` | `data/glossario.json` | Real (121 verbetes; eram 6 na Entrega 5) |
| `glossario_relacoes.csv` | `data/glossario.json` | Real |
| `glossario_cobertura_questionario.csv` | Glossário × itens do questionário | Real |

As tabelas do questionário (`frequencias.csv`, `cruzamentos.csv` etc.) só aparecem aqui quando o notebook tratar o arquivo **real** `data/raw/respostas_questionario.csv`. O teste com dados sintéticos fica em `outputs/sintetico_teste/` e **nunca** em `data/processed/`.

Todos são gerados por `notebooks/03_obtencao_limpeza_tratamento.ipynb`; não edite à mão.

Cada arquivo deve citar no nome ou em comentário o script que o gerou (pasta `notebooks/`) e a data de geração.
