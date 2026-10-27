# data/raw/

Dados originais permitidos. **Nada desta pasta é versionado**, exceto este arquivo e o `.gitkeep` (ver `.gitignore`).

## O que vai aqui (somente no computador de quem coletou)

| Arquivo (local) | Origem | Observação |
|---|---|---|
| `respostas_questionario.csv` | Exportação da plataforma do questionário | Contém respostas individuais. **Não subir ao Git.** Remover carimbo de data/hora e qualquer campo de identificação antes do tratamento |

## Como obter

1. Na plataforma do questionário, exportar as respostas em CSV (UTF-8).
2. Salvar nesta pasta com o nome `respostas_questionario.csv`.
3. Rodar o tratamento descrito em `docs/plano-de-dados.md`, seção "Plano de aquisição".

Fontes públicas grandes ou não redistribuíveis também não são versionadas: registrar o link e o procedimento de download no inventário (`docs/plano-de-dados.md`).
