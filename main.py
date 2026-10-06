from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app import models
from app.auth import dogrula_sifre, token_olustur
from app.routers import depo_giris_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Depo ERP")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(depo_giris_router.router)


@app.get("/", response_class=HTMLResponse)
def login_sayfa(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login_post(request: Request,
               kullanici_adi: str = Form(...),
               sifre: str = Form(...),
               db: Session = Depends(get_db)):
    k = db.query(models.Kullanici).filter(
        models.Kullanici.kullanici_adi == kullanici_adi
    ).first()
    if not k or not dogrula_sifre(sifre, k.sifre_hash):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "hata": "Kullanici adi veya sifre hatali"}
        )
    token = token_olustur(k.kullanici_adi, k.rol)
    resp = RedirectResponse("/dashboard", status_code=302)
    resp.set_cookie("token", token, httponly=True, max_age=28800)
    return resp


@app.get("/cikis")
def cikis():
    resp = RedirectResponse("/", status_code=302)
    resp.delete_cookie("token")
    return resp


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    stoklar = db.query(models.Stok).all()
    toplam_kg = sum(float(s.kalan_kg) for s in stoklar)
    giris_sayisi = db.query(models.DepoGiris).count()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "toplam_kg": round(toplam_kg, 2),
        "stok_kayit": len(stoklar),
        "giris_sayisi": giris_sayisi,
    })


@app.get("/depo-giris", response_class=HTMLResponse)
def depo_giris_sayfa(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("depo_giris.html", {
        "request": request,
        "cesitler": db.query(models.Cesit).filter_by(aktif=True).all(),
        "ebatlar": db.query(models.Ebat).filter_by(aktif=True).all(),
        "depolar": db.query(models.Depo).filter_by(aktif=True).all(),
        "partiler": db.query(models.Parti).all(),
        "hasat_yerleri": db.query(models.HasatYeri).all(),
        "tedarikciler": db.query(models.Tedarikci).all(),
    })


@app.get("/stok", response_class=HTMLResponse)
def stok_sayfa(request: Request, db: Session = Depends(get_db)):
    stoklar = db.query(models.Stok).all()
    return templates.TemplateResponse("stok.html", {
        "request": request, "stoklar": stoklar
    })