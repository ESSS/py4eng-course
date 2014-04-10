import guidata
from linconvection1d_gui import MainWindow


if __name__ == "__main__":
    app = guidata.qapplication()
    inputs = MainWindow()
    inputs.show()
    app.exec_()
