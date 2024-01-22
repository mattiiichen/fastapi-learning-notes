from uuid import UUID

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from lagom import Container
from lagom.integrations.fast_api import FastApiIntegration

from repository.complaints import BadRecipeRepository

container = Container()
container[BadRecipeRepository] = BadRecipeRepository()
# container[BadRecipeRepository] = Singleton(BadRecipeRepository) #another way

router = APIRouter()
deps = FastApiIntegration(container, request_singletons=[BadRecipeRepository])


@router.post("/complaint/recipe", summary='回報食譜抱怨',tags=['抱怨'])
def report_recipe(rid: UUID, complaintservice=deps.depends(BadRecipeRepository)):
    complaintservice.add_bad_recipe(rid)
    return JSONResponse(content={"message": "reported bad recipe"}, status_code=201)


@router.get("/complaint/list/all", summary='取得全部抱怨清單',tags=['抱怨'])
def list_defective_recipes(complaintservice=deps.depends(BadRecipeRepository)):
    defects_list = jsonable_encoder(complaintservice.query_bad_recipes())
    return defects_list
