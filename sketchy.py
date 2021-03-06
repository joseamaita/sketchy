#!/usr/bin/env python3
import wx
import wx.adv
import pickle, os
from base import SketchWindow
from controlpanel import ControlPanel
from aboutbox import SketchAbout

class SketchFrame(wx.Frame):
    wildcard = "Sketch files (*.sketch)|*.sketch|All files (*.*)|*.*"
    
    def __init__(self, parent):
        self.title = "Sketch Frame"
        wx.Frame.__init__(self, 
                          parent, 
                          -1, 
                          self.title, 
                          size = (800, 600))
        self.filename = ""
        self.sketch = SketchWindow(self, -1)
        self.sketch.Bind(wx.EVT_MOTION, self.OnSketchMotion)
        self.initStatusBar()
        self.createMenuBar()
        self.createToolBar()
        self.createPanel()

    def initStatusBar(self):
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

    def menuData(self):
        return [("&File", (
                          ("&New", "New Sketch file", self.OnNew), 
                          ("&Open", "Open sketch file", self.OnOpen), 
                          ("&Save", "Save sketch file", self.OnSave), 
                          ("", "", ""), 
                          ("&Color", (
                                     ("&Black", 
                                      "", 
                                      self.OnColor, 
                                      wx.ITEM_RADIO), 
                                     ("&Red", 
                                      "", 
                                      self.OnColor, 
                                      wx.ITEM_RADIO), 
                                     ("&Green", 
                                      "", 
                                      self.OnColor, 
                                      wx.ITEM_RADIO), 
                                     ("&Blue", 
                                      "", 
                                      self.OnColor, 
                                      wx.ITEM_RADIO), 
                                      ("&Other...", 
                                      "", 
                                      self.OnOtherColor, 
                                      wx.ITEM_RADIO))),
                          ("", "", ""), 
                          ("About...", "'About' window", self.OnAbout),
                          ("&Quit", "Quit", self.OnCloseWindow)))]

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1]
            menuBar.Append(self.createMenu(menuItems), menuLabel)
        self.SetMenuBar(menuBar)

    def createMenu(self, menuData):
        menu = wx.Menu()
        for eachItem in menuData:
            if len(eachItem) == 2:
                label = eachItem[0]
                subMenu = self.createMenu(eachItem[1])
                menu.Append(wx.NewId(), label, subMenu)
            else:
                self.createMenuItem(menu, *eachItem)
        return menu

    def createMenuItem(self, 
                       menu, 
                       label, 
                       status, 
                       handler, 
                       kind = wx.ITEM_NORMAL):
        if not label:
            menu.AppendSeparator()
            return
        menuItem = menu.Append(-1, label, status, kind)
        self.Bind(wx.EVT_MENU, handler, menuItem)

    def createToolBar(self):
        toolbar = self.CreateToolBar()
        for each in self.toolbarData():
            self.createTool(toolbar, *each)
        toolbar.AddSeparator()
        for each in self.toolbarColorData():
            self.createColorTool(toolbar, each)
        toolbar.Realize()

    def createTool(self, toolbar, label, filename, help, handler):
        if not label:
            toolbar.AddSeparator()
            return
        bitmap = wx.Image(filename, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        tool = toolbar.AddTool(-1, 
                               label, 
                               bitmap, 
                               wx.NullBitmap, 
                               kind = wx.ITEM_NORMAL, 
                               shortHelpString = help, 
                               longHelpString = "", 
                               clientData = None)
        self.Bind(wx.EVT_MENU, handler, tool)

    def toolbarData(self):
        return (("New", 
                 "files/new.bmp", 
                 "Create new sketch", 
                 self.OnNew),
                ("", "", "", ""), 
                ("Open", 
                 "files/open.bmp", 
                 "Open existing sketch", 
                 self.OnOpen),
                ("Save", 
                 "files/save.bmp", 
                 "Save existing sketch", 
                 self.OnSave))

    def createColorTool(self, toolbar, color):
        bmp = self.MakeBitmap(color)
        tool = toolbar.AddRadioTool(-1, 
                                    label = "", 
                                    bitmap1 = bmp, 
                                    bmpDisabled = wx.NullBitmap, 
                                    shortHelp = color, 
                                    longHelp = "", 
                                    clientData = None)
        self.Bind(wx.EVT_MENU, self.OnColor, tool)

    def MakeBitmap(self, color):
        bmp = wx.Bitmap(16, 15)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBackground(wx.Brush(color))
        dc.Clear()
        dc.SelectObject(wx.NullBitmap)
        return bmp

    def toolbarColorData(self):
        return ("Black", "Red", "Green", "Blue")

    def OnNew(self, event): pass
    def OnOpen(self, event): pass

    def OnColor(self, event):
        menubar = self.GetMenuBar()
        itemId = event.GetId()
        item = menubar.FindItemById(itemId)
        if not item:
            toolbar = self.GetToolBar()
            item = toolbar.FindById(itemId)
            color = item.GetShortHelp()
        else:
            color = item.GetLabel()
        self.sketch.SetColor(color)

    def OnCloseWindow(self, event):
        self.Destroy()

    def OnSave(self, event):
        if not self.filename:
            self.OnSaveAs(event)
        else:
            self.SaveFile()

    def OnSaveAs(self, event):
        dlg = wx.FileDialog(self, 
                            "Save sketch as...", 
                            os.getcwd(), 
                            style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT, 
                            wildcard = self.wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            if not os.path.splitext(filename)[1]:
                filename = filename + '.sketch'
            self.filename = filename
            self.SaveFile()
            self.SetTitle(self.title + ' -- ' + self.filename)
        dlg.Destroy()

    def SaveFile(self):
        if self.filename:
            data = self.sketch.GetLinesData()
            f = open(self.filename, 'wb')
            pickle.dump(data, f)
            f.close()

    def OnOpen(self, event):
        dlg = wx.FileDialog(self, 
                            "Open sketch file...", 
                            os.getcwd(), 
                            style = wx.FD_OPEN, 
                            wildcard = self.wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.ReadFile()
            self.SetTitle(self.title + ' -- ' + self.filename)
        dlg.Destroy()

    def ReadFile(self):
        if self.filename:
            try:
                f = open(self.filename, 'rb')
                data = pickle.load(f)
                f.close()
                self.sketch.SetLinesData(data)
            except (EOFError, pickle.UnpicklingError) as e:
                wx.MessageBox("{} is not a sketch file.".\
                              format(self.filename), 
                              "oops!", 
                              style = wx.OK | wx.ICON_EXCLAMATION)

    def OnOtherColor(self, event):
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            self.sketch.SetColor(dlg.GetColourData().GetColour())
        dlg.Destroy()

    def createPanel(self):
        controlPanel = ControlPanel(self, -1, self.sketch)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(controlPanel, 0, wx.EXPAND)
        box.Add(self.sketch, 1, wx.EXPAND)
        self.SetSizer(box)

    def OnAbout(self, event):
        dlg = SketchAbout(self)
        dlg.ShowModal()
        dlg.Destroy()

class App(wx.App):
    def OnInit(self):
        bmp = wx.Bitmap('files/splash.png', wx.BITMAP_TYPE_PNG)
        splash = wx.adv.SplashScreen(bmp, 
                                     wx.adv.SPLASH_CENTRE_ON_SCREEN | \
                                     wx.adv.SPLASH_TIMEOUT, 
                                     6000, 
                                     None, 
                                     -1, 
                                     wx.DefaultPosition, 
                                     wx.DefaultSize, 
                                     wx.BORDER_SIMPLE | wx.STAY_ON_TOP)
        wx.Yield()
        self.frame = SketchFrame(None)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()
