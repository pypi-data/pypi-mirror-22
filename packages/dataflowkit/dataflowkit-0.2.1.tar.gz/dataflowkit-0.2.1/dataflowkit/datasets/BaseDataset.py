class BaseDataset(object):
    is_checkpoint = False

    def __init__(self):
    	self._data = None
    
    def save(self, data):
        self._data = data
    
    def load(self):
        return self._data
        