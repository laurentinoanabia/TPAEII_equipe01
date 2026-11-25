"""Monta data/pesquisa.json, lido pela página "Resultados da pesquisa" do site.

Entrada: tabelas agregadas do questionário em data/processed/questionario/ (geradas pela
análise da Entrega 6 a partir da exportação do Google Forms; células com menos de 5
respondentes já vêm como "<5"). Nenhuma resposta individual é lida aqui.

Uso (na raiz do repositório):
    python3 scripts/montar_painel_pesquisa.py
"""
import csv
import re
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
T = RAIZ / "data" / "processed" / "questionario"


def ler(nome):
    with open(T / f"{nome}.csv", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def num(x):
    x = (x or "").strip()
    if x in ("", "<5"):
        return None
    return float(x)


def virgula(texto):
    """Decimais no padrão brasileiro (73.3 -> 73,3)."""
    return re.sub(r"(\d)\.(\d)", r"\1,\2", texto)


def item(rot, n, pct, base=None):
    """n pode ser '<5'; nesse caso o percentual é omitido."""
    oculto = str(n).strip() == "<5"
    return {"rotulo": rot, "n": None if oculto else int(float(n)), "pct": None if oculto else num(pct), "base": int(float(base)) if base else None}


def linhas(tab, indicador, coluna="indicador", nomes=None):
    out = []
    for r in tab:
        if r[coluna] == indicador:
            rot = (nomes or {}).get(r["categoria"], r["categoria"])
            out.append(item(rot, r["n"], r["pct"], r.get("base")))
    return out


funil = {r["etapa"].strip(): r["n"] for r in ler("T1_funil")}
acertos = ler("T3_acertos")
escore = ler("T4_escore")
curso = {r["grupo"]: r for r in ler("T5_escore_curso")}
pratica = ler("T6_pratica")
familia = ler("T8_familia")
fam_est = ler("T9_familia_estudante")
gloss = ler("T10_glossario")
perfil = ler("T2_perfil")
hip = ler("T11_hipoteses")

N = int(funil["Base analítica"])

painel = {
    "_leia_me": "Gerado por scripts/montar_painel_pesquisa.py a partir de data/processed/questionario/. Não edite à mão.",
    "n": N,
    "coleta": "28/10 a 15/11/2026",
    "instrumento": "Questionário no Google Forms, anônimo e voluntário, 29 perguntas",
    "versoes_formulario": {"v1": int(funil["respondidas na versão 1 do formulário (28/10 a 02/11)"]),
                           "v2": int(funil["respondidas na versão 2 do formulário (05/11 a 15/11)"])},
    "perfil": {
        "curso": [item(r["categoria"], r["n"], r["pct"], N) for r in perfil if r["dimensao"] == "Curso"],
        "periodo": [item(r["categoria"], r["n"], r["pct"], N) for r in perfil if r["dimensao"] == "Período"],
        "ocupacao": [item(r["categoria"], r["n"], r["pct"], N) for r in perfil if r["dimensao"] == "Ocupação"],
        "renda_propria": [item(r["categoria"], r["n"], r["pct"], N) for r in perfil if r["dimensao"] == "Renda própria"],
    },
    "acertos": [{"rotulo": r["item"], "pct": num(r["acertos_pct_total"]), "n": int(r["acertos_n"]),
                 "economia": num(r["pct_economia_n32"]), "demais": num(r["pct_demais_n28"]), "pontua": "não pontua" not in r["item"]} for r in acertos],
    "juros_simples_erro": {"n": 13, "pct": 21.7, "nota": "escolheram R$ 1.200, resultado de juros simples"},
    "escore": [item(f"{r['escore']} acerto{'s' if r['escore'] != '1' else ''}", r["n"], r["pct"], N) for r in escore],
    "escore_medio": num(curso["Total"]["escore_0a4"]),
    "pratica": {
        "tem_reserva": linhas(pratica, "Tem reserva (c2)"),
        "cobertura": linhas(pratica, "Meses cobertos pela reserva (c3) – só quem tem reserva"),
        "onde_guarda": linhas(pratica, "Onde guarda (c4, múltipla) – só quem tem reserva"),
        "planeja": linhas(pratica, "Planeja gastos (c1)"),
        "poupa": linhas(pratica, "Poupa todo mês (c6)"),
        "dividas": linhas(pratica, "Dívidas atuais (c5, múltipla)"),
    },
    "familia": {
        "conversa": linhas(familia, "Conversam sobre dinheiro (d2)"),
        "orcamento": linhas(familia, "Família controla orçamento (d3)"),
        "reserva": linhas(familia, "Família tem reserva (d4)"),
        "reserva_estudante": [item(r["grupo"], r["n"], r["pct_ou_media"], r["n_grupo"]) for r in fam_est
                              if r["indicador"].startswith("Estudante tem alguma reserva")],
        "poupa_por_conversa": [item(r["grupo"], r["n"], r["pct_ou_media"], r["n_grupo"]) for r in fam_est
                               if r["indicador"].startswith("Estudante poupa todo mês")],
        "escore_por_conversa": [{"rotulo": r["grupo"], "base": int(r["n_grupo"]), "media": num(r["pct_ou_media"])} for r in fam_est
                                if r["indicador"].startswith("Escore médio")],
    },
    "curso": [{"rotulo": g, "n": int(curso[g]["n"]), "escore": num(curso[g]["escore_0a4"]), "autoavaliacao": num(curso[g]["autoavaliacao_1a5"])}
              for g in ("Ciências Econômicas", "Demais cursos")],
    "curso_p": {"escore": num(curso["p (Mann-Whitney)"]["escore_0a4"]), "autoavaliacao": num(curso["p (Mann-Whitney)"]["autoavaliacao_1a5"])},
    "glossario": {
        "temas": linhas(gloss, "Temas desejados (e1, até 3)"),
        "termo": linhas(gloss, "Termo prioritário (e3)"),
        "usaria": linhas(gloss, "Usaria o glossário (e2)"),
        "contato": linhas(gloss, "Onde teve contato com educação financeira (d7, múltipla)"),
    },
    "hipoteses": [{"hipotese": r["hipotese"], "evidencia": virgula(r["evidencia"]), "leitura": r["leitura_preliminar"]} for r in hip],
}

saida = RAIZ / "data" / "pesquisa.json"
saida.write_text(json.dumps(painel, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Gerado {saida.relative_to(RAIZ)} (n = {N})")
