import numpy as np

from .matrixaxis import MatrixAxis




class MatrixDomain:
    def __init__(self, axes):
        self.axes = axes


    def __repr__(self):
        return "\n".join([str(axis) for axis in self.axes])


    @property
    def axes(self):
        return self._axes
    
    @axes.setter
    def axes(self, axes):
        axes = np.asarray(axes)
        MatrixDomain._check_axes(axes)
        self._axes = axes

    
    @property
    def shape(self):
        return tuple(axis.size for axis in self.axes)
    
    @property
    def length(self):
        return len(self.axes)
    
    @property
    def size(self):
        return np.prod(self.shape)


    @property
    def names(self):
        return [axis.name for axis in self.axes]


    @staticmethod
    def _check_axes(axes):
        if axes is None:
            return

        # Ensure numpy array.
        assert(isinstance(axes, np.ndarray))

        # Ensure 1D.
        assert(len(axes.shape) == 1)

        # Ensure all values are string.
        assert(np.all([isinstance(axis, MatrixAxis) for axis in axes]))

        # Ensure no axis has the same name.
        names = [axis.name for axis in axes]
        assert(len(set(names)) == len(names))
