from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models import Kullanici

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def hash_sifre(sifre: str) -> str:
    return pwd_context.hash(sifre)


def dogrula_sifre(sifre: str, hash_: str) -> bool:
    return pwd_context.verify(sifre, hash_)


def token_olustur(kullanici_adi: str, rol: str) -> str:
    exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": kullanici_adi, "rol": rol, "exp": exp}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def aktif_kullanici(token: str = Depends(oauth2_scheme),
                    db: Session = Depends(get_db)) -> Kullanici:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        kullanici_adi = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Gecersiz token")
    kullanici = db.query(Kullanici).filter(Kullanici.kullanici_adi == kullanici_adi).first()
    if not kullanici or not kullanici.aktif:
        raise HTTPException(status_code=401, detail="Kullanici bulunamadi")
    return kullanici