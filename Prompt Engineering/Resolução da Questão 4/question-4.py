"""
Questão 4

Prompt:
Contexto:
Você é uma IA especializada em gerar código com base em requisitos técnicos.

Tarefa:
Crie um endpoint em FastAPI que receba e valide um objeto Item com as regras:

nome: string, máximo 25 caracteres.
valor: float.
data: formato YYYY-MM-DD, não pode ser futura.
Após validação, adicione ao objeto um campo uuid gerado dinamicamente.
Retorne o objeto validado e atualizado.
Gerar uuid automaticamente em cada requisição.

"""

from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from uuid import uuid4
from fastapi import FastAPI

app = FastAPI()

class Item(BaseModel):
    nome: str = Field(..., max_length=25, description="Nome descritivo do item. Limite de 25 caracteres.")
    valor: float = Field(..., description="Preço ou valor monetário associado ao item.")
    data: str = Field(..., description="Data de referência no formato AAAA-MM-DD. A data não pode ser futura.")

    @field_validator("data")
    def validar_formato_e_logica_data(cls, v):
        try:
            data_objeto = datetime.strptime(v, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de data inválido. Utilize AAAA-MM-DD.")
        
        if data_objeto > date.today():
            raise ValueError("A data informada não pode ser no futuro.")
        
        return v

@app.post("/processar-item", response_model=dict)
async def processar_item(item: Item):
    # Converte o modelo para um dicionário
    item_processado = item.model_dump()
    
    # Adiciona um identificador único ao dicionário do item
    item_processado["uuid"] = str(uuid4())
    
    return item_processado