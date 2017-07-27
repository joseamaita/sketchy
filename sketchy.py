#!/usr/bin/env python3
import wx
from base import SketchWindow

class SketchFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, 
                          parent, 
                          -1, 
                          "Sketch Frame", 
                          size = (800, 600))
        self.sketch = SketchWindow(self, -1)
        self.sketch.Bind(wx.EVT_MOTION, self.OnSketchMotion)
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1, -2, -3])

    def OnSketchMotion(self, event):
        self.statusbar.SetStatusText("Pos: {}".\
                                     format(str(event.GetPosition())), 
                                     0)
        self.statusbar.SetStatusText("Current Pts: {}".\
                                     format(len(self.sketch.curLine)), 
                                     1)
        self.statusbar.SetStatusText("Line Count: {}".\
                                     format(len(self.sketch.lines)), 
                                     2)
        event.Skip()

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
