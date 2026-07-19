from typing import Optional
from pydantic import BaseModel

class Quantidade(BaseModel):
    aulas: int
    horas: int

class DadosCurso(BaseModel):
    titulo: str
    meta: Quantidade

class Curso(BaseModel):
    id: Optional[int] = None
    dados: DadosCurso

class AlteraQuantidade(BaseModel):
    aulas: Optional[int] = None
    horas: Optional[int] = None

class AlteraDados(BaseModel):
    titulo: Optional[str] = None
    meta: Optional[AlteraQuantidade] = None

class AlteraCurso(BaseModel):
    id: Optional[int] = None
    dados: Optional[AlteraDados] = None