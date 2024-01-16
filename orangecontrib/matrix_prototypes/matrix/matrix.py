import numpy as np
import numbers

from .matrixdomain import MatrixDomain
from .matrixaxis import MatrixAxis
from .utils import MatrixBaseMixin

from Orange.data import Table, Domain, ContinuousVariable, DiscreteVariable




class Matrix(MatrixBaseMixin):
    def __init__(self, name, data, domain, meta):
        MatrixBaseMixin.__init__(self, name, meta)
        self.data = data
        self.domain = domain


    def __repr__(self):
        return str(self.name) + "\n" + str(self.domain) + "\n" + str(self.data)


    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, data):
        data = np.asarray(data)
        Matrix._check_data(data)
        self._data = data

    
    @property
    def shape(self):
        return self.data.shape


    @property
    def domain(self):
        return self._domain
    
    @domain.setter
    def domain(self, domain):
        Matrix._check_domain(domain)
        self._domain = domain



    def as_table(self, attr_axis=0):
        # If attr_axis is the name, get the index.
        if isinstance(attr_axis, str):
            attr_axis = self.domain.names.index(attr_axis)

        # Reshape the data.
        x = np.moveaxis(self.data, attr_axis, -1)
        data = x.reshape(-1, self.domain.shape[attr_axis])

        # Get the attributes.
        attrs = [ContinuousVariable(name=value)
                for value in self.domain.axes[attr_axis].values]

        # Get the meta attributes.
        meta_attrs = [DiscreteVariable(name=axis.name, values=axis.values) 
                      for i, axis in enumerate(self.domain.axes) if i != attr_axis]
        
        # Get the values for each attribute
        meta_values = [np.arange(len(variable.values)) for variable in meta_attrs]

        # Reshape the value permutations to match the data shape.
        meta_data = np.array(np.meshgrid(*meta_values)).T.reshape(-1,len(meta_attrs))

        domain = Domain(attrs, metas=meta_attrs)
        table = Table.from_numpy(domain, data, metas=meta_data)
        table.name = self.name

        return table

    


    @staticmethod
    def _check_data(data):
        # Ensure numpy array.
        assert(isinstance(data, np.ndarray))

        # Ensure all values are numbers.
        assert(np.all([isinstance(value, numbers.Number) for value in data.flatten()]))


    @staticmethod
    def _check_domain(domain):
        # Ensure MatrixDomain.
        assert(isinstance(domain, MatrixDomain))

    
    @staticmethod
    def _check_matrix(matrix):
        assert(matrix.shape == matrix.domain.shape)



    @staticmethod
    def from_table(table):
        order = ["x", "y", "z"]

        data = table.X
        attrs = table.domain.attributes

        meta_attrs = table.domain.metas
        meta_data = table.metas

        ms = [m.name for m in meta_attrs]

        attrs_name = "Attributes"

        if order is None:
            order = ["Attributes"] + ms

        else:
            possible_attrs = set(order) - set(ms)
            remaining = set(ms) - set(order)

            if len(remaining) > 0:
                raise Exception("Meta values not in order were found.")
            
            if len(possible_attrs) == 0:
                order = ["Attributes"] + order

            elif len(possible_attrs) == 1:
                attrs_name = list(possible_attrs)[0]
            
            else:
                raise Exception("Too many unknown values were given.")
        
        axes = []
        shape = []
        pos = []

        k = None

        for i, name in enumerate(order):
            if name == attrs_name:
                values = [attr.name for attr in attrs]
                k = i
            
            else:
                values = [attr.values for attr in meta_attrs if attr.name == name][0]
                pos.append(i)

            shape.append(len(values))
            axes.append(MatrixAxis(name, values, dict()))

        pos.append(k)

        domain = MatrixDomain(axes)

        x = data.reshape(*(np.array(shape)[pos]))

        return Matrix(table.name, np.moveaxis(x, -1, 0), domain, dict())
