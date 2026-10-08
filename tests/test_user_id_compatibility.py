from uuid import uuid4

import httpx
import pytest
from database import SessionLocal
from models import User
from api.deps import get_current_active_user
from schemas.user import UserUpdate
from services.user_service import get_user, update_user, delete_user


@pytest.mark.asyncio
async def test_uuid_user_lookup_update_delete_supported_by_text_primary_key():
    identifier = uuid4()
    with SessionLocal() as db:
        db.add(User(id=str(identifier), username="synthetic-user", email="synthetic@example.com", password_hash="unused"))
        db.commit()
        assert (await get_user(db, identifier)).id == str(identifier)
        assert (await update_user(db, identifier, UserUpdate(full_name="Updated"))).full_name == "Updated"
        assert await delete_user(db, identifier)
        assert await get_user(db, identifier) is None


@pytest.mark.asyncio
async def test_user_http_uuid_detail_update_delete():
    from main import app
    identifier, actor_id = uuid4(), uuid4()
    with SessionLocal() as db:
        actor = User(id=str(actor_id), username="synthetic-admin", email="admin@example.com", password_hash="unused")
        db.add_all([actor, User(id=str(identifier), username="synthetic-user", email="user@example.com", password_hash="unused")])
        db.commit()
        previous = dict(app.dependency_overrides)
        app.dependency_overrides[get_current_active_user] = lambda: actor
        try:
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
                path = "/api/v1/users/" + str(identifier)
                assert (await client.get(path)).json()["data"]["id"] == str(identifier)
                response = await client.put(path, json={"full_name": "更新"})
                assert response.status_code == 200, response.text
                assert response.json()["data"]["full_name"] == "更新"
                assert (await client.delete(path)).status_code == 200
        finally:
            app.dependency_overrides.clear(); app.dependency_overrides.update(previous)
