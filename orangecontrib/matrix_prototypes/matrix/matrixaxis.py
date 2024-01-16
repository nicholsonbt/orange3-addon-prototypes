import numpy as np

from .utils import MatrixBaseMixin




class MatrixAxis(MatrixBaseMixin):
    def __init__(self, name, values, meta):
        MatrixBaseMixin.__init__(self, name, meta)
        self.values = values

    def __repr__(self):
        return str(self.name) + ": " + str(self.values)

    @property
    def values(self):
        return self._values
    
    @values.setter
    def values(self, values):
        values = np.asarray(values)
        MatrixAxis._check_values(values)
        self._values = values

    
    @property
    def size(self):
        return len(self.values)


    @staticmethod
    def _check_values(values):
        # Ensure numpy array.
        assert(type(values) == np.ndarray)

        # Ensure 1D.
        assert(len(values.shape) == 1)

        # Ensure all values are string.
        assert(np.all([isinstance(value, str) for value in values]))