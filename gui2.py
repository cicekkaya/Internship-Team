import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QTextEdit, QVBoxLayout, QWidget, QTabWidget, QLabel, QPushButton
import os
import mayavi2,rasterioex
os.environ['ETS_TOOLKIT'] = 'qt4'
from pyface.qt import QtGui
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from mayavi2 import MyMayAvi

class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())

    @on_trait_change('scene.activated')
    def update_plot(self):
        # This function is called when the view is opened. We don't
        # populate the scene when the view is not yet open, as some
        # VTK features require a GLContext.

        # We can do normal mlab calls on the embedded scene.
        mayavi = (mayavi2.MyMayAvi())
        return mayavi()

    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=300, show_label=False),
                resizable=True)

class MayaviQWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.visualization = Visualization()

        # The edit_traits call will generate the widget to embed.
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    """def contextMenuEvent(self, event):
        # Handle the right-click event
        if event.reason() == event.Mouse:
            x = event.x()
            y = event.y()
            pos = event.pos()
            pos2 = QWidget.mapFromGlobal(self,pos)

            print(pos2.x())
            print(pos2.y())
            print(type(x))
            #MyMayAvi.NewElevation(self,event, x, y)"""

    def init_ui(self):
        self.setWindowTitle("GUI")
        self.setGeometry(100, 100, 800, 600)
        self.button = QPushButton("Set Elevation")

        # Menü çubuğu
        menubar = self.menuBar()
        file_menu1 = menubar.addMenu("Scene")
        file_menu2 = menubar.addMenu("Project")
        file_menu3 = menubar.addMenu("Debug")
        file_menu4 = menubar.addMenu("Editor")
        file_menu5 = menubar.addMenu("Help")
        file_menu1.addAction("Option1")
        file_menu1.addAction("Option2")
        file_menu2.addAction("Option1")
        file_menu2.addAction("Option2")
        file_menu3.addAction("Option1")
        file_menu3.addAction("Option2")
        file_menu4.addAction("Option1")
        file_menu4.addAction("Option2")
        file_menu5.addAction("Option1")
        file_menu5.addAction("Option2")

        # Panel1
        panel1 = QDockWidget("Panel1", self)
        panel1.setStyleSheet("background-color: #363737; color: #FFFFFF; border: 0px solid #363737;")
        panel1.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        panel1_widget = QWidget()
        panel1_layout = QVBoxLayout(panel1_widget)
        panel1_layout.addWidget(QTextEdit("Panel1 content"))
        panel1.setWidget(panel1_widget)
        self.addDockWidget(1, panel1)

        # Panel2
        panel2 = QDockWidget("Panel2", self)
        panel2.setStyleSheet("background-color: #363737; color: #FFFFFF; border: 0px solid #363737;")
        panel2.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        panel2_widget = QWidget()
        panel2_layout = QVBoxLayout(panel2_widget)
        panel2_layout.addWidget(QLabel(rasterioex.write_meta_data()))
        panel2.setWidget(panel2_widget)
        self.addDockWidget(1, panel2)

        # Panel3
        panel3 = QDockWidget("Panel3", self)
        panel3.setStyleSheet("background-color: #363737; color: #FFFFFF; border: 0px solid #363737;")
        panel3.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        panel3_widget = QWidget()
        panel3_layout = QVBoxLayout(panel3_widget)
        panel3_layout.addWidget(QTextEdit("Panel3 content"))

        panel3.setWidget(panel3_widget)
        self.addDockWidget(2, panel3)

        # Panel4
        panel4 = QDockWidget("Panel4", self)
        panel4.setStyleSheet("background-color: #363737; color: #FFFFFF; border: 0px solid #363737")
        panel4.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        panel4_widget = QWidget()
        panel4_layout = QVBoxLayout(panel4_widget)
        panel4_layout.addWidget(self.button)

        panel4.setWidget(panel4_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, panel4)

        # Merkezi Widget (Ekran alanı)
        central_widget = QWidget(self)
        central_widget.setStyleSheet("background-color: #363737; color: #FFFFFF;")
        central_layout = QVBoxLayout(central_widget)

        # Merkezi Widget içinde sekmeler oluştur
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("color: #363737;")

        # Replace the QTextEdit with the MayaviQWidget
        self.mayavi_widget = MayaviQWidget()
        tab_widget.addTab(self.mayavi_widget, "Scene")  # Add the Mayavi widget to the tab

        tab_widget.addTab(QTextEdit("Tab 2 content"), "Tab 2")
        central_layout.addWidget(tab_widget)
        central_widget.setLayout(central_layout)

        # Set central widget for the main window
        self.setCentralWidget(central_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    # Now, you can update the Mayavi visualization by accessing the `visualization` attribute in the `MayaviQWidget`.
    main_window.mayavi_widget.visualization.update_plot()

    sys.exit(app.exec_())
