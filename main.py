# from itertools import count
# from tokenize import String
from typing import Dict
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import os
import util
from models import AlteraCurso, Curso

security = HTTPBearer()
API_TOKEN = os.environ.get("API_TOKEN", "meu_token_seguro")

def validar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.scheme.lower() != "bearer" or credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou ausente",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return credentials.credentials

global dbcursos_json
global cursos

util.Cabecalho()
cursos = util.InicializaArquivo()
app = FastAPI(
    title="QA br Treinamento REST",
    version="1.0.0",
    description="QAonline BR",
    openapi_url="/restcurso.json",
    dependencies=[Depends(validar_token)],
)
print("")
print(cursos)

@app.get('/cursos', 
         description="Retornas todos os Curso",
         summary="Retorna todos dos cursos",
         response_model=Dict[str, Curso],
         response_description="Cursos encontrados com sucesso!"
         ) 
async def get_cursos():
    print(type(cursos))
    return cursos

@app.get('/cursos/{curso_id}', 
         description="Retornas o Curso referente ao ID",
         summary="Retorna Curso pelo ID")
async def get_curso(curso_id: int):
    int_keys = [int(key) for key in cursos.keys()]
    try:
        curso = cursos[str(curso_id)]
        print(curso)
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID Curso id {curso_id} não encontrado..."
        )
        
@app.get('/cursos/titulo/{titulo}',
         description="Retorna todos os cursos cujo título começa com o nome fornecido",
         summary="Retorna cursos pelo primeiro nome do título")
async def get_curso_por_titulo(titulo: str):
    cursos_filtrados = {
        curso_id: curso
        for curso_id, curso in cursos.items()
        if curso["dados"]["titulo"].lower().startswith(titulo.lower())
    }
    if not cursos_filtrados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhum curso encontrado com o primeiro nome '{titulo}'"
        )
    return cursos_filtrados
        
@app.post('/cursos', 
        status_code=status.HTTP_201_CREATED, 
        description="Inclui um curso Novo no com ID Incremental",
        summary="Inclui um curso novo e seu ID")
async def post_curso(curso: Curso):
    if curso.id is not None and str(curso.id) in cursos.keys():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                             detail=f"Já existe um curso com ID: {curso.id}.")

    int_keys = [int(k) for k in cursos.keys()]
    next_id = max(int_keys) + 1 if int_keys else 1
    curso_dict = curso.dict()
    curso_dict["id"] = next_id
    cursos[str(next_id)] = curso_dict
    return curso_dict
         
@app.patch('/cursos/{curso_id}', 
        description="Atualiza dados do Curso pelo ID",
        summary="Atualiza dados do curso pelo ID")
async def path_curso(curso_id: int, curso: AlteraCurso):
    if str(curso_id) not in cursos:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Curso id {curso_id} não encontrado..."
        )

    curso_atualizado = cursos[str(curso_id)].copy()
    update_data = curso.dict(exclude_unset=True)
    update_data.pop("id", None)

    if "dados" in update_data and update_data["dados"] is not None:
        dados_update = update_data["dados"]
        if dados_update.get("titulo") is not None:
            curso_atualizado["dados"]["titulo"] = dados_update["titulo"]
        if dados_update.get("meta") is not None:
            curso_atualizado["dados"]["meta"].update({
                k: v for k, v in dados_update["meta"].items() if v is not None
            })

    cursos[str(curso_id)] = curso_atualizado
    return {"mensagem": f"Curso id {curso_id} atualizado com sucesso..."}
         
@app.delete('/cursos/{curso_id}', 
         description="Exclui Curso pelo ID informado",
         summary="Remove um Curso pelo ID")
async def del_curso(curso_id: int):
    if str(curso_id) in cursos:
        del cursos[str(curso_id)]
        return {"mensagem":f"Curso ID:{curso_id} removido com SUCESSO..."}
    else:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID Curso id {curso_id} não encontrado..."
        )
       
# Execução pelo Main

# if __name__ == "__main__":
#     print("Execute o servidor usando o comando: uvicorn nome_do_arquivo:app --reload")
#     import uvicorn
#     # # uvicorn.run("main:app", host="0.0.0.0", port=8000, 
#     # #             log_level="debug", reload=True)
#     # uvicorn.run("main:app", host="0.0.0.0", port=8000, 
#     #             log_level="debug")
#     uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug") 