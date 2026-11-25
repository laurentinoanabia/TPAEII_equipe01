"""Gera uma versão do site em arquivo único, com os dados de data/*.json embutidos.

O index.html lê os dados com fetch e por isso precisa de um servidor (ou do GitHub Pages).
O arquivo gerado abre com dois cliques, sem servidor, e pode ser enviado por e-mail ou pendrive.

Uso (na raiz do repositório):
    python3 scripts/montar_site_unico.py
Saída: site_unico/glossario-da-economia.html (regenerar sempre que data/ ou index.html mudar).
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQUIVOS = ["glossario.json", "trilhas.json", "quiz.json", "indicadores.json", "projeto.json"]
MARCA = "const __DADOS = {};"

html = (RAIZ / "index.html").read_text(encoding="utf-8")
if html.count(MARCA) != 1:
    raise SystemExit(f"index.html deve conter exatamente uma vez a linha que começa com '{MARCA}'")
dados = {f"data/{n}": json.loads((RAIZ / "data" / n).read_text(encoding="utf-8")) for n in ARQUIVOS}
embutido = "const __DADOS = " + json.dumps(dados, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";"
inicio = html.index(MARCA)
fim = html.index("\n", inicio)
saida = RAIZ / "site_unico" / "glossario-da-economia.html"
saida.parent.mkdir(exist_ok=True)
saida.write_text(html[:inicio] + embutido + html[fim:], encoding="utf-8")
print(f"Gerado {saida.relative_to(RAIZ)} ({saida.stat().st_size / 1024:.0f} KB, {len(dados['data/glossario.json'])} verbetes)")
