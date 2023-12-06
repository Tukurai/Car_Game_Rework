class EventHandler:
    '''Event handler class for the observer pattern'''
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(Observer(observer))

    def remove_observer(self, observer):
        self._observers.remove(Observer(observer))

    def notify(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(*args, **kwargs)

class Observer:
    '''Observer class for the observer pattern'''
    def __init__(self, func):
        self.func = func

    def update(self, *args, **kwargs):
        self.func(*args, **kwargs)