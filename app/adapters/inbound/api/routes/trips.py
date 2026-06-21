from fastapi import APIRouter

router = APIRouter()


@router.get(
    '',
    description='Cria uma viagem'
)
async def get_trips():
    return {
        "trips": 'test'
    }
