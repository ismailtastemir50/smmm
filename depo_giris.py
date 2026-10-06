from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import DepoGiris, Stok, StokHareket
from app.schemas import DepoGirisCreate


def giris_olustur(db: Session, veri: DepoGirisCreate, kullanici_id: int):
    try:
        giris = DepoGiris(**veri.dict(), kullanici_id=kullanici_id)
        db.add(giris)
        db.flush()

        stok = db.query(Stok).filter(and_(
            Stok.depo_id == veri.depo_id,
            Stok.cesit_id == veri.cesit_id,
            Stok.ebat_id == veri.ebat_id,
            Stok.parti_id == veri.parti_id,
        )).first()

        if stok:
            stok.giris_kg = Decimal(str(stok.giris_kg)) + Decimal(str(veri.giris_kg))
            stok.kalan_kg = Decimal(str(stok.kalan_kg)) + Decimal(str(veri.giris_kg))
        else:
            stok = Stok(
                depo_id=veri.depo_id, cesit_id=veri.cesit_id,
                ebat_id=veri.ebat_id, parti_id=veri.parti_id,
                giris_kg=veri.giris_kg, kalan_kg=veri.giris_kg,
            )
            db.add(stok)

        hareket = StokHareket(
            tarih=veri.tarih, kaynak_tablo="depo_giris", kaynak_id=giris.id,
            depo_id=veri.depo_id, cesit_id=veri.cesit_id,
            ebat_id=veri.ebat_id, parti_id=veri.parti_id,
            hareket_tipi="giris", miktar_kg=veri.giris_kg,
            aciklama=veri.aciklama, kullanici_id=kullanici_id,
        )
        db.add(hareket)
        db.commit()
        db.refresh(giris)
        return giris
    except Exception as e:
        db.rollback()
        raise e