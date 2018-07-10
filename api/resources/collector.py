# Third-party Imports
import falcon
import json


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

        # TODO: Send the message
        self.activemq_conn.send(queue, json.dumps(data).encode())

        # Answer the request
        resp.media = {
            'created': json.dumps(data),
            'status': 'success'
        }
        resp.status = falcon.HTTP_201
