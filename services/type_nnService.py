from models.type_nnModels import type_nn, type_nn_pydantic


async def get_all_types_nn():
    return await type_nn_pydantic.from_queryset(type_nn.all())


async def get_type_nn(type_nn_id: int):
    return await type_nn_pydantic.from_queryset_single(type_nn.get(id = type_nn_id))
    