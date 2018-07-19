# Third-party Imports
import falcon
import json
from time import time


class CollectorIdResource:
    """
    Represents the data collector REST resource.
    """

    # ActiveMQ Send Headers
    headers = {
        'persistent':'true'
    }

    def on_post(self, req, resp, queue):
        """
        Handles /collector/$queue post requests.
        Queues new data into the given queue located at the ActiveMQ instance.
        """
        # If the queue name is not an alphanumeric return error
        if not str(queue).isalnum():
            raise falcon.HTTPInvalidParam('Invalid queue name.', 'queue')

        # Create the message
        data = req.media.get('data')

        # Check if data is not empty
        if not data:
            raise falcon.HTTPMissingParam('data')

        # Send the message
        self.activemq_conn.send(queue, json.dumps({'data': data}).encode(), self.headers)

        # Answer the request
        resp.media = {
            'created': json.dumps(data),
            'status': 'success'
        }

        # Created a new entry on the queue
        resp.status = falcon.HTTP_201
