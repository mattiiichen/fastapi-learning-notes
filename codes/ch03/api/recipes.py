from fastapi import APIRouter, Depends
from service.factory import get_recipe_service
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from model.recipes import Recipe
from model.classifications import Category, Origin
from typing import List
from uuid import UUID


class IngredientReq(BaseModel):
    id: UUID
    name: str
    qty: int
    measure: str


class RecipeReq(BaseModel):
    id: UUID
    name: str
    ingredients: List[IngredientReq]
    cat: Category
    orig: Origin


router = APIRouter()


@router.post("/recipes/insert", summary='新增食譜',tags=['食譜'])
def insert_recipe(recipe: RecipeReq, handler=Depends(get_recipe_service)):
    json_dict = jsonable_encoder(recipe)
    rec = Recipe(**json_dict)
    handler.add_recipe(rec)
    return JSONResponse(content=json_dict, status_code=200)


@router.get("/recipes/list/all", summary='取得食譜清單',tags=['食譜'])
def get_all_recipes(handler=Depends(get_recipe_service)):
    return handler.get_recipes()
