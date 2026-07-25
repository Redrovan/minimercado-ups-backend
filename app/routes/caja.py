from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.schemas import CajaCerrarCreate, CajaCreate, CajaResponse, MovimientoCajaCreate, MovimientoCajaResponse
from app.services.caja_service import CajaService
from app.utils.dependencies import get_db

router = APIRouter(prefix="/caja", tags=["Caja"])
service = CajaService()


@router.post("/abrir", response_model=CajaResponse)
def abrir_caja(payload: CajaCreate, db: Session = Depends(get_db)):
    return service.abrir_caja(db, payload)


@router.get("/abierta", response_model=CajaResponse)
def obtener_caja_abierta(db: Session = Depends(get_db)):
    return service.obtener_caja_abierta(db)


@router.post("/{caja_id}/cerrar", response_model=CajaResponse)
def cerrar_caja(caja_id: int, payload: CajaCerrarCreate, db: Session = Depends(get_db)):
    return service.cerrar_caja(db, caja_id, payload.saldo_final)


@router.get("/{caja_id}/movimientos", response_model=list[MovimientoCajaResponse])
def movimientos(caja_id: int, db: Session = Depends(get_db)):
    return service.listar_movimientos(db, caja_id)


@router.post("/movimientos", response_model=MovimientoCajaResponse)
def crear_movimiento(payload: MovimientoCajaCreate, db: Session = Depends(get_db)):
    return service.registrar_movimiento(db, payload)