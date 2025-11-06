"""
Privacy policy evaluation endpoint (shell version with mock responses)
"""

from fastapi import APIRouter, HTTPException
from app.schemas.evaluator import EvaluateRequest, EvaluateResponse
from app.services.evaluator_service import EvaluatorService

router = APIRouter(prefix="/api/v1", tags=["evaluation"])
service = EvaluatorService()

@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate_privacy_policy(request: EvaluateRequest):
    try:
        return service.evaluate_policy(request.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")

