# data/processed/

Dados tratados e **agregados**, sem informação pessoal. Aqui podem ser versionados:

- tabelas de frequência por pergunta (contagens e percentuais);
- cruzamentos agregados (por exemplo, nível de conhecimento por grupo);
- versões do glossário já validadas, se necessário.

Regra para publicar uma tabela: células com menos de 5 respondentes devem ser agrupadas ou omitidas, para que ninguém possa ser reconhecido.

## Conteúdo atual (Entrega 5)

| Arquivo | Origem | Dado |
|---|---|---|
| `glossario_verbetes.csv` | `data/glossario.json` | Real (6 verbetes de rascunho) |
| `glossario_relacoes.csv` | `data/glossario.json` | Real |
| `glossario_cobertura_questionario.csv` | Glossário × itens do questionário | Real |

As tabelas do questionário (`frequencias.csv`, `cruzamentos.csv` etc.) só aparecem aqui quando o notebook tratar o arquivo **real** `data/raw/respostas_questionario.csv`. O teste com dados sintéticos fica em `outputs/sintetico_teste/` e **nunca** em `data/processed/`.

Todos são gerados por `notebooks/03_obtencao_limpeza_tratamento.ipynb`; não edite à mão.

Cada arquivo deve citar no nome ou em comentário o script que o gerou (pasta `notebooks/`) e a data de geração.
