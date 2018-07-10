# Third-Party Imports
from stompest.sync import Stomp

class ActiveMQSession(object):
    """
    Create a scoped session for every request and
    closes it when the request ends.
    """
    def __init__(self, stompconf):
        self.client = Stomp(stompconf)

    def process_resource(self, req, resp, resource, params):
        self.client.connect()
        resource.activemq_conn = self.client

    def process_response(self, req, resp, resource, req_succeeded):
        if hasattr(resource, 'activemq_conn'):
            self.client.disconnect()
            self.client.close()