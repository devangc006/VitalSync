from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models import HealthRecord, User
from app.schemas.health import HealthCreateRequest, HealthHistoryResponse, HealthRead
from app.utils.health import calculate_bmi

router = APIRouter(prefix="/health", tags=["Health"])


@router.post("")
def create_health_record(
    payload: HealthCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    bmi = calculate_bmi(payload.weight_kg, payload.height_cm)
    record = HealthRecord(
        user_id=current_user.id,
        weight_kg=payload.weight_kg,
        height_cm=payload.height_cm,
        bmi=bmi,
        water_intake_liters=payload.water_intake_liters,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return {
        'message': 'Health record saved',
        'record': HealthRead(
            id=record.id,
            weight_kg=record.weight_kg,
            height_cm=record.height_cm,
            bmi=record.bmi,
            water_intake_liters=record.water_intake_liters,
            recorded_at=record.recorded_at,
        ),
    }


@router.get("/history", response_model=HealthHistoryResponse)
def get_health_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> HealthHistoryResponse:
    records = (
        db.query(HealthRecord)
        .filter(HealthRecord.user_id == current_user.id)
        .order_by(HealthRecord.recorded_at.desc())
        .all()
    )
    return HealthHistoryResponse(
        records=[
            HealthRead(
                id=record.id,
                weight_kg=record.weight_kg,
                height_cm=record.height_cm,
                bmi=record.bmi,
                water_intake_liters=record.water_intake_liters,
                recorded_at=record.recorded_at,
            )
            for record in records
        ],
    )
