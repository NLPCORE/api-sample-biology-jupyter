from urllib.parse import urljoin

import requests

from .load_graph import load_graph


class ApiLoader:
    project_name = None
    auth_key = None
    common_params = None

    BASE_URL = 'https://apis.nlpcore.com/1.0.0/'

    request_fncs = {
        'GET': requests.get,
        'POST': requests.post
    }

    def __init__(self, project_name, auth_key):
        self.project_name = project_name
        self.auth_key = auth_key
        self.common_params = {'project_name': project_name, 'compressed': True, 'async': False, 'auth': auth_key}

    @staticmethod
    def show_progress_message():
        print('Searching for results...You may check progress at https://apis.nlpcore.com/graph/alpha/task-progress/')

    @staticmethod
    def check_response_code(response):
        if response.status_code != 200:
            raise ValueError("Request failed with status code: %d" % response.status_code)

    @staticmethod
    def perform_request(request_fnc, show_progress_message=False, *args, **kwargs):
        try:
            fnc = ApiLoader.request_fncs[request_fnc]
        except KeyError:
            raise NotImplemented("Requested function '%s' has not been implemented for api requests" % request_fnc)
        if show_progress_message:
            ApiLoader.show_progress_message()
        response = fnc(*args, **kwargs)
        ApiLoader.check_response_code(response)
        return response

    def load_graph(self, query, filters, page, depth=1, max_distance=-1):
        url = urljoin(self.BASE_URL, "get_graph")
        params = {'words': query, 'filters': filters, 'page': page, 'depth': depth, 'max_distance': max_distance}
        params.update(self.common_params)
        response = ApiLoader.perform_request("GET", show_progress_message=True, url=url, params=params)
        return load_graph(response.json())

    def get_entity_reference(self, document_id, connected_words):
        url = urljoin(self.BASE_URL, "get_entity_reference")
        params = {'document_id': document_id, 'connected_words': connected_words}
        params.update(self.common_params)
        response = ApiLoader.perform_request("GET", url=url, params=params)
        return response.json()
