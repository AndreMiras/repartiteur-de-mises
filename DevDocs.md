# Developer Documentation #

## GUI Designer ##

### Using ui files with Python programs ###
http://lionel.textmalaysia.com/a-simple-tutorial-on-gui-programming-using-qt-designer-with-pyqt4.html

### Updating Python GUI file ###
Update the gui.py after making gui.ui changes.
pyuic4 gui.ui -o gui.py


## Producing binaries ##

### Summary ###
Single executable (Windows)

py2exe - Probably the most popular out there (PyInstaller is also gaining in popularity)


Single executable (Linux)

Freeze - works the same way like py2exe but targets Linux platform


Single executable (Mac)

py2app - again, works like py2exe but targets Mac OS


### Linux examples ###
```
$ python2 pyinstaller.py run.py
```

```
$ bb-freeze run.py
```
If you get a "ImportError: No module named sip" error, check this conversation:

http://groups.google.com/group/bbfreeze-users/browse_thread/thread/e9909bdb8663d82e/dc6833df3822a5b8

## Running tests ##
You can run doctests to verify the module works as expected.
```
$ python distributor.py
```
The test succeed if there's no output.