from sqlalchemy.orm import Session
from backend.models.tasks import Task
from tests import helpers
from tests.base import login_as, test_admin


def test_tasks_crud(db: Session):
    client = login_as(test_admin)

    course = helpers.create_course(db)
    topic = helpers.create_topic(db, course_id=course.id)

    response = client.post(f'/api/courses/{course.id}/topics/{topic.id}/tasks', json={
        'name': 'task_1',
        'description': 'task_1',
        'task_type': 'text',
    })
    data = response.json()
    assert response.status_code == 200, data
    task_1_id = data['id']

    response = client.post(f'/api/courses/{course.id}/topics/{topic.id}/tasks', json={
        'name': 'task_2',
        'description': 'task_2',
        'prev_task_id': task_1_id,
        'task_type': 'text',
    })
    data = response.json()
    assert response.status_code == 200, data
    task_2_id = data['id']

    response = client.post(f'/api/courses/{course.id}/topics/{topic.id}/tasks', json={
        'name': 'task_3',
        'description': 'task_3',
        'prev_task_id': None,
        'task_type': 'text',
    })
    data = response.json()
    assert response.status_code == 200, data
    task_3_id = data['id']

    # create task with invalid prev_task_id
    response = client.post(f'/api/courses/{course.id}/topics/{topic.id}/tasks', json={
        'name': 'task_3',
        'description': 'task_3',
        'prev_task_id': -1,
        'task_type': 'text',
    })
    assert response.status_code == 404

    # get one task
    response = client.get(f'/api/courses/{course.id}/topics/{topic.id}/tasks/{task_1_id}')
    data = response.json()
    assert response.status_code == 200, data
    assert data == {
        'id': task_1_id,
        'name': 'task_1',
        'description': 'task_1',
        'task_type': 'text',
        'prev_task': {
            'id': task_3_id,
            'name': 'task_3',
        },
        'next_task': {
            'id': task_2_id,
            'name': 'task_2',
        },
    }

    # check that now first is task_3
    response = client.get(f'/api/courses/{course.id}/topics/{topic.id}/tasks')
    data = response.json()
    assert response.status_code == 200
    assert data['total'] == 3
    assert [item['id'] for item in data['items']] == [
        task_3_id,
        task_1_id,
        task_2_id,
    ]

    # update task_3, make it last
    response = client.patch(f'/api/courses/{course.id}/topics/{topic.id}/tasks/{task_3_id}', json={
        'prev_task_id': task_2_id,
    })
    data = response.json()
    assert response.status_code == 200, data
    response = client.get(f'/api/courses/{course.id}/topics/{topic.id}/tasks')
    data = response.json()
    assert response.status_code == 200
    assert data['total'] == 3
    assert [item['id'] for item in data['items']] == [
        task_1_id,
        task_2_id,
        task_3_id,
    ]

    # delete at the middle
    response = client.delete(f'/api/courses/{course.id}/topics/{topic.id}/tasks/{task_2_id}')
    assert response.status_code == 204
    response = client.get(f'/api/courses/{course.id}/topics/{topic.id}/tasks')
    data = response.json()
    assert response.status_code == 200
    assert data['total'] == 2
    assert [item['id'] for item in data['items']] == [
        task_1_id,
        task_3_id,
    ]

    # delete first
    response = client.delete(f'/api/courses/{course.id}/topics/{topic.id}/tasks/{task_1_id}')
    assert response.status_code == 204
    response = client.get(f'/api/courses/{course.id}/topics/{topic.id}/tasks')
    data = response.json()
    assert response.status_code == 200
    assert data['total'] == 1
    assert [item['id'] for item in data['items']] == [
        task_3_id,
    ]

    # delete last
    response = client.delete(f'/api/courses/{course.id}/topics/{topic.id}/tasks/{task_3_id}')
    assert response.status_code == 204
    response = client.get(f'/api/courses/{course.id}/topics/{topic.id}/tasks')
    data = response.json()
    assert response.status_code == 200
    assert data['total'] == 0

    # delete parent topic
    response = client.delete(f'/api/courses/{course.id}/topics/{topic.id}')
    assert response.status_code == 204
    results = db.query(Task).filter(Task.topic_id == topic.id).all()
    assert len(results) == 0
