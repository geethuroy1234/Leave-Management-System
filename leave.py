from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter()

@router.post("/")
def apply_leave(leave: schemas.LeaveCreate, db: Session = Depends(get_db)):
    emp = db.query(models.Employee).filter(models.Employee.id == leave.employee_id).first()
    if not emp:
        raise HTTPException(status_code=400, detail="Employee not found")

    new_leave = models.LeaveRequest(**leave.dict(), status="Pending")
    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)

    return new_leave


@router.get("/")
def get_leaves(db: Session = Depends(get_db)):
    return db.query(models.LeaveRequest).all()


@router.put("/approve/{leave_id}")
def approve_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    leave.status = "Approved"
    db.commit()
    db.refresh(leave)

    return {"message": "Leave Approved", "leave": leave}


@router.put("/reject/{leave_id}")
def reject_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    leave.status = "Rejected"
    db.commit()
    db.refresh(leave)

    return {"message": "Leave Rejected", "leave": leave}