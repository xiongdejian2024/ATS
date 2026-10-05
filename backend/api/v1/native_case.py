"""项目原生配置接口，沿用项目权限和事务日志。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from api.deps import get_current_user
from api.v1.case_governance import transact, result
from models.native_case import ApiDefinition, ApiTestEnvironment
from schemas.native_case import DefinitionInput, EnvironmentInput, ConfigInput
from services import native_case as service
router = APIRouter(prefix='/projects/{project_id}/native-cases', tags=['API与场景配置'])

@router.get('/catalog')
def catalog(project_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return result(service.catalog(db, user, project_id))

@router.post('/definitions')
def definition_create(project_id: str, body: DefinitionInput, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return result(transact(db, lambda: service.save_entity(db, user, project_id, ApiDefinition, body)))

@router.put('/definitions/{identity}')
def definition_update(project_id: str, identity: str, body: DefinitionInput, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return result(transact(db, lambda: service.save_entity(db, user, project_id, ApiDefinition, body, identity)))

@router.post('/environments')
def environment_create(project_id: str, body: EnvironmentInput, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return result(transact(db, lambda: service.save_entity(db, user, project_id, ApiTestEnvironment, body)))

@router.put('/environments/{identity}')
def environment_update(project_id: str, identity: str, body: EnvironmentInput, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return result(transact(db, lambda: service.save_entity(db, user, project_id, ApiTestEnvironment, body, identity)))

@router.get('/cases/{case_id}')
def config(project_id: str, case_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return result(service.config_data(db, user, project_id, case_id))

@router.put('/cases/{case_id}')
def config_save(project_id: str, case_id: str, body: ConfigInput, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return result(transact(db, lambda: service.save_config(db, user, project_id, case_id, body)))
