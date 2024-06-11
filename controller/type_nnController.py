from fastapi import APIRouter

from services.type_nnService import get_all_types_nn, get_type_nn

router = APIRouter()

@router.get("/type_nn", tags=["Type_NN"])
async def get_all_type_nn():
    response = await get_all_types_nn()
    return {"status": "ok", "data" : response}


@router.get("/type_nn/{type_nn_id}", tags=["Type_NN"])
async def get_type_nn_id(type_nn_id: int):
    response = await get_type_nn(type_nn_id)
    return {"status": "ok", "data" : response}
