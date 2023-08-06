""" sets up the base class for all backend services """
from rancon.common import CommonBase


class BackendBase(CommonBase):
    """ base class for all implementations of a backend """
    required_opts = ()
    additional_opts = ()

    def register(self, service):
        """
        Registers a service in the backend.
        :param service: A rancon.service.Service instance
        :return: None
        """
        pass

    def cleanup(self, keep_services):
        """
        Performs 'garbage collection' of no-longer-present services. (If a
        service was registered in a previous run, and is no longer present, it
        might have to be removed manually).
        :param keep_services: A list of services to keep. Each service in the
        list is a return value from register(), which can be pretty much
        anything.
        :return: An integer how many services have been removed.
        """
        pass
