from fastapi import APIRouter, Depends
from .dependencies import get_token_header

router = APIRouter( dependencies=[Depends(get_token_header)], prefix="/companyapi", tags=["company"], responses={404: {"description": "Not found"}})


@router.get("/")
async def get_company_name():
  return {"company_name": "FastAPI Company"}

@router.get("/employees")
async def get_employees():
  return {"employees": ["John", "Jane", "Bob", "Alice"]}
