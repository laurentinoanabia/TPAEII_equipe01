# Histórico das entregas

**TPAE II – PSAE00320 · Equipe 01** · Ana Beatriz Laurentino, Arthur Almeida e Gabriel Pinheiro · Orientador: Alessio

| Entrega | Prazo sugerido | Tema | Situação |
|---|---|---|---|
| 1 | 09/09/2026 | Prospecção de potenciais demandantes | Entregue |
| 2 | 21/09/2026 | Escuta e compreensão da demanda | Demandante definido: CORECON-PB. Memória e roteiro: **[a registrar]** |
| 3 | 01/10/2026 | Definição do problema e plano de pesquisa | Entregue, com o projeto de educação financeira em escolas |
| 4 | 20/10/2026 | Repositório e plano de dados | Repositório, plano de dados e PDF prontos em 27/10/2026. Falta o acesso do professor ao repositório e o envio do PDF |
| 5 | 29/10/2026 | Obtenção, limpeza e tratamento dos dados | Notebook, base processada do glossário e relatório de qualidade prontos em 27/10/2026; atualizados em 05/11/2026 para o formulário publicado. Nenhuma exportação de respostas foi tratada ainda: as regras foram testadas com dados sintéticos e com uma exportação simulada no formato do Forms |
| Final | 15/12/2026 | Apresentação com banca no CORECON-PB | Pendente |

## Entrega 1: prospecção (09/09/2026)

Três indicações de demandante em reciclagem, em João Pessoa:

1. **Emlur**, autarquia municipal de limpeza urbana, responsável pelo programa Recicla JP. Problema: medir a eficiência econômica do programa. Viabilidade média.
2. **Ascare-JP**, associação de catadores. Problema: renda pouco previsível. Viabilidade média.
3. **Semear Sustentabilidade**, empresa privada. Problema: medir o impacto econômico e ambiental. Viabilidade alta.

Priorização: Emlur como indicação mais promissora, com a Ascare-JP como fonte complementar.

## Entrega 2: escuta (21/09/2026)

Demandante definido pela equipe: **CORECON-PB**. Roteiro de perguntas e memória da reunião: **[a registrar neste repositório, se a equipe autorizar]**. Os materiais internos do CORECON-PB não devem ser versionados.

## Entrega 3: problema e plano de pesquisa (01/10/2026)

- Demandante: CORECON-PB. Beneficiários: estudantes de ensino médio de João Pessoa, voluntários da UFPB e o próprio Conselho.
- Problema: desenhar uma iniciativa voluntária de educação financeira em escolas de João Pessoa, sem diagnóstico de escolas, conteúdos e capacidade de voluntários.
- Pergunta principal: que perfil de escolas, conteúdos e capacidade de voluntários deve orientar a iniciativa.
- Fontes previstas: Censo Escolar (Inep), Censo 2022 (IBGE), secretarias de educação, ENEF, BNCC e PISA.
- Em 20/10/2026 o foco passou a um piloto com a escola Interactivo e uma escola pública a selecionar.

## Mudança de rumo (22/10/2026)

A equipe trocou o projeto das escolas por um **site de conhecimento para o CORECON-PB**, a partir da lista de demandas do Conselho, em apoio ao programa "PB sem dívidas". O site virou um **glossário de termos da economia**, para a população em geral, com acessibilidade. O repositório anterior (`TPAE-II`, depois `TPAE-II-`) foi substituído por este. O material do projeto das escolas está preservado em [`arquivo/escolas/`](arquivo/escolas/README.md).

## Incorporação da pesquisa com graduandos (27/10/2026)

A equipe decidiu somar ao glossário uma **pesquisa com estudantes de graduação** sobre educação financeira: quantos entendem e aplicam reserva de emergência, qual a situação financeira da família e qual o nível de conhecimento das famílias. A pesquisa orienta quais termos o glossário prioriza. Instrumento em [`questionario.md`](questionario.md).

## Ajustes no site publicado (25/11/2026)

- Site publicado no GitHub Pages (https://laurentinoanabia.github.io/TPAEII_equipe01/).
- Novo verbete "Dívida barata e dívida cara", com dados do Banco Central e os limites legais do cheque especial e do rotativo, ligado aos verbetes de dívida e à trilha "Dívidas sob controle".
- O painel da pesquisa passou a mostrar só percentuais, sem o total de respostas nem contagens, por decisão da equipe. O relatório técnico continua informando o n; as tabelas agregadas com contagens seguem em `data/processed/questionario/`.
- Escala tipográfica do site reduzida (texto-base de 18 px para 16 px, títulos menores) e controle de tamanho da letra com quatro opções (normal, grande, muito grande, pequena).

## Painel "Resultados da pesquisa" no site (25/11/2026)

- A demanda do CORECON-PB foi registrada nas palavras da equipe: um glossário econômico de fácil entendimento para quem navega pelo site.
- Nova página `#/pesquisa` com as descobertas do questionário (n = 60, respostas de 28/10 a 15/11/2026): indicadores-resumo, cinco achados com gráficos de barras, quadro das hipóteses H1 a H4 e as limitações. Os resultados são apresentados como associações, e grupos com menos de 5 pessoas aparecem como "<5". A nota principal é a de 0 a 4 do plano de análise.
- As tabelas agregadas estão em `data/processed/questionario/`, e `scripts/montar_painel_pesquisa.py` gera `data/pesquisa.json`.

## Reposicionamento do site e reforço do conteúdo (25/11/2026)

- **Versão atual do site no repositório.** O site foi desenvolvido fora do repositório, com apoio de IA, a partir de dois prompts da equipe: um de escopo (enciclopédia em 7 níveis, simuladores, trilhas, quiz, fontes oficiais) e outro que o apresentava como projeto independente, sem vínculo com o CORECON-PB. Essa versão ("Opção B") foi trazida para `index.html` e `data/`.
- **Posicionamento definido pela equipe.** O site é apresentado como produto da pesquisa: surgiu de uma demanda do CORECON-PB, é de autoria da equipe e não tem chancela do Conselho. Os textos de "Sobre", rodapé e metadados foram ajustados, e a página Sobre ganhou a seção "A pesquisa".
- **Conteúdo reequilibrado.** Os prompts não pediam orçamento, dívidas nem reserva, e o site tinha 27 verbetes de investimentos contra 6 de dívidas e planejamento. Foram criados 11 verbetes (Superendividamento, Renegociação de dívidas, Cheque especial, Juros de mora e multa, Registrato, Cadastro Positivo, Empréstimo consignado, Comprometimento de renda, Despesas fixas e variáveis, Caderneta de poupança, Educação financeira), com fontes legais e oficiais, e reforçados Orçamento pessoal, Endividamento, Inadimplência, Reserva de emergência e Crédito rotativo. Todos os verbetes passaram a ter `fonte`. Nova trilha "Dívidas sob controle" e indicador de famílias endividadas (Peic/CNC, out/2026).
- **Correções.** Quiz com 10 perguntas novas e posição da resposta certa equilibrada (antes, 53 de 67 respostas estavam na 2ª opção); "juros de mora" deixou de ser sinônimo de "juros remuneratórios"; mensagem da calculadora de dívida para quitações acima de 30 anos.
- **Entrega 5 reexecutada.** O notebook 03 foi reexecutado com o glossário novo; as tabelas do glossário em `data/processed/` e os arquivos de `outputs/` foram regenerados. O PDF da Entrega 5 continua sendo o retrato de 05/11/2026 (6 verbetes).

## Entrega 5: obtenção, limpeza e tratamento (prazo sugerido 29/10/2026)

Entregáveis do guia e onde estão:

| Exigência | Onde |
|---|---|
| Notebook que executa do início ao fim | `notebooks/03_obtencao_limpeza_tratamento.ipynb` (estrutura obrigatória de 7 seções), com o tradutor do formulário em `notebooks/02a_formulario_google.py` |
| Base processada | `data/processed/glossario_*.csv` (dado real). Questionário: só depois da coleta |
| Relatório de qualidade | `outputs/relatorio_qualidade.csv` e `docs/E05_equipe01_qualidade_dados.pdf` |
| Dicionário atualizado | `docs/plano-de-dados.md`, seções 4.2 e 4.3, `outputs/livro_de_codigos.csv` e `outputs/mapa_formulario.csv` |
| Testes e contagens antes/depois | `outputs/testes_integridade.csv` e `outputs/funil_contagens.csv` |

**Atualização de 05/11/2026 (formulário publicado).** O formulário do Google Forms foi publicado e lido. Ele difere do rascunho em três pontos (pergunta nova b7; termo e3 virou múltipla escolha; curso virou lista fechada) e, sobretudo, o Google Forms exporta o **texto** das opções, não códigos. O notebook passou a traduzir a exportação (`02a_formulario_google.py`), o mapa foi conferido contra o formulário publicado e foi testado com uma exportação simulada no formato do Forms, em uma cópia descartável, que ativa o caminho de dados reais.

**Limite a declarar ao professor:** nenhuma exportação real de respostas foi tratada. A única base real era o glossário (6 verbetes de rascunho em 05/11/2026; 121 desde 25/11/2026). Para o questionário, o notebook foi testado com dados sintéticos com defeitos plantados e com a exportação simulada. O PDF `docs/E04_equipe01_plano_dados.pdf` é o retrato de 27/10/2026 e não reflete o formulário publicado.

## Entrega 4: repositório e plano de dados

Exigências do guia e onde estão atendidas:

| Exigência | Onde |
|---|---|
| Estrutura mínima de pastas e `.gitignore` | Raiz do repositório |
| README com problema, equipe, fontes, estrutura e instruções | `README.md` |
| Inventário de fontes (instituição, link, cobertura, formato, licença, data de acesso) | `docs/plano-de-dados.md`, seção 2 |
| Unidade, chaves, periodicidade e junções | `docs/plano-de-dados.md`, seção 3 |
| Dicionário das variáveis essenciais | `docs/plano-de-dados.md`, seção 4 |
| Procedimento de aquisição | `docs/plano-de-dados.md`, seção 5 |
| Segurança dos dados | `docs/plano-de-dados.md`, seção 6, e `.gitignore` |
| Tarefas com responsável, prazo e situação | `docs/tarefas.md` (responsáveis herdados do plano anterior, a confirmar) |
| Acesso do professor ao repositório | **Pendente:** adicionar o professor como colaborador (tarefa 2) |
| PDF `E04_equipe01_plano_dados.pdf` | Gerado em 27/10/2026 a partir de `plano-de-dados.md`, em `docs/E04_equipe01_plano_dados.pdf` (regenerar se o plano mudar). **Pendente:** enviar ao professor (tarefa 5) |
