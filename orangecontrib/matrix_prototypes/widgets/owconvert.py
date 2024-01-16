from Orange.widgets.widget import OWWidget, Input, Output, Msg
from Orange.widgets import gui
from Orange.data import Table, ContinuousVariable

from orangecontrib.matrix_prototypes.matrix import Matrix

import numpy as np


class OWConvert(OWWidget):
    name = "Convert Matrices"
    priority = 200

    class Inputs:
        matrix = Input("Matrix", Matrix)
        table = Input("Data", Table)
    
    class Outputs:
        matrix = Output("Matrix", Matrix)
        table = Output("Data", Table)

    class Error(OWWidget.Error):
        multi_input = Msg("Only one input allowed.")

    
    def __init__(self):
        super().__init__()

        self.matrix = None
        self.table = None


    @Inputs.matrix
    def set_matrix(self, matrix):
        self.Error.clear()

        self.matrix = matrix
            
        if matrix and self.table:
            self.Error.multi_input()

        else:
            self.commit()


    @Inputs.table
    def set_table(self, table):
        self.Error.clear()

        self.table = table
            
        if table and self.matrix:
            self.Error.multi_input()

        else:
            self.commit()

            
    def commit(self):
        if self.matrix:
            self.Outputs.table.send(self.matrix.as_table())
            self.Outputs.matrix.send(self.matrix)

        else:
            self.Outputs.table.send(self.table)
            self.Outputs.matrix.send(Matrix.from_table(self.table)) ## Not Implemented Yet.
    


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWConvert).run()