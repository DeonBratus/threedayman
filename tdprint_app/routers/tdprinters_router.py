from fastapi import APIRouter
from pydantic import BaseModel
from services.tdprinter_service import TdPrinterService

class Printer(BaseModel):
    name: str
    addr: str
    clustername: str

printers_api = APIRouter(prefix="/api/printers")

@printers_api.post('/')
async def add_printer(printer: Printer):
    printers_service = TdPrinterService()
    printers_service.add_printer(name=printer.name, addr=printer.addr, clustername=printer.clustername)
    return {"name": printer.name, "addr": printer.addr, "clustername": printer.clustername}

@printers_api.get('/')
async def get_printers():
    printers_service = TdPrinterService()
    data = printers_service.get_printers()
    return data