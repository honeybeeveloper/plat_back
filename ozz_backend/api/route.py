class Route(object):
    def __init__(self, path, endpoint, methods=['GET'], response_model=None):
        self.path = path
        self.endpoint = endpoint
        self.methods = methods
        self.response_model = response_model
