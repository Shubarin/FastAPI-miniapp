from settings import API_PREFIX


def test_get_index_page_check_status_code_equals_200(test_app):
    """
    Test available urls index page
    :param test_app:
    :return:
    """
    resources = (
        '/', '/get_last_images'
    )
    for resource in resources:
        response = test_app.get(resource)
        assert response.status_code == 200, f'{resource} status:' \
                                            f' {response.status_code} != 200'


def test_get_negative_image_page_check_status_code_equals_200(test_app):
    """
    Test available urls negative image page
    :param test_app:
    :return:
    """
    resource = '/negative_image'
    response = test_app.get(resource)
    assert response.status_code == 200, f'{resource} status:' \
                                        f' {response.status_code} != 200'


def test_api_get_latest_images_check_status_code_equals_200(test_app):
    """
    Test available method get to API /get_latest_images
    :param test_app:
    :return:
    """
    resource = f'{API_PREFIX}/get_last_images'
    response = test_app.get(resource)
    assert response.status_code == 200, f'{resource} status:' \
                                        f' {response.status_code} != 200'


def test_api_get_negative_image_check_status_code_equals_405(test_app):
    """
    Test deprecated method get to API /negative_image
    :param test_app:
    :return:
    """
    resource = f'{API_PREFIX}/negative_image'
    response = test_app.get(resource)
    assert response.status_code == 405, f'{resource} status:' \
                                        f' {response.status_code} != 405'
