from fastapi import APIRouter
from app.reports.hiring_quarterly_report import get_hiring_quarterly_report
from app.reports.hiring_above_average import generate_hiring_above_average_report

router = APIRouter()

@router.get("/hiring-quarterly", summary="Hiring Quartely Report 2021", tags=["Reports"])
def hiring_quarterly_report():
    return get_hiring_quarterly_report()

@router.get("/hiring-above-average", summary="Hiring Above Average Report 2021", tags=["Reports"])
def hiring_above_average():
    return generate_hiring_above_average_report()
