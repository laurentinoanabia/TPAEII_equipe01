# -*- coding: utf-8 -*-
"""Adaptador do formulário publicado no Google Forms.

Formulário: "Educação financeira entre estudantes de graduação (UFPB / CORECON-PB)"
(8 páginas, 29 perguntas). Link: https://docs.google.com/forms/d/e/1FAIpQLSel8h8rKd4svyMe79V1ME_7TQSW466HPaT5WGMpb-kU3PNWgg/viewform

Por que este módulo existe. O Google Forms NÃO exporta códigos: a planilha de respostas tem
uma coluna por pergunta, com o TÍTULO da pergunta como cabeçalho, e cada célula traz o TEXTO da
opção escolhida ("b) Dinheiro guardado e de fácil acesso..."). Respostas de caixas de seleção
vêm numa célula só, separadas por ", ". Já o tratamento (notebooks/02 e 03) trabalha com nomes
de variável (b1_reserva_def) e códigos curtos (b, 1_3, nao_sei) listados em
outputs/livro_de_codigos.csv. Este módulo faz a tradução, com o mapa abaixo transcrito do
formulário publicado em 05/11/2026.

Regras de segurança desta tradução:
- rótulo que não está no mapa vira o código "__desconhecido__" (o texto original NÃO segue
  adiante) e o tratamento o invalida e conta;
- "Outro" em curso (texto livre) vira "outro": o texto digitado nunca é guardado;
- colunas que não são perguntas conhecidas passam sem alteração para o tratamento, que descarta
  identificação/rastreio e depois qualquer coluna fora do livro de códigos.

Se o formulário mudar (pergunta nova, opção renomeada), atualize QUESTOES e rode de novo o
notebook: o teste "mapa × livro de códigos" e o de ida e volta apontam o que ficou fora.
"""
import re
import unicodedata

import pandas as pd

DESCONHECIDO = "__desconhecido__"
SEPARADOR = ";"          # separador interno das respostas de múltipla escolha (o do Forms é ", ")

# (variável, título da pergunta no formulário, tipo, [(rótulo da opção no formulário, código)])
# tipo: "unica" (uma opção) ou "multipla" (caixas de seleção).
QUESTOES = [
    ("consentimento", "Consentimento", "unica", [
        ("Tenho 18 anos ou mais, li as informações acima e aceito participar.", "aceito"),
        ("Não aceito participar.", "nao_aceito")]),
    ("a1_curso", "Qual é o seu curso de graduação?", "unica", [
        ("Ciências Econômicas", "ciencias_economicas"), ("Administração", "administracao"),
        ("Ciências Contábeis", "ciencias_contabeis")]),               # + "Outro" (texto livre) -> "outro"
    ("a2_periodo", "Em que período você está?", "unica", [
        ("1º ao 4º", "1_4"), ("5º ao 8º", "5_8"), ("9º ou mais", "9_mais")]),
    ("a3_idade", "Qual é a sua faixa de idade?", "unica", [
        ("18 a 20", "18_20"), ("21 a 23", "21_23"), ("24 a 26", "24_26"), ("27 ou mais", "27_mais")]),
    ("a4_ocupacao", "Qual é a sua situação atual?", "unica", [
        ("Só estudo", "so_estuda"), ("Estudo e trabalho ou estágio", "estuda_trabalha"), ("Outra", "outra")]),
    ("a5_renda_propria", "Qual é a sua renda própria mensal (trabalho, estágio, bolsa)?", "unica", [
        ("Nenhuma", "nenhuma"), ("Até 1 salário mínimo", "ate_1"), ("Mais de 1 até 2 salários mínimos", "1_2"),
        ("Mais de 2 salários mínimos", "mais_2"), ("Prefiro não responder", "pnr")]),
    ("b1_reserva_def", "Qual alternativa melhor descreve uma reserva de emergência?", "unica", [
        ("a) Dinheiro guardado para comprar algo que você quer muito, como uma viagem.", "a"),
        ("b) Dinheiro guardado e de fácil acesso para cobrir imprevistos ou perda de renda.", "b"),
        ("c) Dinheiro investido em ações para ganhar o máximo possível.", "c"),
        ("d) Limite do cartão de crédito ou do cheque especial.", "d"),
        ("e) Não sei", "e")]),
    ("b2_reserva_meses", "Na sua opinião, quantos meses de despesas seria adequado guardar como reserva de emergência?", "unica", [
        ("Menos de 1 mês", "menos_1"), ("De 1 a 3 meses", "1_3"), ("De 3 a 6 meses", "3_6"),
        ("Mais de 6 meses", "mais_6"), ("Não sei", "nao_sei")]),
    ("b7_reserva_local", "Qual destes lugares é mais adequado para a reserva de emergência?", "unica", [
        ("a) Um investimento de longo prazo, sem possibilidade de resgate por anos.", "a"),
        ("b) Ações da bolsa, que podem render muito.", "b"),
        ("c) Uma aplicação segura, que possa ser resgatada rapidamente quando necessário.", "c"),
        ("d) Um limite de crédito pré-aprovado no banco.", "d"),
        ("e) Não sei", "e")]),
    ("b3_inflacao", "Você tem R$ 100 guardados e eles rendem 2% em um ano. Nesse mesmo ano, os preços sobem 5%. Depois de um ano, com esse dinheiro você poderá comprar:", "unica", [
        ("a) Mais do que hoje.", "a"), ("b) Exatamente o mesmo.", "b"), ("c) Menos do que hoje.", "c"), ("d) Não sei", "d")]),
    ("b4_juros_compostos", "Você deve R$ 1.000 em uma dívida com juros de 10% ao mês e não paga nada por 2 meses. Quanto você deverá no fim do segundo mês?", "unica", [
        ("a) R$ 1.200", "a"), ("b) R$ 1.210", "b"), ("c) R$ 1.100", "c"), ("d) Não sei", "d")]),
    ("b5_diversificacao", "Colocar todo o seu dinheiro em um único investimento, em vez de dividi-lo em vários, em geral significa:", "unica", [
        ("a) Risco maior.", "a"), ("b) Risco menor.", "b"), ("c) O mesmo risco.", "c"), ("d) Não sei", "d")]),
    ("b6_autoavaliacao", "De 1 (nenhum) a 5 (muito alto), como você avalia o seu conhecimento sobre finanças pessoais?", "unica", [
        ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")]),
    ("c1_orcamento", "Você anota ou planeja seus gastos e receitas do mês?", "unica", [
        ("Nunca", "nunca"), ("Às vezes", "as_vezes"), ("Sempre", "sempre")]),
    ("c2_tem_reserva", "Você tem uma reserva de emergência?", "unica", [
        ("Sim", "sim"), ("Parcialmente", "parcial"), ("Não", "nao")]),
    ("c3_reserva_cobertura", "Sua reserva cobre aproximadamente quantos meses das suas despesas?", "unica", [
        ("Menos de 1 mês", "menos_1"), ("De 1 a 3 meses", "1_3"), ("De 3 a 6 meses", "3_6"), ("Mais de 6 meses", "mais_6")]),
    ("c4_onde_guarda", "Onde você guarda esse dinheiro?", "multipla", [
        ("Poupança", "poupanca"), ("Renda fixa (CDB, Tesouro etc.)", "renda_fixa"), ("Conta corrente", "conta_corrente"),
        ("Dinheiro em casa", "dinheiro_casa"), ("Outro", "outro")]),
    ("c5_dividas", "Você tem alguma dessas dívidas hoje?", "multipla", [
        ("Cartão de crédito", "cartao"), ("Empréstimo ou financiamento", "emprestimo"), ("Parcelas atrasadas", "atrasadas"),
        ("Nenhuma", "nenhuma"), ("Prefiro não responder", "pnr")]),
    ("c6_poupa_regular", "Você guarda uma parte do que recebe todo mês?", "unica", [
        ("Sim", "sim"), ("Às vezes", "as_vezes"), ("Não", "nao")]),
    ("d1_renda_familiar", "Qual é, aproximadamente, a renda mensal total da sua família?", "unica", [
        ("Até 1 salário mínimo", "ate_1"), ("Mais de 1 até 3", "1_3"), ("Mais de 3 até 6", "3_6"), ("Mais de 6", "mais_6"),
        ("Não sei", "nao_sei"), ("Prefiro não responder", "pnr")]),
    ("d2_fam_conversa", "Na sua casa, vocês conversam sobre dinheiro e contas?", "unica", [
        ("Nunca", "nunca"), ("Às vezes", "as_vezes"), ("Frequentemente", "frequente")]),
    ("d3_fam_orcamento", "Sua família controla o orçamento (anota ou planeja os gastos)?", "unica", [
        ("Sim", "sim"), ("Não", "nao"), ("Não sei", "nao_sei")]),
    ("d4_fam_reserva", "Sua família tem dinheiro guardado para emergências?", "unica", [
        ("Sim", "sim"), ("Não", "nao"), ("Não sei", "nao_sei")]),
    ("d5_fam_dividas", "Sua família tem dívidas em atraso?", "unica", [
        ("Sim", "sim"), ("Não", "nao"), ("Não sei", "nao_sei"), ("Prefiro não responder", "pnr")]),
    ("d6_fam_conhecimento", "De 1 (nenhum) a 5 (muito alto), como você avalia o conhecimento da sua família sobre finanças?", "unica", [
        ("1 – Nenhum", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5 – Muito alto", "5"), ("Não sei", "nao_sei")]),
    ("d7_educ_recebida", "Onde você já teve contato com educação financeira?", "multipla", [
        ("Escola", "escola"), ("Família", "familia"), ("Curso ou faculdade", "curso"),
        ("Internet e redes sociais", "internet"), ("Nunca tive", "nunca")]),
    ("e1_temas_interesse", "Que temas você gostaria de ver explicados no glossário?", "multipla", [
        ("Orçamento", "orcamento"), ("Reserva de emergência", "reserva"), ("Crédito e juros", "credito_juros"),
        ("Dívidas e renegociação", "dividas"), ("Investimentos", "investimentos"), ("Inflação e Selic", "inflacao_selic"),
        ("Impostos", "impostos"), ("Outro", "outro")]),
    ("e3_termo_prioritario", "Qual destes termos você mais gostaria de ver explicado?", "unica", [
        ("Juros compostos", "juros_compostos"), ("Inflação", "inflacao"), ("Taxa Selic", "taxa_selic"),
        ("Renda fixa", "renda_fixa"), ("Diversificação", "diversificacao"), ("Endividamento", "endividamento"),
        ("Orçamento pessoal", "orcamento_pessoal"), ("Nenhum deles", "nenhum")]),
    ("e2_usaria_glossario", "Você usaria um glossário online de termos da economia?", "unica", [
        ("Sim", "sim"), ("Talvez", "talvez"), ("Não", "nao")]),
]

# Perguntas em que "Outro" é um campo de texto livre: qualquer texto fora das opções vira este código.
OUTRO_LIVRE = {"a1_curso": "outro"}

# Cabeçalhos completos, quando o título tem uma segunda linha (assim o teste usa cabeçalhos realistas).
TITULO_COMPLETO = {
    "a1_curso": "Qual é o seu curso de graduação?\nSe diferente das opções, por favor informar",
    "e2_usaria_glossario": "Você usaria um glossário online de termos da economia?\nConsidere um site interativo que deve ampliar o conhecimento comum sobre termos econômicos, educação financeira e macroeconomia.",
}
COLUNA_CARIMBO = "Carimbo de data/hora"
MULTIPLAS = [v for v, _, t, _ in QUESTOES if t == "multipla"]


def norm(s):
    """Para comparar textos: sem acento, minúsculas, travessões iguais, espaços colapsados."""
    t = unicodedata.normalize("NFD", str(s))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn").lower()
    t = t.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", t).strip()


_TITULOS = {v: norm(t) for v, t, _, _ in QUESTOES}
_MAPA = {v: {norm(r): c for r, c in ops} for v, _, _, ops in QUESTOES}
_TIPO = {v: t for v, _, t, _ in QUESTOES}


def variavel_do_cabecalho(cabecalho):
    """Variável cujo título é o início do cabeçalho (vence o título mais longo). None se não for pergunta conhecida."""
    h = norm(cabecalho)
    achadas = [(len(t), v) for v, t in _TITULOS.items() if h == t or h.startswith(t + " ")]
    return max(achadas)[1] if achadas else None


def e_exportacao_do_forms(df, minimo=5):
    """True se o CSV tem cabeçalhos de pergunta do formulário (e não nomes de variável)."""
    return sum(variavel_do_cabecalho(c) is not None for c in df.columns) >= minimo


def _vazio(x):
    return x is None or (isinstance(x, float) and pd.isna(x)) or x is pd.NA or str(x).strip() == ""


def _quebrar_multipla(texto, mapa):
    """Separa 'A, B, Renda fixa (CDB, Tesouro etc.)' sem quebrar o rótulo que tem vírgula (tenta juntar partes)."""
    partes = str(texto).split(", ")
    saida, i = [], 0
    while i < len(partes):
        for j in range(min(len(partes), i + 4), i, -1):          # junta do mais longo para o mais curto
            cand = ", ".join(partes[i:j])
            if norm(cand) in mapa:
                saida.append(mapa[norm(cand)])
                i = j
                break
        else:
            saida.append(DESCONHECIDO)
            i += 1
    return SEPARADOR.join(dict.fromkeys(saida))


def adaptar(bruto):
    """Exportação do Google Forms -> tabela com nomes de variável e códigos do livro de códigos.

    Devolve (tabela, info). Colunas que não são perguntas conhecidas seguem sem alteração (o tratamento
    descarta identificação/rastreio e depois tudo o que estiver fora do livro de códigos).
    """
    cab = {c: variavel_do_cabecalho(c) for c in bruto.columns}
    saida = pd.DataFrame(index=bruto.index)
    outros_texto = 0
    for col in bruto.columns:
        var = cab[col]
        if var is None:
            saida[col] = bruto[col]                       # passa; o tratamento decide
            continue
        mapa, tipo = _MAPA[var], _TIPO[var]

        def traduz(x, var=var, mapa=mapa, tipo=tipo):
            nonlocal outros_texto
            if _vazio(x):
                return pd.NA
            if tipo == "multipla":
                return _quebrar_multipla(x, mapa)
            k = norm(x)
            if k in mapa:
                return mapa[k]
            if var in OUTRO_LIVRE:                        # texto livre: não guardar o que foi digitado
                outros_texto += 1
                return OUTRO_LIVRE[var]
            return DESCONHECIDO
        saida[var] = bruto[col].map(traduz)
    reconhecidas = [v for v in cab.values() if v]
    info = {
        "perguntas_reconhecidas": len(set(reconhecidas)),
        "perguntas_do_formulario_ausentes_no_csv": [v for v, _, _, _ in QUESTOES if v not in reconhecidas],
        "colunas_nao_reconhecidas": [c for c, v in cab.items() if v is None],
        "cursos_outros_texto_livre": outros_texto,
    }
    return saida, info


def simular_exportacao(cod):
    """Faz o caminho inverso (códigos -> texto da opção, ', ' nas caixas de seleção, cabeçalho = título).

    Serve ao teste de ida e volta: mostra que adaptar(simular_exportacao(x)) devolve x. Não é uma
    amostra de respostas reais.
    """
    rotulo = {v: {c: r for r, c in ops} for v, _, _, ops in QUESTOES}
    titulos = {v: TITULO_COMPLETO.get(v, t) for v, t, _, _ in QUESTOES}
    exp = pd.DataFrame(index=cod.index)
    for v, _, tipo, _ in QUESTOES:
        if v not in cod.columns:
            continue

        def inverso(x, v=v, tipo=tipo):
            if _vazio(x):
                return ""
            if tipo == "multipla":
                return ", ".join(rotulo[v][c] for c in str(x).split(SEPARADOR))
            return rotulo[v].get(x, "Engenharia Civil" if v in OUTRO_LIVRE else DESCONHECIDO)   # "outro" = texto livre
        exp[titulos[v]] = cod[v].map(inverso)
    return exp
