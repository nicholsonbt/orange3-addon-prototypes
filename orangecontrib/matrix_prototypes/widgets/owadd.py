from Orange.widgets.widget import OWWidget, MultiInput, Output, Msg
from Orange.widgets import gui
from Orange.data import Table, ContinuousVariable

import numpy as np


class OWAdd(OWWidget):
    name = "Add Matrices"
    priority = 100

    class Inputs:
        matrices = MultiInput("Matrices", Table, default=True)
    
    class Outputs:
        matrix = Output("Matrix", Table, default=True)

    class Error(OWWidget.Error):
        different_shapes = Msg("The input matrices must all have the same shapes.")
        non_numeric = Msg("All features of all matrices must be continuous.")

    
    def __init__(self):
        super().__init__()

        self.matrices = []
        self.shape = None


    def _checkMatrices(self):
        self.Error.clear()

        for matrix in self.matrices:
            if np.any([type(attr) != ContinuousVariable for attr in matrix.domain.attributes]):
                self.Error.non_numeric()

        if len(self.matrices) > 1:
            shape = self.matrices[0].X.shape

            for i in range(1, len(self.matrices)):
                if shape != self.matrices[i].X.shape:
                    self.Error.different_shapes()

    
    @Inputs.matrices
    def set_matrices(self, index, matrix):
        self.matrices[index] = matrix
        self.commit()

    @Inputs.matrices.insert
    def insert_matrix(self, index, matrix):
        self.matrices.insert(index, matrix)
        self.commit()

    @Inputs.matrices.remove
    def remove_matrix(self, index):
        self.matrices.pop(index)
        self.commit()


    @property
    def sum(self):
        table = None

        if self.matrices:
            table = self.matrices[0].copy()

            for i in range(1, len(self.matrices)):
                table.X += self.matrices[i].X

        return table
            
    def commit(self):
        self._checkMatrices()
        self.Outputs.matrix.send(self.sum)
    


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWAdd).run()