import numpy as np




class MatrixBaseMixin:
    def __init__(self, name, meta):
        self.name = name
        self.meta = meta
    

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        MatrixBaseMixin._check_name(name)
        self._name = name


    @property
    def meta(self):
        return self._meta
    
    @meta.setter
    def meta(self, meta):
        MatrixBaseMixin._check_meta(meta)
        self._meta = meta


    @staticmethod
    def _check_name(name):
        # Ensure name is string.
        assert(type(name) == str)


    @staticmethod
    def _check_meta(meta):
        # Ensure dictionary.
        assert(type(meta) == dict)