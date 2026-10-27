"""Valida data/glossario.json.

Verifica: campos obrigatórios, tipos, termos duplicados (pelo mesmo slug usado
no site), temas vazios e links "relacionados" que não existem.

Uso (a partir da raiz do repositório):
    python3 notebooks/01_validar_glossario.py
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

CAMINHO = Path(__file__).resolve().parent.parent / "data" / "glossario.json"
OBRIGATORIOS = ["termo", "definicao"]
RECOMENDADOS = ["tema", "exemplo", "importa"]


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", str(s or ""))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", norm(s)).strip("-")


def main() -> int:
    try:
        dados = json.loads(CAMINHO.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERRO: não foi possível ler {CAMINHO}: {e}")
        return 1

    if not isinstance(dados, list):
        print("ERRO: o arquivo deve conter uma lista de verbetes.")
        return 1

    erros, avisos = [], []
    slugs = {}
    for i, v in enumerate(dados, start=1):
        if not isinstance(v, dict):
            erros.append(f"#{i}: item não é um objeto")
            continue
        nome = v.get("termo") or f"(sem termo, item {i})"
        for campo in OBRIGATORIOS:
            if not str(v.get(campo, "")).strip():
                erros.append(f"{nome}: campo obrigatório '{campo}' vazio ou ausente")
        for campo in RECOMENDADOS:
            if not str(v.get(campo, "")).strip():
                avisos.append(f"{nome}: campo recomendado '{campo}' vazio")
        if "relacionados" in v and not isinstance(v["relacionados"], list):
            erros.append(f"{nome}: 'relacionados' deve ser uma lista")
        if v.get("termo"):
            s = slug(v["termo"])
            if s in slugs:
                erros.append(f"{nome}: termo duplicado de '{slugs[s]}' (mesmo identificador '{s}')")
            slugs[s] = nome

    for v in dados:
        if isinstance(v, dict) and isinstance(v.get("relacionados"), list):
            for r in v["relacionados"]:
                if slug(r) not in slugs:
                    avisos.append(f"{v.get('termo')}: 'Veja também' aponta para '{r}', que não existe (o site oculta o link)")

    print(f"{len(dados)} verbetes lidos de {CAMINHO.name}")
    for a in avisos:
        print("AVISO:", a)
    for e in erros:
        print("ERRO: ", e)
    print("OK: nenhum erro." if not erros else f"{len(erros)} erro(s).")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
