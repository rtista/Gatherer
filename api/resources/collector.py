# Third-party Imports
import falcon


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

        # TODO: Create the message

        # TODO: Connect to ActiveMQ queue

        # TODO: Send the message

        # Answer the request
        resp.media = {}
        resp.status = falcon.HTTP_201
