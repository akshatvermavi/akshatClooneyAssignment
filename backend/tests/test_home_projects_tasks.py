from datetime import date

import pytest

from app import crud, models, schemas
from app.database import Base


def seed_sample_data(db):
    ws = models.Workspace(name="Demo Workspace")
    db.add(ws)
    db.flush()

    proj = models.Project(workspace_id=ws.id, name="My Project", color="#3a258e", icon="list")
    db.add(proj)
    db.flush()

    inbox = models.Section(project_id=proj.id, name="Inbox", order_index=0)
    db.add(inbox)
    db.flush()

    task1 = models.Task(
        project_id=proj.id,
        section_id=inbox.id,
        name="Task 1",
        status="today",
        assignee="me",
        priority="high",
        due_date=date.today(),
    )
    task2 = models.Task(
        project_id=proj.id,
        section_id=inbox.id,
        name="Task 2",
        status="inbox",
        assignee="someone-else",
    )
    db.add_all([task1, task2])
    db.commit()
    db.refresh(ws)
    db.refresh(proj)
    db.refresh(inbox)
    db.refresh(task1)
    db.refresh(task2)
    return ws, proj, inbox, task1, task2


def test_home_summary_my_tasks_and_recent_projects(client, db_session):
    seed_sample_data(db_session)

    resp = client.get("/api/home")
    assert resp.status_code == 200
    data = resp.json()

    assert any(p["name"] == "My Project" for p in data["recent_projects"])
    assert any(t["assignee"] == "me" for t in client.get("/api/projects/1/tasks").json())
    assert any(t["project_name"] == "My Project" for t in data["my_tasks"])


@pytest.mark.parametrize(
    "status_param, expected_code",
    [
        (None, 200),
        ("today", 200),
        ("", 200),
        ("*special*&^", 200),
        ("x" * 65, 422),  # too long
    ],
)
def test_project_tasks_status_variants(client, db_session, status_param, expected_code):
    _, proj, _, _, _ = seed_sample_data(db_session)

    params = {}
    if status_param is not None:
        params["status"] = status_param

    resp = client.get(f"/api/projects/{proj.id}/tasks", params=params)
    assert resp.status_code == expected_code


@pytest.mark.parametrize(
    "assignee_param",
    [None, "", "me", "non-existent", "*special*&^"],
)
def test_project_tasks_assignee_variants(client, db_session, assignee_param):
    _, proj, _, _, _ = seed_sample_data(db_session)

    params = {}
    if assignee_param is not None:
        params["assignee"] = assignee_param

    resp = client.get(f"/api/projects/{proj.id}/tasks", params=params)
    assert resp.status_code == 200


def test_get_and_update_task_edge_cases(client, db_session):
    _, proj, _, task1, _ = seed_sample_data(db_session)

    # Get existing
    resp = client.get(f"/api/tasks/{task1.id}")
    assert resp.status_code == 200

    # Non-existent
    resp404 = client.get("/api/tasks/9999")
    assert resp404.status_code == 404

    # Update with partial body and special characters
    update_body = {
        "name": "Updated ✨",
        "description": "".join(["x" for _ in range(256)]),
        "status": "completed",
        "assignee": None,
    }
    resp_upd = client.patch(f"/api/tasks/{task1.id}", json=update_body)
    assert resp_upd.status_code == 200
    body = resp_upd.json()
    assert body["name"].startswith("Updated")
    assert body["status"] == "completed"


def test_create_project_invalid_workspace(client, db_session):
    body = {"name": "No Workspace Project", "workspace_id": 9999}
    resp = client.post("/api/projects", json=body)
    assert resp.status_code == 400


def test_create_and_get_project(client, db_session):
    # prepare workspace
    ws = models.Workspace(name="Workspace X")
    db_session.add(ws)
    db_session.commit()
    db_session.refresh(ws)

    body = {"name": "Project X", "workspace_id": ws.id, "color": "#3a258e"}
    resp = client.post("/api/projects", json=body)
    assert resp.status_code == 201
    project = resp.json()
    assert project["name"] == "Project X"
    assert project["color"] == "#3a258e"

    # get
    get_resp = client.get(f"/api/projects/{project['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Project X"


def test_project_sections_endpoint(client, db_session):
    ws, proj, inbox, _, _ = seed_sample_data(db_session)

    resp = client.get(f"/api/projects/{proj.id}/sections")
    assert resp.status_code == 200
    sections = resp.json()
    assert any(s["name"] == "Inbox" for s in sections)

    resp404 = client.get("/api/projects/9999/sections")
    assert resp404.status_code == 404
