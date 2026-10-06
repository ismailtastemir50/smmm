from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from decimal import Decimal


class DepoGirisCreate(BaseModel):
    tarih: date
    depo_id: int
    cesit_id: int
    ebat_id: int
    parti_id: int
    hasat_yeri_id: Optional[int] = None
    tedarikci_id: Optional[int] = None
    arac_plaka: Optional[str] = None
    giris_kg: Decimal = Field(..., gt=0)
    kasa_adet: Optional[int] = None
    aciklama: Optional[str] = None