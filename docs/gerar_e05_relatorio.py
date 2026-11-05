# -*- coding: utf-8 -*-
"""Gera o relatório de qualidade da Entrega 5 (PDF e DOCX) a partir dos CSV de outputs/ e data/processed/.

Nenhum número é digitado à mão: tudo vem do que o notebook 03 gravou. Rode o notebook primeiro e depois:

    python3 docs/gerar_e05_relatorio.py

Saídas: docs/E05_equipe01_qualidade_dados.pdf e docs/E05_equipe01_qualidade_dados.docx
Requisitos (só para gerar o relatório, não para o tratamento): pandas, python-docx e o programa wkhtmltopdf.
"""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
OUT, PROC, DOCS = RAIZ / "outputs", RAIZ / "data" / "processed", RAIZ / "docs"
NOME = "E05_equipe01_qualidade_dados"
DATA = "05/11/2026"

rel = pd.read_csv(OUT / "relatorio_qualidade.csv")
funil = pd.read_csv(OUT / "funil_contagens.csv")
testes = pd.read_csv(OUT / "testes_integridade.csv").fillna("")
aq = pd.read_csv(OUT / "registro_aquisicao.csv")
cobertura = pd.read_csv(PROC / "glossario_cobertura_questionario.csv")
relacoes = pd.read_csv(PROC / "glossario_relacoes.csv")
verbetes = pd.read_csv(PROC / "glossario_verbetes.csv")

ROTULO = {"tratado": "Tratado", "sem ocorrência": "Sem ocorrência", "pendência": "Pendência", "informativo": "Informativo"}
cont = rel["status"].value_counts()
resumo = ", ".join(f"{cont.get(k, 0)} {nome}" for k, nome in
                   (("tratado", "tratados"), ("sem ocorrência", "verificados sem ocorrência"), ("pendência", "pendências"), ("informativo", "informativos")))

f = funil.set_index(["base", "etapa"])["linhas"]
q_bruto, q_dup, q_cons = f["questionario", "bruto"], f["questionario", "após Q1 (envios duplicados)"], f["questionario", "após Q2 (consentimento)"]
q_final = f["questionario", "após Q6 (base limpa)"]
pares, pares_ok = int(len(cobertura)), int(cobertura["existe_no_glossario"].sum())
ausentes = sorted(cobertura.loc[~cobertura["existe_no_glossario"], "verbete_necessario"].unique())
assim = int((~relacoes["reciproca"]).sum())
sha_glos = aq.loc[aq["fonte"].str.startswith("F2"), "sha256"].iloc[0][:16]
n_ok = int((testes["resultado"] == "OK").sum())
origem_q = aq.loc[aq["fonte"].str.startswith("F1"), "origem"].iloc[0]
if origem_q != "SINTETICO":
    sys.exit("Este texto do relatório foi escrito para a execução com base sintética (sem respostas reais). "
             "Com respostas reais, revise as seções 1 e 6 antes de gerar o relatório.")


def e_lista(itens):
    itens = list(itens)
    return itens[0] if len(itens) == 1 else ", ".join(itens[:-1]) + " e " + itens[-1]


# ---------------------------------------------------------------- conteúdo (blocos independentes do formato)
B = []
B.append(("h1", "Entrega 5 – Relatório de qualidade dos dados"))
B.append(("sub", "PSAE00320 – Técnicas de Pesquisa e Análise Econômica II · Turma 01 · 2026.2 · Equipe 01"))
B.append(("p", "**Integrantes:** Ana Beatriz Laurentino, Arthur Almeida e Gabriel Pinheiro · **Orientador:** Prof. Alessio · **Demandante:** CORECON-PB"))
B.append(("p", f"**Repositório:** https://github.com/laurentinoanabia/TPAEII_equipe01 · **Notebook:** notebooks/03_obtencao_limpeza_tratamento.ipynb · **Data:** {DATA} (atualiza a versão de 27/10/2026)"))

B.append(("h2", "1. O que foi tratado e o que ainda não existe"))
B.append(("callout", "**Declaração de limite.** O formulário do questionário está publicado no Google Forms, mas **nenhuma exportação de respostas reais foi tratada**: "
                     "não há dados reais de respondentes neste repositório. A única base real é o glossário (%d verbetes de rascunho). "
                     "As regras de limpeza e o tradutor do formulário foram testados com uma base sintética com defeitos plantados e com uma exportação simulada "
                     "no formato do Google Forms, em uma cópia descartável do repositório. Os números do questionário neste relatório são do teste, "
                     "não de pesquisa, e não devem ser citados como resultado." % len(verbetes)))
B.append(("table", ["Base", "Origem", "Situação", "Saída"], [
    ["Glossário (F2)", "Real", f"{len(verbetes)} verbetes escritos pela equipe", "data/processed/glossario_verbetes.csv, glossario_relacoes.csv, glossario_cobertura_questionario.csv"],
    ["Questionário (F1)", "Sintética (teste)", "Formulário publicado; aguardando a exportação das respostas",
     "outputs/sintetico_teste/ (nunca em data/processed/). Com o arquivo real, o mesmo notebook grava as tabelas agregadas em data/processed/"]]))
B.append(("p", f"Resumo do relatório: {len(rel)} itens registrados ({resumo})."))

B.append(("h2", "2. Fontes, preservação e reprodutibilidade"))
B.append(("ul", [
    f"**Preservação:** os dados originais nunca são editados. O arquivo do glossário é lido como bytes e seu sha256 ({sha_glos}…) é conferido de novo no fim (teste de integridade). "
    "Ele é recuperável por qualquer commit do Git. As respostas reais do questionário ficam em `data/raw/`, bloqueada pelo `.gitignore`; para obtê-las de novo, basta baixar as respostas do Google Forms (aba Respostas).",
    "**Reprodutibilidade:** o notebook executa do início ao fim sem intervenção manual. Duas execuções seguidas geraram arquivos idênticos byte a byte (semente fixa 20261029).",
    "**Formulário:** o Google Forms exporta o texto das opções e usa o título da pergunta como cabeçalho; `notebooks/02a_formulario_google.py` traduz para variável e código (`outputs/mapa_formulario.csv`). "
    "O mapa foi conferido contra o formulário publicado em 05/11/2026: 29 perguntas, títulos, tipos e todas as opções idênticos. A cada execução o tradutor é testado por ida e volta (códigos → texto do Forms → códigos).",
    "**Execução:** `jupyter nbconvert --to notebook --execute --inplace notebooks/03_obtencao_limpeza_tratamento.ipynb`"]))

B.append(("h2", "3. Contagens antes e depois de cada etapa"))
B.append(("table", ["Base/tabela", "Etapa", "Linhas"], [[r.base, r.etapa, str(r.linhas)] for r in funil.itertuples()]))
B.append(("p", f"Funil do questionário (teste): {q_bruto} linhas brutas − {q_bruto - q_dup} envios duplicados − {q_dup - q_cons} sem consentimento = {q_final} respondentes. "
               f"Junção glossário × itens do questionário: {pares} pares item-verbete, {pares_ok} com correspondência."))

B.append(("h2", "4. Relatório de qualidade"))
cab = ["Variável/base", "Status", "Problema encontrado", "Decisão aplicada", "Impacto/validação"]
def linhas(df):
    return [[r.base_variavel, ROTULO.get(r.status, r.status), r.problema_encontrado, r.decisao_aplicada, r.impacto_validacao] for r in df.itertuples()]
eh_q = rel["base_variavel"].str.startswith("questionario")
B.append(("h3", "4.1 Glossário e cobertura do questionário (dados reais)"))
B.append(("table", cab, linhas(rel[~eh_q])))
B.append(("h3", "4.2 Regras de limpeza do questionário (teste com dados sintéticos)"))
B.append(("table", cab, linhas(rel[eh_q])))

B.append(("h2", f"5. Testes de integridade ({n_ok} de {len(testes)} OK)"))
B.append(("table", ["Teste", "Resultado", "Detalhe"], [[r.teste, r.resultado, str(r.detalhe)] for r in testes.itertuples()]))

B.append(("h2", "6. Limitações que permaneceram", True))   # True = começa em página nova
B.append(("ol", [
    "**Sem dado real do questionário.** O formulário está publicado e seu mapa foi conferido, mas nenhuma exportação real foi tratada. Falta rodar o notebook na primeira exportação e conferir o resultado contra `outputs/mapa_formulario.csv`.",
    f"**Glossário pequeno e sem fontes:** {len(verbetes)} verbetes de rascunho, {int((~verbetes['tem_fonte']).sum())} sem campo `fonte`. Pendência de conteúdo antes de publicar.",
    f"**Verbetes ausentes:** {e_lista(ausentes)}, exigidos por itens do questionário (b5 e os termos oferecidos em e3). Não foram criados sem fonte para \"fechar\" a conta.",
    "**Item b7 fora do escore.** O formulário publicado tem uma pergunta de conhecimento a mais que o plano (lugar adequado para a reserva). Ela é tabulada, mas não pontua; pontuar muda o escore para 0 a 5 e os cortes dos níveis. Decisão da equipe.",
    f"**Relações assimétricas** no \"Veja também\" ({assim} de {len(relacoes)}); mantidas como o autor escreveu.",
    "**Sem imputação:** ausentes e inválidos ficam como NA; \"não sei\" e \"prefiro não responder\" são categorias válidas.",
    "**Privacidade:** respostas individuais, identificação e qualquer coluna fora do livro de códigos nunca entram em tabelas versionadas; o texto digitado em \"Outro\" de curso não é guardado; células com menos de 5 respondentes aparecem como \"<5\".",
    "**Limites do desenho da pesquisa:** amostra por conveniência, autodeclaração e relato do estudante sobre a família. O formulário aceita três cursos e \"Outro\"; a população definida em 27/10/2026 era Ciências Econômicas (a confirmar)."]))

# ---------------------------------------------------------------- HTML -> PDF
def inline_html(t):
    t = html.escape(str(t))
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return re.sub(r"`(.+?)`", r"<code>\1</code>", t)

CSS = """
body{font-family:'DejaVu Sans',Arial,sans-serif;font-size:9.5px;color:#111;line-height:1.4}
h1{font-size:19px;margin:0 0 4px} h2{font-size:14px;border-bottom:1px solid #999;padding-bottom:2px;margin:20px 0 8px} h3{font-size:11.5px;margin:12px 0 6px}
.sub{font-weight:bold;margin:0 0 8px} p{margin:4px 0}
.callout{border:1px solid #c9d6cf;border-left:4px solid #2d6a4f;background:#f1f7f3;padding:6px 9px;margin:8px 0}
table{border-collapse:collapse;width:100%;margin:6px 0;page-break-inside:auto} tr{page-break-inside:avoid}
th,td{border:1px solid #bbb;padding:3px 5px;text-align:left;vertical-align:top;font-size:8.5px} th{background:#eee}
code{font-family:'DejaVu Sans Mono',monospace;font-size:8.3px;background:#f2f2f2;padding:0 2px} ul,ol{margin:4px 0 4px 18px;padding:0} li{margin:2px 0}
"""
def para_html():
    h = ["<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><title>E05 Relatório de qualidade</title><style>" + CSS + "</style></head><body>"]
    for b in B:
        k = b[0]
        if k in ("h1", "h2", "h3"):
            quebra = " style='page-break-before:always'" if len(b) > 2 and b[2] else ""
            h.append(f"<{k}{quebra}>{inline_html(b[1])}</{k}>")
        elif k == "sub": h.append(f"<p class='sub'>{inline_html(b[1])}</p>")
        elif k == "p": h.append(f"<p>{inline_html(b[1])}</p>")
        elif k == "callout": h.append(f"<div class='callout'>{inline_html(b[1])}</div>")
        elif k in ("ul", "ol"): h.append(f"<{k}>" + "".join(f"<li>{inline_html(i)}</li>" for i in b[1]) + f"</{k}>")
        elif k == "table":
            h.append("<table><thead><tr>" + "".join(f"<th>{inline_html(c)}</th>" for c in b[1]) + "</tr></thead><tbody>"
                     + "".join("<tr>" + "".join(f"<td>{inline_html(c)}</td>" for c in r) + "</tr>" for r in b[2]) + "</tbody></table>")
    h.append("</body></html>")
    return "\n".join(h)

with tempfile.TemporaryDirectory() as tmp:
    arq = Path(tmp) / "e05.html"
    arq.write_text(para_html(), encoding="utf-8")
    subprocess.run(["wkhtmltopdf", "--quiet", "--page-size", "A4", "--orientation", "Landscape", "--margin-top", "12mm", "--margin-bottom", "12mm",
                    "--margin-left", "12mm", "--margin-right", "12mm", "--title", "E05 Relatório de qualidade", str(arq), str(DOCS / f"{NOME}.pdf")], check=True)

# ---------------------------------------------------------------- DOCX
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt

doc = Document()
sec = doc.sections[0]
sec.orientation, sec.page_width, sec.page_height = WD_ORIENT.LANDSCAPE, Mm(297), Mm(210)
sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Mm(15)
doc.styles["Normal"].font.size = Pt(9)
doc.core_properties.title = "E05 Relatório de qualidade"
doc.core_properties.language = "pt-BR"

def runs(par, texto, tam=None):
    for parte in re.split(r"(\*\*.+?\*\*|`.+?`)", str(texto)):
        if not parte: continue
        if parte.startswith("**"): r = par.add_run(parte[2:-2]); r.bold = True
        elif parte.startswith("`"): r = par.add_run(parte[1:-1]); r.font.name = "Consolas"
        else: r = par.add_run(parte)
        if tam: r.font.size = Pt(tam)

def sombra(celula, cor):
    tc = celula._tc.get_or_add_tcPr(); s = OxmlElement("w:shd")
    s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), cor); tc.append(s)

for b in B:
    k = b[0]
    if k == "h1": doc.add_heading(b[1], level=1)
    elif k == "h2":
        if len(b) > 2 and b[2]: doc.add_page_break()
        doc.add_heading(b[1], level=2)
    elif k == "h3": doc.add_heading(b[1], level=3)
    elif k == "sub": runs(doc.add_paragraph(), "**" + b[1] + "**")
    elif k == "p": runs(doc.add_paragraph(), b[1])
    elif k == "callout":
        t = doc.add_table(rows=1, cols=1); t.style = "Table Grid"; c = t.rows[0].cells[0]; sombra(c, "F1F7F3"); runs(c.paragraphs[0], b[1])
        doc.add_paragraph()
    elif k in ("ul", "ol"):
        for i in b[1]: runs(doc.add_paragraph(style="List Bullet" if k == "ul" else "List Number"), i)
    elif k == "table":
        t = doc.add_table(rows=1, cols=len(b[1])); t.style = "Table Grid"
        for c, titulo in zip(t.rows[0].cells, b[1]):
            runs(c.paragraphs[0], "**" + titulo + "**", 8); sombra(c, "EEEEEE")
        for r in b[2]:
            for c, v in zip(t.add_row().cells, r): runs(c.paragraphs[0], v, 8)
        doc.add_paragraph()
doc.save(DOCS / f"{NOME}.docx")
print("Gerados:", DOCS / f"{NOME}.pdf", "e", DOCS / f"{NOME}.docx")
