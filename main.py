# from itertools import count
# from tokenize import String
from typing import Dict, List, Optional
from fastapi import FastAPI, responses
from fastapi import HTTPException
from fastapi import status
import os
import json
import util
from models import AlteraCurso, Curso

global dbcursos_json
global cursos

util.Cabecalho()
cursos = util.InicializaArquivo()
app = FastAPI(title="QA br Treinamento REST",  
              version= "1.0.0",         
              description="QAonline BR",
              openapi_url="/restcurso.json",)
print("")
print(cursos)

@app.get('/cursos', 
         description="Retornas todos os Curso",
         summary="Retorna todos dos cursos",
         response_model=Dict[int, Curso],
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
    # Filtra os cursos cujo título começa com o nome fornecido
    cursos_filtrados = {
        curso_id: 
            curso 
                for curso_id, curso in cursos.items()
                    if curso["titulo"].lower().startswith(titulo.lower())
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
async def post_curso(curso : Curso):
    if str(curso.id) in cursos.keys():
        print("ID Duplicado, dados não incluidos!")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                             detail=f"Já existe um curso com ID: {curso.id}.")
    
    # # Garante que o próximo ID seja sempre único
    # Gera o próximo ID
    int_keys = [int(k) for k in cursos.keys()]
    next_id = max(int_keys) + 1 if int_keys else 1
    
    # Converte Curso para dicionario
    curso_dict = curso.dict()
    
    # Adiciona o novo curso com a chave como str
    curso_dict["id"] = next_id
    cursos[str(next_id)] = curso_dict
    print(cursos)
    return curso
         
@app.patch('/cursos/{curso_id}', 
        description="Atualiza dados do Curso pelo ID",
        summary="Atualiza dados do curso pelo ID")
async def path_curso(curso_id: int, curso: AlteraCurso):
    if str(curso_id) in cursos:
        curso_atualizado = cursos[str(curso_id)]
        print(curso)  
        curso.id = curso_id
        cursos[str(curso_id)] = curso
        return {"mensagem":f"Curso id {curso_id} atualizado com sucesso..."}
    else:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Curso id {curso_id} não encontrado..."
        )
         
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