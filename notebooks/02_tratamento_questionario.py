# -*- coding: utf-8 -*-
"""Tratamento do questionário sobre educação financeira (graduandos e famílias).

Lê o CSV exportado do formulário, remove campos de identificação, calcula o escore
de conhecimento e grava SOMENTE tabelas agregadas, com supressão de células pequenas.

ANTES DE USAR: testado apenas com um CSV sintético, nunca com a exportação real do
formulário. Confira se os nomes das colunas e os códigos das respostas (a, b, c...) do
formulário coincidem com docs/questionario.md e ajuste GABARITO e as listas abaixo se preciso.

Uso (a partir da raiz do repositório):
    python3 notebooks/02_tratamento_questionario.py [ENTRADA.csv] [PASTA_DE_SAIDA]

Padrões:
    ENTRADA        data/raw/respostas_questionario.csv   (não versionado)
    PASTA_DE_SAIDA data/processed/

Nada que identifique pessoas é gravado: as respostas individuais nunca saem de data/raw/.
"""
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA_PADRAO = RAIZ / "data" / "raw" / "respostas_questionario.csv"
SAIDA_PADRAO = RAIZ / "data" / "processed"

MIN_CELULA = 5          # células com menos respondentes são suprimidas ("<5")
SEPARADOR_MULTIPLA = ";"  # separador das respostas de múltipla escolha na exportação

# Respostas corretas (códigos das opções em docs/questionario.md).
# b2_reserva_meses NÃO pontua: nenhuma fonte oficial consultada traz um número único.
GABARITO = {
    "b1_reserva_def": "b",
    "b3_inflacao": "c",
    "b4_juros_compostos": "b",
    "b5_diversificacao": "a",
}
# Cortes do nível de conhecimento (proposta, a confirmar pela equipe).
NIVEIS = [(0, 1, "baixo"), (2, 3, "medio"), (4, 4, "alto")]

MULTIPLA = ["c4_onde_guarda", "c5_dividas", "d7_educ_recebida", "e1_temas_interesse"]
# Resposta aberta: revisada à mão, nunca entra nas tabelas agregadas.
TEXTO_LIVRE = ["e3_termo_dificil"]
# Colunas descartadas se existirem na exportação (identificação ou rastreio).
DESCARTAR = ["carimbo", "timestamp", "data/hora", "hora", "e-mail", "email", "nome",
             "matricula", "matrícula", "cpf", "ip"]
# Cruzamentos: (variável de linha, variável de coluna)
CRUZAMENTOS = [
    ("b1_acertou", "c2_tem_reserva"),
    ("c2_tem_reserva", "d4_fam_reserva"),
    ("d2_fam_conversa", "nivel_conhecimento"),
    ("d1_renda_familiar", "d4_fam_reserva"),
    ("a1_curso", "nivel_conhecimento"),
]
# Médias do escore por grupo
MEDIAS_POR = ["a1_curso", "a2_periodo", "d2_fam_conversa", "c2_tem_reserva"]


def limpar_colunas(df):
    df.columns = [str(c).strip().lower() for c in df.columns]
    descartar = [c for c in df.columns
                 if any(c == d or c.startswith(d + " ") or c.startswith(d + "_") for d in DESCARTAR)]
    return df.drop(columns=descartar), descartar


def como_texto(serie):
    return serie.astype("string").str.strip().str.lower()


def suprimir(n):
    return "<5" if n < MIN_CELULA else int(n)


def frequencias(df, variaveis, multiplas):
    linhas = []
    for v in variaveis:
        if v not in df.columns:
            continue
        s = como_texto(df[v]).dropna()
        s = s[s != ""]
        base = len(s)
        if v in multiplas:
            itens = s.str.split(SEPARADOR_MULTIPLA).explode().str.strip()
            itens = itens[itens != ""]
            contagem = itens.value_counts()
        else:
            contagem = s.value_counts()
        for cat, n in contagem.items():
            linhas.append({
                "variavel": v, "categoria": cat, "n": suprimir(n),
                "pct": "" if n < MIN_CELULA or base == 0 else round(100 * n / base, 1),
                "base": base,
            })
    return pd.DataFrame(linhas)


def cruzar(df, linha, coluna):
    if linha not in df.columns or coluna not in df.columns:
        return pd.DataFrame()
    sub = df[[linha, coluna]].dropna()
    if sub.empty:
        return pd.DataFrame()
    ct = pd.crosstab(sub[linha].astype(str), sub[coluna].astype(str))
    saida = []
    for lin, linha_ct in ct.iterrows():
        total = linha_ct.sum()
        for col, n in linha_ct.items():
            saida.append({
                "linha": linha, "categoria_linha": lin, "coluna": coluna, "categoria_coluna": col,
                "n": suprimir(n),
                "pct_da_linha": "" if n < MIN_CELULA or total < MIN_CELULA else round(100 * n / total, 1),
                "base_linha": int(total),
            })
    return pd.DataFrame(saida)


def medias(df, grupo):
    if grupo not in df.columns:
        return pd.DataFrame()
    sub = df[[grupo, "escore_conhecimento"]].dropna()
    saida = []
    for cat, g in sub.groupby(grupo):
        n = len(g)
        saida.append({
            "grupo": grupo, "categoria": cat, "n": suprimir(n),
            "escore_medio": "" if n < MIN_CELULA else round(g["escore_conhecimento"].mean(), 2),
        })
    return pd.DataFrame(saida)


def nivel(escore):
    for lo, hi, nome in NIVEIS:
        if lo <= escore <= hi:
            return nome
    return None


def main(entrada, saida):
    entrada, saida = Path(entrada), Path(saida)
    if not entrada.exists():
        sys.exit(f"Arquivo não encontrado: {entrada}\nExporte as respostas do formulário (CSV, UTF-8) para esse caminho.")
    df = pd.read_csv(entrada, dtype=str, keep_default_na=False, na_values=[""])
    df, descartadas = limpar_colunas(df)
    if descartadas:
        print("Colunas de identificação/rastreio descartadas:", descartadas)

    if "consentimento" in df.columns:
        antes = len(df)
        df = df[como_texto(df["consentimento"]).str.startswith(("s", "a"), na=False)]
        print(f"Consentimento: {len(df)} de {antes} respostas mantidas")
    df = df.reset_index(drop=True)
    df.insert(0, "id_resposta", range(1, len(df) + 1))
    print(f"{len(df)} respostas")
    if len(df) < MIN_CELULA:
        sys.exit(f"Menos de {MIN_CELULA} respostas: não é seguro gerar tabelas agregadas.")

    faltando = [c for c in GABARITO if c not in df.columns]
    if faltando:
        sys.exit(f"Colunas de conhecimento ausentes (confira docs/questionario.md): {faltando}")

    acertos = pd.DataFrame({c: (como_texto(df[c]) == g).astype(int) for c, g in GABARITO.items()})
    df["escore_conhecimento"] = acertos.sum(axis=1)
    df["nivel_conhecimento"] = df["escore_conhecimento"].map(nivel)
    df["b1_acertou"] = acertos["b1_reserva_def"].map({1: "acertou", 0: "nao_acertou"})

    saida.mkdir(parents=True, exist_ok=True)
    ignorar = {"id_resposta", "escore_conhecimento", *TEXTO_LIVRE}
    variaveis = [c for c in df.columns if c not in ignorar]
    freq = frequencias(df, variaveis, set(MULTIPLA))
    freq.to_csv(saida / "frequencias.csv", index=False)

    dist = df["escore_conhecimento"].value_counts().sort_index()
    pd.DataFrame({"escore": dist.index, "n": [suprimir(n) for n in dist.values],
                  "base": len(df)}).to_csv(saida / "escore_distribuicao.csv", index=False)

    cruz = pd.concat([cruzar(df, a, b) for a, b in CRUZAMENTOS], ignore_index=True)
    cruz.to_csv(saida / "cruzamentos.csv", index=False)
    med = pd.concat([medias(df, g) for g in MEDIAS_POR], ignore_index=True)
    med.to_csv(saida / "escore_medio_por_grupo.csv", index=False)

    print("Gravado em", saida)
    for nome in ["frequencias.csv", "escore_distribuicao.csv", "cruzamentos.csv", "escore_medio_por_grupo.csv"]:
        print(" -", nome)
    print("Lembrete: revisar manualmente a resposta aberta e as tabelas antes de publicar.")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    main(args[0] if len(args) > 0 else ENTRADA_PADRAO, args[1] if len(args) > 1 else SAIDA_PADRAO)
