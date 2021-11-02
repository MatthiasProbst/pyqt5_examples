# Workflow for PyQt5 projects

Use the qt5 designer (https://doc.qt.io/qt-5/qtdesigner-manual.html) to build your gui.

### Procedure:

* To build and manipulate the gui frontend use the qt5 designer and work on the `ui`-file.
* Then convert the `.ui`-file into the `.py` file by running ```pyuic5 image_manipulator.ui -o image_manipulator.py```.
  Don't touch that file!
* Your own code goes into a separate python file (e.g. `main.py`), that imports the `UI Window class`. Here, you define
  what happens when you press a button for instance.