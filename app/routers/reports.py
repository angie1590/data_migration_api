from fastapi import APIRouter
from app.reports.hiring_quarterly_report import get_hiring_quarterly_report

router = APIRouter()

@router.get("/hiring-quarterly", summary="Hiring Quartely Report 2021", tags=["Reports"])
def hiring_report():
    return get_hiring_quarterly_report()
