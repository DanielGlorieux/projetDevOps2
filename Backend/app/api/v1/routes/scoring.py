from fastapi import APIRouter, Depends, HTTPException
from app.schemas.scoring import ScoreResult
from app.services.scoring_engine import get_user_score
from app.core.security import get_api_key

router = APIRouter()

@router.get("/score/{user_id}", response_model=ScoreResult, dependencies=[Depends(get_api_key)])
@router.get("/predict/{user_id}", response_model=ScoreResult, dependencies=[Depends(get_api_key)])
async def get_score(user_id: str):
    score_data = get_user_score(user_id)
    if score_data is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable.")

    if isinstance(score_data, int):
        score_data = {
            'score': score_data,
            'profile': 'N/A',
            'features': {},
        }

    features = score_data.get('features', {})
    
    # Calculate a valid capacity based on score and feature extracted income for backward compatibility just in case
    cap_emp = features.get('capacite_emprunt', 0.0)
    rev = features.get('revenu_moyen_mensuel', 0.0)
    score_val = score_data['score']
    
    if cap_emp == 0.0 and rev > 0:
        cap_emp = rev * 0.33 * 12 * (score_val/850.0)

    return ScoreResult(
        user_id=user_id,
        score=score_val,
        risk_level=_determine_risk(score_val),
        profile=score_data.get('profile', 'N/A'),
        revenu_moyen_mensuel=rev,
        regularite_revenus=features.get('regularite_revenus', 0.0),
        ratio_epargne=features.get('ratio_epargne', 0.0),
        freq_transactions_mois=features.get('freq_transactions_mois', 0.0),
        capacite_emprunt=cap_emp
    )

def _determine_risk(score: int) -> str:
    if score >= 750:
        return "Faible"
    if score >= 650:
        return "Moyen"
    return "Élevé"
