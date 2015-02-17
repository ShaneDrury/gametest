import abc


class Entity(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def update(self, parent):
        raise NotImplementedError()

    @abc.abstractmethod
    def handle_event(self, event):
        raise NotImplementedError()

    @abc.abstractmethod
    def transform_polygons(self):
        raise NotImplementedError()
