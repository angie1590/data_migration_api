from fastapi import APIRouter
from app.reports.hiring_quarterly_report import get_hiring_quarterly_report
from app.reports.hiring_above_average import generate_hiring_above_average_report

router = APIRouter()

@router.get("/hiring-quarterly", summary="Hiring Quartely Report 2021", tags=["Reports"])
def hiring_quarterly_report():
    result = get_hiring_quarterly_report()
    data = [row.asDict() for row in result.collect()]
    return data

@router.get("/hiring-above-average", summary="Hiring Above Average Report 2021", tags=["Reports"])
def hiring_above_average():
    result = generate_hiring_above_average_report()
    data = [row.asDict() for row in result.collect()]
    return data
