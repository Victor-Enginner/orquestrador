"""Adapter Semantica — ContextGraph em JSONL append-only.

O texto-fonte define o Semantica como 'memória, grafo de conhecimento e
camada de auditoria' com namespaces (discovery/, validation/, matraix/...).
Implementação HONESTA do MVP: grafo em arquivo JSONL (append-only,
inspecionável, commitável). NÃO é a lib semantica-agi real — a integração
real (provenance, confiança calculada, citações, histórico de transformação)
é FUTURO e está marcado como tal no DECISIONS.md.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from orquestrador.models import Namespace


class ContextGraph:
    def __init__(self, caminho: str | Path):
        self.caminho = Path(caminho)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)

    def registrar(self, ns: Namespace, tipo: str, payload: dict) -> dict:
        evento = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "ns": ns.value,
            "tipo": tipo,
            "payload": payload,
        }
        with self.caminho.open("a", encoding="utf-8") as f:
            f.write(json.dumps(evento, ensure_ascii=False) + "\n")
        return evento

    def consultar(self, ns: Namespace | None = None, tipo: str | None = None) -> list[dict]:
        if not self.caminho.exists():
            return []
        out = []
        for linha in self.caminho.read_text(encoding="utf-8").splitlines():
            if not linha.strip():
                continue
            ev = json.loads(linha)
            if ns and ev["ns"] != ns.value:
                continue
            if tipo and ev["tipo"] != tipo:
                continue
            out.append(ev)
        return out
