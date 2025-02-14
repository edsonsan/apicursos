from itertools import count
from tokenize import String
from typing import Dict, List, Optional
from fastapi import FastAPI, responses
from fastapi import HTTPException
from fastapi import status
import os
import json
import util
from models import AlteraCurso, Curso

global dbcursos_json

util.Cabecalho()
cursos = util.InicializaArquivo()
app = FastAPI(title="QA br Treinamento REST",  
              version= "1.0.0",         
              description="QAonline BR")
print("")
print(cursos)

@app.get('/cursos', 
         description="Retornas todos os Curso",
         summary="Retorna todos dos cursos",
         response_model=Dict[int, Curso],
        #  response_model=Curso,
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
        if curso_id <= 19 :
            curso = cursos[str(curso_id)]
        else:
            curso = cursos[curso_id]
        print(curso)
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID Curso id {curso_id} não encontrado..."
        )
        
@app.get('/cursos/titulo/{titulo}',
        description="Retorna o Curso referente ao título informado",
        summary="Retorna Curso pelo Título")
async def get_curso_por_titulo(titulo: str):
    # Procura um curso com o título fornecido
    for curso_id, curso in cursos.items():
        if curso["titulo"].lower() == titulo.lower():
            return curso
    
    # Se não encontrar, levanta uma exceção
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Curso com título '{titulo}' não encontrado..."
    )
   
        
@app.post('/cursos', 
        status_code=status.HTTP_201_CREATED, 
        description="Inclui um curso Novo no com ID Incremental",
        summary="Inclui um curso novo e seu ID")
async def post_curso(curso : Curso):
    if curso.id in cursos.keys():
        print("ID Duplicado, dados não incluidos!")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                             detail=f"Já existe um curso com ID: {curso.id}.")
    else:   
        int_keys = [int(key) for key in cursos.keys()]
    # Garante que o próximo ID seja sempre único
        next_id = (max(int_keys)) + 1     
        # Valida se o ID já existe e insere caso contrário
        if  next_id not in cursos:
            cursos[next_id] = curso
            curso.id = next_id    
        #  util.GravaArquivo(cursos)
            print(cursos)   
            return curso
         
@app.patch('/cursos/{curso_id}', 
        description="Atualiza dados do Curso pelo ID",
        summary="Atualiza dados do curso pelo ID")
async def path_curso(curso_id: int, curso: AlteraCurso):
    if curso_id in cursos:
        curso_atualizado = cursos[curso_id]
        print(curso)  
        curso.id = curso_id
        cursos[curso_id] = curso
        return cursos
    else:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID Curso id {curso_id} não encontrado..."
        )
         
@app.delete('/cursos/{curso_id}', 
         description="Exclui Curso pelo ID informado",
         summary="Remove um Curso pelo ID")
async def del_curso(curso_id: int):
    if curso_id in cursos:
        del cursos[curso_id]
        # return cursos
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