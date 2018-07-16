# Third-party Imports
import falcon
import json
from time import time


class CollectorIdResource:
    """
    Represents the data collector REST resource.
    """
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

        if not data:
            raise falcon.HTTPMissingParam('data')

        # Send the message
        # TODO: Make the message persistent
        self.activemq_conn.send(queue, 
                                json.dumps({
                                    'data': data, 
                                    'timestamp': int(time())
                                }).encode())

        # Answer the request
        resp.media = {
            'created': json.dumps(data),
            'status': 'success'
        }
        resp.status = falcon.HTTP_201
