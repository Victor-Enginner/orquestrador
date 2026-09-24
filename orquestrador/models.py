"""Modelos do orquestrador — objetos do grafo (texto colado §1:
Ideia → resolve Problema / atende Público / sustentada_por Evidência /
testada_por Experimento MatrAIx / recebeu Objeção / resultou_em Decisão).

Classes de estado (princípio do portfólio: nada finge funcionar):
- implementado: estrutura de dados + serialização
- simulação determinística: resultados do motor MatrAIx (adapter)
- futuro: integração com a lib semantica-agi real (provenance/confiança real)
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class Namespace(str, Enum):
    """Namespaces do ContextGraph compartilhado (texto colado §3)."""

    DISCOVERY = "discovery"
    VALIDATION = "validation"
    MATRAIX = "matraix"
    PRODUCTION = "production"
    DISTRIBUTION = "distribution"
    OPTIMIZATION = "optimization"


@dataclass
class Evidencia:
    url: str
    trecho: str
    fonte: str        # "interna" | "externa"
    confianca: float  # 0..1 — atribuída pelo agente que registra


@dataclass
class Persona:
    id: str
    perfil: str
    orcamento_faixa: str
    ceticismo: float  # 0..1 — reduz conversão simulada


@dataclass
class RespostaPersona:
    persona_id: str
    estagio: str      # "interesse" | "objecao" | "conversao"
    resposta: str
    aceitou: bool


@dataclass
class SimulacaoMatrAIx:
    ideia_id: str
    versao_motor: str
    interesse_medio: float
    objecoes: list[str]
    taxa_conversao_simulada: float
    respostas: list[RespostaPersona] = field(default_factory=list)
    nota: str = "SIMULAÇÃO DETERMINÍSTICA — não é evidência de demanda real"


@dataclass
class Veredito:
    aprovada: bool
    justificativa: str
    regras_aplicadas: list[str] = field(default_factory=list)


@dataclass
class RegistroDecisao:
    etapa: str  # discovery | validation | production | ...
    agente: str
    ideia_id: str
    decisao: str
    justificativa: str
    evidencias: list[Evidencia] = field(default_factory=list)
    simulacao: Optional[dict] = None
    veredito: Optional[Veredito] = None


@dataclass
class Ideia:
    id: str
    titulo: str
    problema: str
    publico: str
    ativo: str
    faixa_preco: str
    evidencias: list[Evidencia] = field(default_factory=list)
    bloqueadores: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
