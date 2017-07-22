# Development

## Add a basic starting point for the initial version

The application's source code is:

```python
#!/usr/bin/env python3
import wx

class SketchFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, 
                          parent, 
                          -1, 
                          "Sketch Frame", 
                          size = (800, 600))

class App(wx.App):
    def OnInit(self):
        self.frame = SketchFrame(None)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()
```

![sketchy-img](screenshots/sketchy-01.png)

Also, type `$ git checkout 1b` to perform a checkout of this version.

## Add the `SketchWindow` class and modify the `SketchFrame` class

The `SketchWindow` class is added with a minimal initialization 
definition and the `sketch` variable in the `SketchFrame` class is 
created.

The application's source code is:

```python
#!/usr/bin/env python3
import wx

class SketchWindow(wx.Window):
    def __init__(self, parent, id):
        wx.Window.__init__(self, parent, id)
        self.SetBackgroundColour("White")
        self.color = "Black"
        self.thickness = 1
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
        self.lines = []
        self.curLine = []
        self.pos = (0, 0)

class SketchFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, 
                          parent, 
                          -1, 
                          "Sketch Frame", 
                          size = (800, 600))
        self.sketch = SketchWindow(self, -1)

class App(wx.App):
    def OnInit(self):
        self.frame = SketchFrame(None)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()
```

![sketchy-img](screenshots/sketchy-02.png)

Also, type `$ git checkout 1c` to perform a checkout of this version.

## Add the `InitBuffer()` and `DrawLines()` methods to `SketchWindow`

The `InitBuffer()` method is added to the `SketchWindow` initialization 
definition. Also, both `InitBuffer()` and `DrawLines()` methods are 
added to the `SketchWindow` class.

The application's source code is:

```python
#!/usr/bin/env python3
import wx

class SketchWindow(wx.Window):
    def __init__(self, parent, id):
        wx.Window.__init__(self, parent, id)
        self.SetBackgroundColour("White")
        self.color = "Black"
        self.thickness = 1
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
        self.lines = []
        self.curLine = []
        self.pos = (0, 0)
        self.InitBuffer()

    def InitBuffer(self):
        size = self.GetClientSize()
        self.buffer = wx.Bitmap(size.width, size.height)
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.DrawLines(dc)
        self.reInitBuffer = False

    def DrawLines(self, dc):
        for colour, thickness, line in self.lines:
            pen = wx.Pen(colour, thickness, wx.SOLID)
            dc.SetPen(pen)
            for coords in line:
                dc.DrawLine(*coords)

class SketchFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, 
                          parent, 
                          -1, 
                          "Sketch Frame", 
                          size = (800, 600))
        self.sketch = SketchWindow(self, -1)

class App(wx.App):
    def OnInit(self):
        self.frame = SketchFrame(None)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()
```

Also, type `$ git checkout 1d` to perform a checkout of this version.

## Bind `OnLeftDown` and `OnLeftUp` events to `SketchWindow` and add 
method definitions

The application's source code is:

```python
#!/usr/bin/env python3
import wx

class SketchWindow(wx.Window):
    def __init__(self, parent, id):
        wx.Window.__init__(self, parent, id)
        self.SetBackgroundColour("White")
        self.color = "Black"
        self.thickness = 1
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
        self.lines = []
        self.curLine = []
        self.pos = (0, 0)
        self.InitBuffer()

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

    def InitBuffer(self):
        size = self.GetClientSize()
        self.buffer = wx.Bitmap(size.width, size.height)
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.DrawLines(dc)
        self.reInitBuffer = False

    def DrawLines(self, dc):
        for colour, thickness, line in self.lines:
            pen = wx.Pen(colour, thickness, wx.SOLID)
            dc.SetPen(pen)
            for coords in line:
                dc.DrawLine(*coords)

    def OnLeftDown(self, event):
        self.curLine = []
        self.pos = event.GetPosition()
        self.CaptureMouse()

    def OnLeftUp(self, event):
        if self.HasCapture():
            self.lines.append((self.color, 
                               self.thickness, 
                               self.curLine))
            self.curLine = []
            self.ReleaseMouse()

class SketchFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, 
                          parent, 
                          -1, 
                          "Sketch Frame", 
                          size = (800, 600))
        self.sketch = SketchWindow(self, -1)

class App(wx.App):
    def OnInit(self):
        self.frame = SketchFrame(None)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()
```

Also, type `$ git checkout 1e` to perform a checkout of this version.
