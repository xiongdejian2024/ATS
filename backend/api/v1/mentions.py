from typing import Literal
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from api.deps import get_current_user
from database import get_db
from schemas.common import APIResponse
from services.mentions import members

router = APIRouter()


@router.get('/projects/{project_id}/mention-members')
def mention_members(project_id: str, context: Literal['case', 'plan'] = 'case',
                    search: str = Query('', max_length=100), page: int = Query(1, ge=1),
                    db: Session = Depends(get_db), user=Depends(get_current_user)):
    return APIResponse(status='success', message='获取成功', data=members(db, user, project_id, context, search, page))
