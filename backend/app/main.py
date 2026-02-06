from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware

from app.database.session import engine
from app.database.base import Base

# Routers
from app.api.routes.vehicle import router as vehicle_router
from app.api.routes.vehicle_notes import router as vehicle_notes_router
from app.api.routes.trip import router as trip_router
from app.api.routes.fuel import router as fuel_router
from app.api.routes.maintenance import router as maintenance_router
from app.api.routes.customer_routes import router as customer_router
from app.api.routes.driver_routes import router as driver_router
from app.api.routes.spare_part import router as spare_part_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.dashboard_notes import router as dashboard_notes_router
from app.api.routes.vendor import router as vendor_router
from app.api.routes.vendor_payment_routes import router as vendor_payment_router
from app.api.routes.driver_expense import router as driver_expense_router
from app.api.routes.payment import router as payment_router
from app.api.routes.driver_salary_routes import router as driver_salary_router
from app.api.routes.auth import router as auth_router
from app.services.auth_service import get_current_user

# Ensure models are imported for table creation
from app.models import vendor_payment  # noqa: F401
from app.models import driver_salary  # noqa: F401
from app.models import user  # noqa: F401
from app.models import trip_pricing_item  # noqa: F401
from app.models import trip_driver_change  # noqa: F401
from app.models import dashboard_note  # noqa: F401

app = FastAPI(
    title="Tour & Travel Management API",
    version="1.0.0",
)

# ===============================
# CORS CONFIG (React Frontend)
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost",
        "http://localhost:80",
        "https://nathkrupa.lmsoftwaresolutions.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# Create DB Tables
# ===============================
Base.metadata.create_all(bind=engine)

# ===============================
# Create Default Users
# ===============================
from sqlalchemy.orm import Session
from app.models.user import User

def create_default_users():
    db = Session(bind=engine)
    try:
        if not db.query(User).filter(User.username == "Nathkrupa_1").first():
            db.add(User(
                username="Nathkrupa_1",
                password_hash=User.hash_password("Nathkrupa_1"),
                role="admin"
            ))

        if not db.query(User).filter(User.username == "Nathkrupa_2").first():
            db.add(User(
                username="Nathkrupa_2",
                password_hash=User.hash_password("Nathkrupa_2"),
                role="admin"
            ))

        if not db.query(User).filter(User.username == "Nathkrupa_3").first():
            db.add(User(
                username="Nathkrupa_3",
                password_hash=User.hash_password("Nathkrupa_3"),
                role="limited"
            ))

        db.commit()
    finally:
        db.close()

create_default_users()

# ===============================
# Register Routers (NO /api HERE)
# ===============================
# ===============================
# Register Routers (/api PREFIX)
# ===============================
auth_dependency = [Depends(get_current_user)]

app.include_router(auth_router, prefix="/api")

app.include_router(vehicle_router, prefix="/api", dependencies=auth_dependency)
app.include_router(vehicle_notes_router, prefix="/api", dependencies=auth_dependency)
app.include_router(trip_router, prefix="/api", dependencies=auth_dependency)
app.include_router(fuel_router, prefix="/api", dependencies=auth_dependency)
app.include_router(maintenance_router, prefix="/api", dependencies=auth_dependency)
app.include_router(customer_router, prefix="/api", dependencies=auth_dependency)
app.include_router(driver_router, prefix="/api", dependencies=auth_dependency)
app.include_router(spare_part_router, prefix="/api", dependencies=auth_dependency)
app.include_router(payment_router, prefix="/api", dependencies=auth_dependency)
app.include_router(dashboard_router, prefix="/api", dependencies=auth_dependency)
app.include_router(dashboard_notes_router, prefix="/api", dependencies=auth_dependency)
app.include_router(vendor_router, prefix="/api", dependencies=auth_dependency)
app.include_router(vendor_payment_router, prefix="/api", dependencies=auth_dependency)
app.include_router(driver_expense_router, prefix="/api", dependencies=auth_dependency)
app.include_router(driver_salary_router, prefix="/api", dependencies=auth_dependency)

# ===============================
# Health Check
# ===============================
@app.get("/health")
def health():
    return {"status": "ok"}

# ===============================
# Root
# ===============================
@app.get("/")
def root():
    return {
        "message": "Tour & Travel Management API is running",
        "status": "OK",
        "login": "POST /auth/login"
    }
