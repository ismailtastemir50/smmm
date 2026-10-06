from sqlalchemy import (
    Column, Integer, String, Numeric, Date, DateTime, ForeignKey,
    Boolean, Text, UniqueConstraint, func
)
from sqlalchemy.orm import relationship
from app.database import Base


class Kullanici(Base):
    __tablename__ = "kullanicilar"
    id = Column(Integer, primary_key=True)
    kullanici_adi = Column(String(50), unique=True, nullable=False)
    ad_soyad = Column(String(100), nullable=False)
    sifre_hash = Column(String(255), nullable=False)
    rol = Column(String(30), default="depo_personeli")
    aktif = Column(Boolean, default=True)
    olusturma = Column(DateTime, server_default=func.now())


class Urun(Base):
    __tablename__ = "urunler"
    id = Column(Integer, primary_key=True)
    ad = Column(String(50), nullable=False)
    aktif = Column(Boolean, default=True)


class Cesit(Base):
    __tablename__ = "cesitler"
    id = Column(Integer, primary_key=True)
    urun_id = Column(Integer, ForeignKey("urunler.id"), nullable=False)
    ad = Column(String(50), nullable=False)
    kod_prefix = Column(String(20))
    aktif = Column(Boolean, default=True)
    urun = relationship("Urun")


class Ebat(Base):
    __tablename__ = "ebatlar"
    id = Column(Integer, primary_key=True)
    urun_id = Column(Integer, ForeignKey("urunler.id"), nullable=False)
    ad = Column(String(50), nullable=False)
    sira_no = Column(Integer, default=0)
    aktif = Column(Boolean, default=True)
    urun = relationship("Urun")


class Depo(Base):
    __tablename__ = "depolar"
    id = Column(Integer, primary_key=True)
    ad = Column(String(50), nullable=False)
    konum = Column(String(200))
    aktif = Column(Boolean, default=True)


class HasatYeri(Base):
    __tablename__ = "hasat_yerleri"
    id = Column(Integer, primary_key=True)
    ad = Column(String(50), nullable=False)
    il = Column(String(50))
    ilce = Column(String(50))
    aktif = Column(Boolean, default=True)


class Tedarikci(Base):
    __tablename__ = "tedarikciler"
    id = Column(Integer, primary_key=True)
    ad = Column(String(100), nullable=False)
    telefon = Column(String(20))
    tip = Column(String(20), default="uretici")
    aktif = Column(Boolean, default=True)


class Parti(Base):
    __tablename__ = "partiler"
    id = Column(Integer, primary_key=True)
    parti_no = Column(String(50), unique=True, nullable=False)
    stok_kodu = Column(String(50))
    cesit_id = Column(Integer, ForeignKey("cesitler.id"), nullable=False)
    hasat_yeri_id = Column(Integer, ForeignKey("hasat_yerleri.id"))
    tedarikci_id = Column(Integer, ForeignKey("tedarikciler.id"))
    uretim_yili = Column(Integer)
    aciklama = Column(Text)
    olusturma = Column(DateTime, server_default=func.now())
    cesit = relationship("Cesit")
    hasat_yeri = relationship("HasatYeri")
    tedarikci = relationship("Tedarikci")


class DepoGiris(Base):
    __tablename__ = "depo_giris"
    id = Column(Integer, primary_key=True)
    tarih = Column(Date, nullable=False)
    depo_id = Column(Integer, ForeignKey("depolar.id"), nullable=False)
    cesit_id = Column(Integer, ForeignKey("cesitler.id"), nullable=False)
    ebat_id = Column(Integer, ForeignKey("ebatlar.id"), nullable=False)
    parti_id = Column(Integer, ForeignKey("partiler.id"), nullable=False)
    hasat_yeri_id = Column(Integer, ForeignKey("hasat_yerleri.id"))
    tedarikci_id = Column(Integer, ForeignKey("tedarikciler.id"))
    arac_plaka = Column(String(20))
    giris_kg = Column(Numeric(12, 2), nullable=False)
    kasa_adet = Column(Integer)
    aciklama = Column(Text)
    kullanici_id = Column(Integer, ForeignKey("kullanicilar.id"))
    olusturma = Column(DateTime, server_default=func.now())
    depo = relationship("Depo")
    cesit = relationship("Cesit")
    ebat = relationship("Ebat")
    parti = relationship("Parti")


class Stok(Base):
    __tablename__ = "stok"
    id = Column(Integer, primary_key=True)
    depo_id = Column(Integer, ForeignKey("depolar.id"), nullable=False)
    cesit_id = Column(Integer, ForeignKey("cesitler.id"), nullable=False)
    ebat_id = Column(Integer, ForeignKey("ebatlar.id"), nullable=False)
    parti_id = Column(Integer, ForeignKey("partiler.id"), nullable=False)
    giris_kg = Column(Numeric(14, 2), default=0)
    cikis_kg = Column(Numeric(14, 2), default=0)
    fire_kg = Column(Numeric(14, 2), default=0)
    kalan_kg = Column(Numeric(14, 2), default=0)
    guncelleme = Column(DateTime, server_default=func.now(), onupdate=func.now())
    depo = relationship("Depo")
    cesit = relationship("Cesit")
    ebat = relationship("Ebat")
    parti = relationship("Parti")
    __table_args__ = (
        UniqueConstraint("depo_id", "cesit_id", "ebat_id", "parti_id", name="uq_stok"),
    )


class StokHareket(Base):
    __tablename__ = "stok_hareketleri"
    id = Column(Integer, primary_key=True)
    tarih = Column(Date, nullable=False)
    kaynak_tablo = Column(String(30))
    kaynak_id = Column(Integer)
    depo_id = Column(Integer, ForeignKey("depolar.id"))
    cesit_id = Column(Integer, ForeignKey("cesitler.id"))
    ebat_id = Column(Integer, ForeignKey("ebatlar.id"))
    parti_id = Column(Integer, ForeignKey("partiler.id"))
    hareket_tipi = Column(String(20))
    miktar_kg = Column(Numeric(14, 2))
    aciklama = Column(Text)
    kullanici_id = Column(Integer, ForeignKey("kullanicilar.id"))
    olusturma = Column(DateTime, server_default=func.now())