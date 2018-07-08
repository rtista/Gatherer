class ActiveMQSession(object):
    """
    Create a scoped session for every request and
    closes it when the request ends.
    """
    def __init__(self, Session):
        self.Session = Session

    def process_resource(self, req, resp, resource, params):
        resource.activemq = self.Session()

    def process_response(self, req, resp, resource, req_succeeded):
        if hasattr(resource, 'activemq'):
            self.Session.remove()