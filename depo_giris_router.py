from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import aktif_kullanici
from app.schemas import DepoGirisCreate
from app.crud import depo_giris as crud
from app.models import DepoGiris

router = APIRouter(prefix="/api/depo-giris", tags=["Depo Giris"])


@router.post("/")
def yeni_giris(veri: DepoGirisCreate,
               db: Session = Depends(get_db),
               kullanici=Depends(aktif_kullanici)):
    try:
        giris = crud.giris_olustur(db, veri, kullanici.id)
        return {"ok": True, "id": giris.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def liste(db: Session = Depends(get_db), kullanici=Depends(aktif_kullanici)):
    kayitlar = db.query(DepoGiris).order_by(DepoGiris.id.desc()).limit(100).all()
    return [
        {
            "id": k.id, "tarih": str(k.tarih),
            "depo": k.depo.ad if k.depo else "",
            "cesit": k.cesit.ad if k.cesit else "",
            "ebat": k.ebat.ad if k.ebat else "",
            "parti": k.parti.parti_no if k.parti else "",
            "giris_kg": float(k.giris_kg),
            "arac_plaka": k.arac_plaka or "",
        }
        for k in kayitlar
    ]