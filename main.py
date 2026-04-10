from fastapi import FastAPI
import models
from database import engine
from routers import leave

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ IMPORTANT LINE
app.include_router(leave.router, prefix="/leave")