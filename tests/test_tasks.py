TASK_NOT_FOUND = { 'detail': "Task not found" }


# ========================================== GET ========================================== #
def test_get_list_tasks(client) :
    """ """

    response = client.get('/task/lists')

    assert response.status_code == 200
    assert response.json() != []


def test_get_task_by_id_success(client) :
    """ """

    response = client.get('/task/id/1')
    
    assert response.status_code == 200
    assert response.json() != TASK_NOT_FOUND


def test_get_task_by_id_error(client) :
    """ """

    response = client.get('/task/id/99')
    assert response.status_code == 404
    assert response.json() == TASK_NOT_FOUND


# ========================================== POST ========================================== #
def test_add_task_success(client) :
    """ """

    response = client.post('/task/add',
                           params={
                               'title': 'Play games',
                               'completed': False
                            })
    
    assert response.json()['title'] == 'Play games'
    assert response.json()['completed'] == False


def test_add_task_error(client) :
    """ """

    response = client.post('/task/add',
                           params={ 'completed': False })
    
    assert response.status_code == 400


def test_add_empty_task_error(client) :
    """ """

    response = client.post('/task/add',
                           params={})
    
    assert response.status_code == 400


# ========================================== PUT ========================================== #
def test_update_values_success(client) :
    """ """

    response = client.put('/task/update/id/1',
                           params={
                               'title': 'Learn coding',
                               'completed': False,
                            })
    
    
    assert response.status_code == 200
    assert response.json()['title'] == 'Learn coding'
    assert response.json()['completed'] == False


def test_update_task_missing_values_error(client) :
    """ """

    response = client.put('/task/update/id/2',
                           params={})
    
    assert response.status_code == 501


def test_update_task_not_found_error(client) :
    """ """

    response = client.put('/task/update/100',
                           params={ 'completed': False })
    
    assert response.status_code == 404


# ========================================== DELETE ========================================== #
def test_remove_task_success(client) :
    """ """

    response = client.delete('/task/delete/id/1')
        
    assert response.status_code == 200
    assert response.json()['id'] == 1


def test_remove_missing_task_error(client) :
    """ """

    response = client.delete('/task/delete/id/100')
        
    assert response.status_code == 404