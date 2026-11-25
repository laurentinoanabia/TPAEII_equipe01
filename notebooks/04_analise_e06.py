# -*- coding: utf-8 -*-
"""Entrega 6 – análise descritiva preliminar do questionário (equipe 01, TPAE II).

Uso (a partir da raiz do repositório):
    python3 notebooks/04_analise_e06.py [ENTRADA.csv] [PASTA_SAIDA]

Padrões: ENTRADA = data/raw/respostas_questionario.csv (exportação do Google Forms, fora do Git);
PASTA_SAIDA = outputs/e06/ (tabelas/*.csv e figuras/*.png).

- Usa o mesmo mapa pergunta/opção → código do tratamento (notebooks/02a_formulario_google.py), que já
  reconhece o separador ";" da exportação real e as redações da versão 2 do formulário.
- Cada resposta recebe a versão do formulário (v1/v2) pela redação exportada; quando a redação não
  permite distinguir, usa o carimbo de data/hora (corte: 03/11/2026). O carimbo não é gravado.
- Escore principal (decisão da equipe, 25/11/2026) = acertos em b1, b3, b4 e b5 (0 a 4). Também são
  calculados o Big Three (b3, b4, b5; 0 a 3) e, só como sensibilidade, a nota de 0 a 6 (inclui b2 = "3 a 6
  meses" e b7 = c).
- Só grava tabelas agregadas; contagens menores que 5 aparecem como "<5".
- Testes (Fisher, Mann-Whitney, Kruskal-Wallis, Spearman) são exploratórios e não indicam causa.
"""
import importlib.util
import sys
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parent.parent
ENT = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "data" / "raw" / "respostas_questionario.csv"
SAIDA = Path(sys.argv[2]) if len(sys.argv) > 2 else RAIZ / "outputs" / "e06"
(SAIDA / "tabelas").mkdir(parents=True, exist_ok=True)
(SAIDA / "figuras").mkdir(parents=True, exist_ok=True)
MIN = 5

spec = importlib.util.spec_from_file_location("forms", RAIZ / "notebooks" / "02a_formulario_google.py")
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)

bruto = pd.read_csv(ENT, dtype=str, keep_default_na=False, encoding="utf-8-sig")
n_bruto = len(bruto)

# carimbo (só para versão e período; descartado logo depois)
COL_TS = next(c for c in bruto.columns if c.strip().lower() in ("timestamp", "carimbo de data/hora"))
ts = bruto[COL_TS].str.replace(" GMT-3", "", regex=False).map(
    lambda s: datetime.strptime(s, "%Y/%m/%d %I:%M:%S %p"))
CORTE = datetime(2026, 11, 3)           # última resp. com texto antigo: 02/11 14:38; 1ª com novo: 05/11 19:18
versao = F.versao_do_formulario(bruto).fillna(pd.Series(np.where(ts < CORTE, "v1", "v2"), index=bruto.index))
assert ((versao == "v1") == (ts < CORTE)).all(), "versão pela redação diverge da data de corte"
periodo = (ts.min(), ts.max())
por_dia = ts.dt.date.value_counts().sort_index()
antes_periodo = int((ts < datetime(2026, 11, 1)).sum())

dup = int(bruto.duplicated().sum())
bruto = bruto.drop_duplicates()
df, info = F.adaptar(bruto.drop(columns=[COL_TS]))
df["versao_form"] = versao.loc[df.index].values
sem_consent = int((df["consentimento"] != "aceito").sum())
df = df[df["consentimento"] == "aceito"].copy()

# invalidações remanescentes (deve ser zero)
inval = {}
for v in df.columns:
    if v in ("versao_form",):
        continue
    s = df[v].astype("string")
    k = s.str.contains(F.DESCONHECIDO, regex=False, na=False).sum()
    if k:
        inval[v] = int(k)

# --- variáveis derivadas -----------------------------------------------------------------
GAB = {"b1_reserva_def": "b", "b3_inflacao": "c", "b4_juros_compostos": "b", "b5_diversificacao": "a"}
for v, g in GAB.items():
    df[v + "_ok"] = (df[v] == g).astype(int)
df["b7_ok"] = (df["b7_reserva_local"] == "c").astype(int)
df["b2_ok"] = (df["b2_reserva_meses"] == "3_6").astype(int)
df["escore"] = df[[v + "_ok" for v in GAB]].sum(axis=1)
df["big3"] = df[["b3_inflacao_ok", "b4_juros_compostos_ok", "b5_diversificacao_ok"]].sum(axis=1)
df["nota6"] = df["escore"] + df["b7_ok"] + df["b2_ok"]
df["nivel"] = pd.cut(df["escore"], [-1, 1, 3, 4], labels=["baixo (0–1)", "médio (2–3)", "alto (4)"])
df["curso2"] = np.where(df["a1_curso"] == "ciencias_economicas", "Ciências Econômicas", "Demais cursos")
df["tem_alguma_reserva"] = df["c2_tem_reserva"].isin(["sim", "parcial"]).astype(int)
df["b6"] = pd.to_numeric(df["b6_autoavaliacao"])
df["d6"] = pd.to_numeric(df["d6_fam_conhecimento"], errors="coerce")
def tem(v, cod):
    return df[v].fillna("").str.split(F.SEPARADOR).map(lambda l: cod in l).astype(int)
df["tem_divida"] = (tem("c5_dividas", "cartao") | tem("c5_dividas", "emprestimo") | tem("c5_dividas", "atrasadas")).astype(int)
N = len(df)

ROT = {
    "a2_periodo": {"1_4": "1º ao 4º", "5_8": "5º ao 8º", "9_mais": "9º ou mais"},
    "a3_idade": {"18_20": "18 a 20", "21_23": "21 a 23", "24_26": "24 a 26", "27_mais": "27 ou mais"},
    "a4_ocupacao": {"so_estuda": "Só estuda", "estuda_trabalha": "Estuda e trabalha/estagia", "outra": "Outra"},
    "a5_renda_propria": {"nenhuma": "Nenhuma", "ate_1": "Até 1 SM", "1_2": "Mais de 1 até 2 SM", "mais_2": "Mais de 2 SM", "pnr": "Prefere não responder"},
    "d1_renda_familiar": {"ate_1": "Até 1 SM", "1_3": "Mais de 1 até 3 SM", "3_6": "Mais de 3 até 6 SM", "mais_6": "Mais de 6 SM", "nao_sei": "Não sabe", "pnr": "Prefere não responder"},
    "b2_reserva_meses": {"menos_1": "Menos de 1 mês", "1_3": "De 1 a 3 meses", "3_6": "De 3 a 6 meses", "mais_6": "Mais de 6 meses", "nao_sei": "Não sabe"},
    "c3_reserva_cobertura": {"menos_1": "Menos de 1 mês", "1_3": "De 1 a 3 meses", "3_6": "De 3 a 6 meses", "mais_6": "Mais de 6 meses"},
    "c1_orcamento": {"nunca": "Nunca", "as_vezes": "Às vezes", "sempre": "Sempre"},
    "c2_tem_reserva": {"sim": "Sim", "parcial": "Parcialmente", "nao": "Não"},
    "c6_poupa_regular": {"sim": "Sim", "as_vezes": "Às vezes", "nao": "Não"},
    "d2_fam_conversa": {"nunca": "Nunca", "as_vezes": "Às vezes", "frequente": "Frequentemente"},
    "d3_fam_orcamento": {"sim": "Sim", "nao": "Não", "nao_sei": "Não sabe"},
    "d4_fam_reserva": {"sim": "Sim", "nao": "Não", "nao_sei": "Não sabe"},
    "d5_fam_dividas": {"sim": "Sim", "nao": "Não", "nao_sei": "Não sabe", "pnr": "Prefere não responder"},
    "d6_fam_conhecimento": {"1": "1 – Nenhum", "2": "2", "3": "3", "4": "4", "5": "5 – Muito alto", "nao_sei": "Não sabe"},
    "b6_autoavaliacao": {"1": "1 – Nenhum", "2": "2", "3": "3", "4": "4", "5": "5 – Muito alto"},
    "e2_usaria_glossario": {"sim": "Sim", "talvez": "Talvez", "nao": "Não"},
    "e3_termo_prioritario": {"juros_compostos": "Juros compostos", "inflacao": "Inflação", "taxa_selic": "Taxa Selic", "renda_fixa": "Renda fixa", "diversificacao": "Diversificação", "endividamento": "Endividamento", "orcamento_pessoal": "Orçamento pessoal", "nenhum": "Nenhum deles"},
    "b7_reserva_local": {"a": "a) Longo prazo, sem resgate", "b": "b) Ações da bolsa", "c": "c) Aplicação segura e de resgate rápido ✔", "d": "d) Limite de crédito", "e": "e) Não sabe"},
    "c4_onde_guarda": {"poupanca": "Poupança", "renda_fixa": "Renda fixa (CDB, Tesouro)", "conta_corrente": "Conta corrente", "dinheiro_casa": "Dinheiro em casa", "outro": "Outro"},
    "c5_dividas": {"cartao": "Cartão de crédito", "emprestimo": "Empréstimo ou financiamento", "atrasadas": "Parcelas atrasadas", "nenhuma": "Nenhuma", "pnr": "Prefere não responder"},
    "d7_educ_recebida": {"escola": "Escola", "familia": "Família", "curso": "Curso ou faculdade", "internet": "Internet e redes sociais", "nunca": "Nunca teve"},
    "e1_temas_interesse": {"orcamento": "Orçamento", "reserva": "Reserva de emergência", "credito_juros": "Crédito e juros", "dividas": "Dívidas e renegociação", "investimentos": "Investimentos", "inflacao_selic": "Inflação e Selic", "impostos": "Impostos", "outro": "Outro"},
}


def sup(n):
    return "<5" if n < MIN else int(n)


def pct(n, b):
    return "" if n < MIN or b == 0 else round(100 * n / b, 1)


def freq(v, multipla=False, sub=None):
    d = df if sub is None else df[sub]
    s = d[v].dropna()
    s = s[s != ""]
    base = len(s)
    if multipla:
        cont = s.str.split(F.SEPARADOR).explode().value_counts()
    else:
        cont = s.value_counts()
    ordem = list(ROT.get(v, {}).keys()) or list(cont.index)
    linhas = []
    for c in ordem + [c for c in cont.index if c not in ordem]:
        n = int(cont.get(c, 0))
        if n == 0 and c not in cont.index:
            n = 0
        linhas.append({"variavel": v, "categoria": ROT.get(v, {}).get(c, c), "n": sup(n) if n else 0,
                       "pct": pct(n, base) if n else 0.0, "base": base})
    return pd.DataFrame(linhas)


def salvar(t, nome):
    t.to_csv(SAIDA / "tabelas" / f"{nome}.csv", index=False, encoding="utf-8-sig")
    return t


def fisher_2x2(a, b):
    """a, b: séries 0/1 alinhadas -> (tabela, p)."""
    ct = pd.crosstab(a, b).reindex(index=[0, 1], columns=[0, 1], fill_value=0)
    return ct, stats.fisher_exact(ct.values)[1]


TAB = {}

# ---------------------------------------------------------------- Dados
TAB["T1_funil"] = salvar(pd.DataFrame([
    ("Respostas exportadas do Google Forms", n_bruto),
    ("Envios duplicados removidos", dup),
    ("Sem consentimento (excluídas)", sem_consent),
    ("Base analítica", N),
    ("  respondidas na versão 1 do formulário (28/10 a 02/11)", int((df.versao_form == "v1").sum())),
    ("  respondidas na versão 2 do formulário (05/11 a 15/11)", int((df.versao_form == "v2").sum())),
    ("  enviadas antes do início oficial da coleta (01/11)", antes_periodo),
    ("Sem c3/c4 por desenho (não têm reserva: c2 = Não)", int((df.c2_tem_reserva == "nao").sum())),
], columns=["etapa", "n"]), "T1_funil")

perfil = []
for v, rot in [("curso2", "Curso"), ("a2_periodo", "Período"), ("a3_idade", "Idade"), ("a4_ocupacao", "Ocupação"),
               ("a5_renda_propria", "Renda própria"), ("d1_renda_familiar", "Renda familiar")]:
    if v == "curso2":
        f = df[v].value_counts().reindex(["Ciências Econômicas", "Demais cursos"])
        for c, n in f.items():
            perfil.append((rot, c, sup(n), pct(n, N)))
    else:
        for _, r in freq(v).iterrows():
            perfil.append((rot, r.categoria, r.n, r.pct))
TAB["T2_perfil"] = salvar(pd.DataFrame(perfil, columns=["dimensao", "categoria", "n", "pct"]), "T2_perfil")

# ---------------------------------------------------------------- Conhecimento
itens = [("b1_reserva_def_ok", "Definição de reserva de emergência (b1)"),
         ("b3_inflacao_ok", "Inflação e poder de compra (b3)"),
         ("b4_juros_compostos_ok", "Juros compostos (b4)"),
         ("b5_diversificacao_ok", "Diversificação e risco (b5)"),
         ("b7_ok", "Local adequado da reserva (b7, não pontua)")]
linhas = []
for v, rot in itens:
    eco = df[df.curso2 == "Ciências Econômicas"][v]
    dem = df[df.curso2 == "Demais cursos"][v]
    p = stats.fisher_exact(pd.crosstab(df.curso2, df[v]).reindex(columns=[0, 1], fill_value=0).values)[1]
    linhas.append((rot, int(df[v].sum()), round(100 * df[v].mean(), 1),
                   round(100 * eco.mean(), 1), round(100 * dem.mean(), 1), round(p, 3)))
TAB["T3_acertos"] = salvar(pd.DataFrame(linhas, columns=["item", "acertos_n", "acertos_pct_total",
                                                          "pct_economia_n32", "pct_demais_n28", "p_fisher"]), "T3_acertos")
# erros típicos
erros = {
    "b4 = R$ 1.200 (juros simples)": int((df.b4_juros_compostos == "a").sum()),
    "b4 = Não sei": int((df.b4_juros_compostos == "d").sum()),
    "b3 = errado ou Não sei": int((df.b3_inflacao != "c").sum()),
}
b7v = {ver: (df[df.versao_form == ver].b7_ok.sum(), (df.versao_form == ver).sum()) for ver in ["v1", "v2"]}

dist = df["escore"].value_counts().reindex(range(5), fill_value=0)
TAB["T4_escore"] = salvar(pd.DataFrame({"escore": dist.index, "n": [sup(x) if x else 0 for x in dist.values],
                                        "pct": [pct(x, N) if x else 0.0 for x in dist.values]}), "T4_escore")
TAB["T4b_b2_opiniao"] = salvar(freq("b2_reserva_meses"), "T4b_b2_opiniao")
TAB["T4c_b7"] = salvar(freq("b7_reserva_local"), "T4c_b7")

esc_grupo = []
for g in ["Ciências Econômicas", "Demais cursos"]:
    s = df[df.curso2 == g]
    esc_grupo.append((g, len(s), round(s.escore.mean(), 2), round(s.big3.mean(), 2), round(s.nota6.mean(), 2),
                      round(s.b6.mean(), 2)))
mw = {k: stats.mannwhitneyu(df[df.curso2 == "Ciências Econômicas"][k], df[df.curso2 == "Demais cursos"][k]).pvalue
      for k in ["escore", "big3", "nota6", "b6"]}
esc_grupo.append(("p (Mann-Whitney)", "", round(mw["escore"], 3), round(mw["big3"], 3), round(mw["nota6"], 3), round(mw["b6"], 3)))
esc_grupo.append(("Total", N, round(df.escore.mean(), 2), round(df.big3.mean(), 2), round(df.nota6.mean(), 2), round(df.b6.mean(), 2)))
TAB["T5_escore_curso"] = salvar(pd.DataFrame(esc_grupo, columns=["grupo", "n", "escore_0a4", "big3_0a3", "nota_0a6_sensib", "autoavaliacao_1a5"]), "T5_escore_curso")
rho_b6, p_b6 = stats.spearmanr(df.b6, df.escore)

# ---------------------------------------------------------------- Prática
pr = []
for v, rot in [("c1_orcamento", "Planeja gastos (c1)"), ("c2_tem_reserva", "Tem reserva (c2)"),
               ("c6_poupa_regular", "Poupa todo mês (c6)")]:
    for _, r in freq(v).iterrows():
        pr.append((rot, r.categoria, r.n, r.pct, r.base))
for _, r in freq("c3_reserva_cobertura").iterrows():
    pr.append(("Meses cobertos pela reserva (c3) – só quem tem reserva", r.categoria, r.n, r.pct, r.base))
for _, r in freq("c4_onde_guarda", multipla=True).iterrows():
    pr.append(("Onde guarda (c4, múltipla) – só quem tem reserva", r.categoria, r.n, r.pct, r.base))
for _, r in freq("c5_dividas", multipla=True).iterrows():
    pr.append(("Dívidas atuais (c5, múltipla)", r.categoria, r.n, r.pct, r.base))
TAB["T6_pratica"] = salvar(pd.DataFrame(pr, columns=["indicador", "categoria", "n", "pct", "base"]), "T6_pratica")
reserva_3m = int(df.c3_reserva_cobertura.isin(["3_6", "mais_6"]).sum())
tem_div = int(df.tem_divida.sum())
div_eco = df.groupby("curso2").tem_divida.agg(["sum", "count"])
p_div = stats.fisher_exact(pd.crosstab(df.curso2, df.tem_divida).values)[1]

# ---------------------------------------------------------------- Conhecimento × prática
cp = []
for cond, rot in [(df.b1_reserva_def_ok == 1, "Acerta a definição (b1)"), (df.b1_reserva_def_ok == 0, "Não acerta b1"),
                  (df.escore == 4, "Escore 4 (alto)"), (df.escore < 4, "Escore 0 a 3")]:
    s = df[cond]
    for c in ["sim", "parcial", "nao"]:
        n = int((s.c2_tem_reserva == c).sum())
        cp.append((rot, len(s), ROT["c2_tem_reserva"][c], sup(n), pct(n, len(s))))
TAB["T7_conhec_pratica"] = salvar(pd.DataFrame(cp, columns=["grupo", "n_grupo", "c2_tem_reserva", "n", "pct"]), "T7_conhec_pratica")
_, p_esc_res = fisher_2x2((df.escore == 4).astype(int), df.tem_alguma_reserva)
rho_esc_c2, p_esc_c2 = stats.spearmanr(df.escore, df.c2_tem_reserva.map({"nao": 0, "parcial": 1, "sim": 2}))
rho_c6_c2, p_c6_c2 = stats.spearmanr(df.c6_poupa_regular.map({"nao": 0, "as_vezes": 1, "sim": 2}),
                                     df.c2_tem_reserva.map({"nao": 0, "parcial": 1, "sim": 2}))
rho_c1_c2, p_c1_c2 = stats.spearmanr(df.c1_orcamento.map({"nunca": 0, "as_vezes": 1, "sempre": 2}),
                                     df.c2_tem_reserva.map({"nao": 0, "parcial": 1, "sim": 2}))
# opinião sobre tamanho x cobertura real entre quem acha 3+ meses adequado
acha3 = df.b2_reserva_meses.isin(["3_6", "mais_6"])
tem3 = df.c3_reserva_cobertura.isin(["3_6", "mais_6"])
gap = (int(acha3.sum()), int((acha3 & ~tem3).sum()))

# ---------------------------------------------------------------- Família
fam = []
for v, rot in [("d2_fam_conversa", "Conversam sobre dinheiro (d2)"), ("d3_fam_orcamento", "Família controla orçamento (d3)"),
               ("d4_fam_reserva", "Família tem reserva (d4)"), ("d5_fam_dividas", "Família tem dívidas em atraso (d5)"),
               ("d6_fam_conhecimento", "Conhecimento da família, 1 a 5 (d6)")]:
    for _, r in freq(v).iterrows():
        fam.append((rot, r.categoria, r.n, r.pct, r.base))
TAB["T8_familia"] = salvar(pd.DataFrame(fam, columns=["indicador", "categoria", "n", "pct", "base"]), "T8_familia")
nao_sabe_d4_d5 = int(((df.d4_fam_reserva == "nao_sei") | (df.d5_fam_dividas == "nao_sei")).sum())
nao_sabe_ambos = int(((df.d4_fam_reserva == "nao_sei") & (df.d5_fam_dividas == "nao_sei")).sum())

# família x estudante
fe = []
for c, rot in [("sim", "Família tem reserva"), ("nao", "Família não tem reserva"), ("nao_sei", "Não sabe se a família tem")]:
    s = df[df.d4_fam_reserva == c]
    n = int(s.tem_alguma_reserva.sum())
    fe.append(("Estudante tem alguma reserva (c2 = Sim ou Parcialmente)", rot, len(s), sup(n), pct(n, len(s))))
for c, rot in [("frequente", "Conversam frequentemente"), ("as_vezes", "Conversam às vezes"), ("nunca", "Nunca conversam")]:
    s = df[df.d2_fam_conversa == c]
    n = int((s.c6_poupa_regular == "sim").sum())
    fe.append(("Estudante poupa todo mês (c6 = Sim)", rot, len(s), sup(n), pct(n, len(s))))
for c, rot in [("frequente", "Conversam frequentemente"), ("as_vezes", "Conversam às vezes"), ("nunca", "Nunca conversam")]:
    s = df[df.d2_fam_conversa == c]
    fe.append(("Escore médio de conhecimento, 0 a 4 (H4)", rot, len(s), "", round(s.escore.mean(), 2) if len(s) >= MIN else ""))
TAB["T9_familia_estudante"] = salvar(pd.DataFrame(fe, columns=["indicador", "grupo", "n_grupo", "n", "pct_ou_media"]), "T9_familia_estudante")
ct_res, p_fam_res = fisher_2x2((df.d4_fam_reserva == "sim").astype(int), df.tem_alguma_reserva)
or_fam = (ct_res.loc[1, 1] * ct_res.loc[0, 0]) / (ct_res.loc[1, 0] * ct_res.loc[0, 1])
ct_conv, p_conv_poupa = fisher_2x2((df.d2_fam_conversa == "frequente").astype(int), (df.c6_poupa_regular == "sim").astype(int))
kw_h4 = stats.kruskal(*[df[df.d2_fam_conversa == c].escore for c in ["nunca", "as_vezes", "frequente"]]).pvalue
rho_d6, p_d6 = stats.spearmanr(df.d6, df.escore, nan_policy="omit")
# renda familiar como possível confundidor da relação reserva família x estudante
renda_alta = df.d1_renda_familiar == "mais_6"
fam_res_por_renda = df.groupby(renda_alta.map({True: "Mais de 6 SM", False: "Até 6 SM, não sabe ou PNR"})).apply(
    lambda s: pd.Series({"n": len(s), "fam_reserva_pct": round(100 * (s.d4_fam_reserva == "sim").mean(), 1),
                         "est_alguma_reserva_pct": round(100 * s.tem_alguma_reserva.mean(), 1)}))
salvar(fam_res_por_renda.reset_index(names="renda_familiar"), "T9b_renda_familiar_reservas")

# ---------------------------------------------------------------- Glossário
gl = []
for v, rot, m in [("e1_temas_interesse", "Temas desejados (e1, até 3)", True), ("e3_termo_prioritario", "Termo prioritário (e3)", False),
                  ("e2_usaria_glossario", "Usaria o glossário (e2)", False), ("d7_educ_recebida", "Onde teve contato com educação financeira (d7, múltipla)", True)]:
    t = freq(v, multipla=m)
    if m or v == "e3_termo_prioritario":
        t = t.assign(_o=pd.to_numeric(t.n, errors="coerce").fillna(0)).sort_values("_o", ascending=False).drop(columns="_o")
    for _, r in t.iterrows():
        gl.append((rot, r.categoria, r.n, r.pct, r.base))
TAB["T10_glossario"] = salvar(pd.DataFrame(gl, columns=["indicador", "categoria", "n", "pct", "base"]), "T10_glossario")

# ---------------------------------------------------------------- Hipóteses
pct_res_sim = round(100 * (df.c2_tem_reserva == "sim").mean(), 1)
pct_alguma = round(100 * df.tem_alguma_reserva.mean(), 1)
hip = pd.DataFrame([
    ("H1: a minoria dos estudantes tem reserva", f"Reserva completa (Sim): {pct_res_sim}%; alguma reserva (Sim ou Parcial): {pct_alguma}%; reserva ≥ 3 meses: {round(100*reserva_3m/N,1)}%",
     "Depende da definição: confirmada para reserva completa e para reserva ≥ 3 meses; não confirmada para 'alguma reserva'"),
    ("H2: mais estudantes reconhecem o conceito do que o praticam", f"Acertam b1: {round(100*df.b1_reserva_def_ok.mean(),1)}%; têm reserva completa: {pct_res_sim}%",
     "Compatível com os dados"),
    ("H3: escore maior em Economia", f"Escore médio 0–4: Economia {esc_grupo[0][2]} × demais {esc_grupo[1][2]} (Mann-Whitney p = {mw['escore']:.2f})",
     "Não há diferença perceptível nesta amostra"),
    ("H4: escore maior quando a família conversa sobre dinheiro", "Escore médio: frequentemente %.2f; às vezes %.2f; nunca %.2f (Kruskal-Wallis p = %.2f)" % (*[df[df.d2_fam_conversa == c].escore.mean() for c in ['frequente', 'as_vezes', 'nunca']], kw_h4),
     "Não confirmada; a direção observada não é a esperada"),
], columns=["hipotese", "evidencia", "leitura_preliminar"])
TAB["T11_hipoteses"] = salvar(hip, "T11_hipoteses")

# ---------------------------------------------------------------- Figuras
plt.rcParams.update({"font.family": ["Times New Roman", "Liberation Serif", "DejaVu Serif"], "font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 200})
AZUL, CINZA, LARANJA = "#2f5d8a", "#9aa5b1", "#c8742c"


def barh(labels, vals, ns, arquivo, xlabel, cores=None, xmax=100):
    fig, ax = plt.subplots(figsize=(6.3, 0.45 * len(labels) + 0.9))
    y = np.arange(len(labels))[::-1]
    ax.barh(y, vals, color=cores or AZUL, height=0.6)
    for yi, v, n in zip(y, vals, ns):
        ax.text(v + 1, yi, f"{v:.1f}%".replace(".", ",") + (f" ({n})" if n is not None else ""), va="center", fontsize=10)
    ax.set_yticks(y, labels)
    ax.set_xlim(0, xmax)
    ax.set_xlabel(xlabel)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    fig.savefig(SAIDA / "figuras" / arquivo)
    plt.close(fig)


# Fig 1: acerto por item
t3 = TAB["T3_acertos"]
lab = ["Definição de reserva (b1)", "Diversificação (b5)", "Inflação (b3)", "Juros compostos (b4)", "Local da reserva (b7)*"]
ordem = [0, 3, 1, 2, 4]
barh(lab, [t3.acertos_pct_total[i] for i in ordem], [t3.acertos_n[i] for i in ordem], "fig1_acerto_por_item.png",
     "% de respondentes que escolheram a opção correta (n = 60)",
     cores=[AZUL, AZUL, AZUL, LARANJA, LARANJA])

# Fig 2: conhecimento x prática (escadinha conceito -> prática)
etapas = [("Acerta o conceito de reserva (b1)", df.b1_reserva_def_ok.sum()),
          ("Tem alguma reserva (c2 Sim/Parcial)", df.tem_alguma_reserva.sum()),
          ("Diz ter reserva completa (c2 Sim)", (df.c2_tem_reserva == "sim").sum()),
          ("Reserva cobre 3 meses ou mais (c3)", reserva_3m),
          ("Planeja sempre os gastos (c1)", (df.c1_orcamento == "sempre").sum())]
barh([e[0] for e in etapas], [100 * e[1] / N for e in etapas], [int(e[1]) for e in etapas], "fig2_conceito_vs_pratica.png",
     "% do total de respondentes (n = 60)", cores=[AZUL, CINZA, CINZA, LARANJA, LARANJA])

# Fig 3: reserva do estudante x reserva da família
fig, ax = plt.subplots(figsize=(6.3, 2.6))
grupos = [("Família tem reserva", df.d4_fam_reserva == "sim"), ("Família não tem\nou não sabe", df.d4_fam_reserva != "sim")]
cats = [("sim", "Sim", AZUL), ("parcial", "Parcialmente", "#7fa7cc"), ("nao", "Não", LARANJA)]
for i, (g, m) in enumerate(grupos[::-1]):
    s = df[m]; left = 0
    for c, rot, cor in cats:
        v = 100 * (s.c2_tem_reserva == c).mean()
        ax.barh(i, v, left=left, color=cor, height=0.55, label=rot if i == 0 else None)
        if v >= 8:
            ax.text(left + v / 2, i, f"{v:.0f}%", ha="center", va="center", color="white", fontsize=10)
        left += v
    ax.text(101, i, f"n = {m.sum()}", va="center", fontsize=10)
ax.set_yticks([0, 1], [g for g, _ in grupos[::-1]])
ax.set_xlim(0, 112); ax.set_xlabel("% dos estudantes do grupo, segundo se têm reserva de emergência (c2)")
ax.legend(ncol=3, frameon=False, loc="upper center", bbox_to_anchor=(0.45, 1.28))
ax.tick_params(axis="y", length=0)
fig.tight_layout(); fig.savefig(SAIDA / "figuras" / "fig3_reserva_familia_estudante.png"); plt.close(fig)

# Fig 4: temas do glossário
t = freq("e1_temas_interesse", multipla=True)
t = t[t.categoria != "Outro"].assign(nn=lambda x: pd.to_numeric(x.n, errors="coerce")).sort_values("nn", ascending=False)
barh(list(t.categoria), list(t.pct.astype(float)), list(t.n), "fig4_temas_glossario.png",
     "% de respondentes que marcaram o tema (até 3 por pessoa; n = 60)")

# Fig 5: distribuição do escore
fig, ax = plt.subplots(figsize=(5.5, 2.8))
ax.bar(dist.index, 100 * dist.values / N, color=[CINZA, CINZA, CINZA, "#7fa7cc", AZUL], width=0.65)
for x, n in zip(dist.index, dist.values):
    ax.text(x, 100 * n / N + 1.5, "<5" if 0 < n < MIN else f"{100*n/N:.1f}%".replace(".", ","), ha="center", fontsize=10)
ax.set_xticks(range(5)); ax.set_xlabel("Escore de conhecimento (acertos em b1, b3, b4 e b5)"); ax.set_ylabel("% (n = 60)")
ax.set_ylim(0, 75); fig.tight_layout(); fig.savefig(SAIDA / "figuras" / "fig5_distribuicao_escore.png"); plt.close(fig)

# ---------------------------------------------------------------- resumo para o texto
R = dict(
    n_bruto=n_bruto, N=N, dup=dup, sem_consent=sem_consent, periodo=periodo, antes_periodo=antes_periodo,
    por_dia=por_dia, inval=inval, info=info, b7v=b7v, erros=erros, reserva_3m=reserva_3m, tem_div=tem_div,
    div_eco=div_eco, p_div=p_div, p_esc_res=p_esc_res, rho_esc_c2=(rho_esc_c2, p_esc_c2), rho_c6_c2=(rho_c6_c2, p_c6_c2),
    rho_c1_c2=(rho_c1_c2, p_c1_c2), gap=gap, nao_sabe_d4_d5=nao_sabe_d4_d5, nao_sabe_ambos=nao_sabe_ambos,
    p_fam_res=p_fam_res, or_fam=or_fam, ct_res=ct_res, p_conv_poupa=p_conv_poupa, kw_h4=kw_h4, rho_d6=(rho_d6, p_d6),
    rho_b6=(rho_b6, p_b6), mw=mw, fam_res_por_renda=fam_res_por_renda,
    escore_medio=df.escore.mean(), nota6=df.nota6.mean(), big3_todos=int((df.big3 == 3).sum()),
    v1=int((df.versao_form == "v1").sum()), v2=int((df.versao_form == "v2").sum()),
    eco_v1=int(((df.versao_form == "v1") & (df.curso2 == "Ciências Econômicas")).sum()),
    nivel=df.nivel.value_counts().to_dict(),
)
if __name__ == "__main__":
    print(f"Tabelas e figuras gravadas em {SAIDA}")
    import pprint
    pprint.pprint({k: v for k, v in R.items() if k != "por_dia"}, width=140)
    print(por_dia)
    for k, t in TAB.items():
        print("\n==", k); print(t.to_string(index=False))
