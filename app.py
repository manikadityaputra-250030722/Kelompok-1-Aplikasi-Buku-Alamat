# app.py
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import User, Contact
from schemas import (
    UserCreate, UserOut, Token,
    ContactCreate, ContactOut, ContactUpdate,
)
from auth import get_password_hash, verify_password, create_access_token, decode_token

# Buat tabel di database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Buku Alamat API")

# ========= STATIC / FRONTEND =========
# Folder "static" harus sejajar dengan app.py
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    # Saat buka http://127.0.0.1:8000/ akan diarahkan ke static/index.html
    return RedirectResponse(url="/static/index.html")


# ========= AUTH SETUP =========
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau kadaluarsa",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid",
        )
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Pengguna tidak ditemukan",
        )
    return user


# ========= AUTH ENDPOINTS =========
@app.post("/register", response_model=UserOut, status_code=201)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Cek username & email unik
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="Username sudah digunakan")
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email sudah digunakan")

    hashed = get_password_hash(user_in.password)
    user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Username atau password salah")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# ========= CONTACTS CRUD =========
@app.post("/contacts", response_model=ContactOut, status_code=201)
def create_contact(
    contact_in: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = Contact(
        user_id=current_user.id,
        **contact_in.dict(),
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@app.get("/contacts", response_model=List[ContactOut])
def list_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    search: Optional[str] = None,
    category: Optional[str] = None,
    sort_by: Optional[str] = "name",
    order: Optional[str] = "asc",
):
    query = db.query(Contact).filter(Contact.user_id == current_user.id)

    # Pencarian
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            (Contact.name.ilike(pattern))
            | (Contact.email.ilike(pattern))
            | (Contact.address.ilike(pattern))
        )

    # Filter kategori
    if category:
        query = query.filter(Contact.category == category)

    # Sorting
    if sort_by == "name":
        query = query.order_by(
            Contact.name.asc() if order == "asc" else Contact.name.desc()
        )
    elif sort_by == "category":
        query = query.order_by(
            Contact.category.asc() if order == "asc" else Contact.category.desc()
        )

    return query.all()


@app.get("/contacts/{contact_id}", response_model=ContactOut)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == current_user.id,
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Kontak tidak ditemukan")
    return contact


@app.put("/contacts/{contact_id}", response_model=ContactOut)
def update_contact(
    contact_id: int,
    contact_in: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == current_user.id,
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Kontak tidak ditemukan")

    update_data = contact_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contact, field, value)

    db.commit()
    db.refresh(contact)
    return contact


@app.delete("/contacts/{contact_id}", status_code=204)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == current_user.id,
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Kontak tidak ditemukan")

    db.delete(contact)
    db.commit()
    return
