from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request

from ozz_backend import app_logger
from ozz_backend.persistence_layer import Material


router = APIRouter(
    prefix="/material",
    tags=["material"],
    # dependencies=[Depends(get_token_header)],
)


class MaterialIn(BaseModel):
    mission_id: int


class MaterialOut(BaseModel):
    id: int
    material_name: str
    material_type: str
    thumbnail_path: str
    cd_name: str


class MaterialOutList(BaseModel):
    materials: list[dict]


@router.get('/test')
def test_api():
    app_logger.info('test')
    return {'test'}


@router.get('/mission-materials', response_model=MaterialOutList)
def get_materials(request: Request, mission_id: int):
    app_logger.info(f'[{request.method}] {request.url}: {request.client.host}:{request.client.port}')
    results = Material.get_material_with_mission_id(mission_id)
    materials = [MaterialOut(id=result.id,
                             material_name=result.material_name,
                             material_type=result.material_type,
                             thumbnail_path=result.thumbnail_path,
                             cd_name=result.cd_name).dict() for result in results]
    return {'materials': materials}
