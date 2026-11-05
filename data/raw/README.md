# data/raw/

Dados originais permitidos. **Nada desta pasta é versionado**, exceto este arquivo e o `.gitkeep` (ver `.gitignore`).

## O que vai aqui (somente no computador de quem coletou)

| Arquivo (local) | Origem | Observação |
|---|---|---|
| `respostas_questionario.csv` | Exportação da plataforma do questionário | Contém respostas individuais. **Não subir ao Git.** O carimbo de data/hora e qualquer campo de identificação são descartados pelo tratamento |

## Como obter

1. No Google Forms (formulário "Educação financeira entre estudantes de graduação (UFPB / CORECON-PB)"), abrir a aba *Respostas* e baixar as respostas em CSV.
2. Salvar nesta pasta com o nome `respostas_questionario.csv`. Não é preciso editar nada: o CSV traz o texto das opções, e o tratamento traduz para códigos (`notebooks/02a_formulario_google.py`).
3. Rodar `notebooks/03_obtencao_limpeza_tratamento.ipynb` (ver `docs/plano-de-dados.md`, seção "Plano de aquisição").

Fontes públicas grandes ou não redistribuíveis também não são versionadas: registrar o link e o procedimento de download no inventário (`docs/plano-de-dados.md`).
