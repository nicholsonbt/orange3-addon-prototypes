from Orange.widgets.widget import OWWidget, Output
from Orange.data import Table, ContinuousVariable

from orangecontrib.matrix_prototypes.matrix import Matrix, MatrixDomain, MatrixAxis

import numpy as np
from Orange.widgets import gui
from Orange.widgets.settings import Setting

from AnyQt.QtCore import Qt
from AnyQt.QtWidgets import QComboBox, QHBoxLayout






class OWRandomMatrix(OWWidget):
    name = "Random Matrix"
    priority = 50

    class Outputs:
        table = Output("Data", Table, default=True)
        matrix = Output("Matrix", Matrix)

    
    def __init__(self):
        super().__init__()

        x = MatrixAxis("x", ["X0", "X1", "X2"], dict())
        y = MatrixAxis("y", ["Y0", "Y1"], dict())
        z = MatrixAxis("z", ["Z0", "Z1", "Z2", "Z3"], dict())

        domain = MatrixDomain([x, y, z])

        data = np.array([
            [
                [ 1,  2,  3,  4],
                [ 5,  6,  7,  8],
            ],
            [
                [ 9, 10, 11, 12],
                [13, 14, 15, 16],
            ],
            [
                [17, 18, 19, 20],
                [21, 22, 23, 24],
            ],
        ])


        self.matrix = Matrix("Matrix", data, domain, dict())

        # dbox = gui.widgetBox(self.controlArea, True)
        # self.controls = gui.vBox(dbox)

        # self.attr_box = self.setup_output_settings_box(["x", "y", "z"])

        #layout.addWidget(self.attr_box)
        #self.controlArea.setLayout(layout)



        self.commit()


    def commit(self):
        self.Outputs.table.send(self.matrix.as_table())
        self.Outputs.matrix.send(self.matrix)
    


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWRandomMatrix).run()