import wx
import wx.html

class SketchAbout(wx.Dialog):
    text = '''
<html>
<body bgcolor="#ACAA60">
<center><table bgcolor="#455481" width="100%" cellspacing="0"
cellpadding="0" border="1">
<tr>
    <td align="center"><h1>Sketchy</h1></td>
</tr>
</table>
</center>
<p><b>Sketchy</b> is a simple draw program or doodle application that 
uses the wxPython Phoenix GUI toolkit. It is loosely based on the Doodle 
and Super Doodle samples that are distributed with wxPython. The 
application is written from Noel Rappin and Robin Dunn's book 
<b>"wxPython in Action"</b> (Chapter 6) and should work with Python 
3.4+. If you want to know about wxPython, go 
here <b>https://wxpython.org/</b> for more information.
</p>
</body>
</html>
'''

    def __init__(self, parent):
        wx.Dialog.__init__(self, 
                           parent, 
                           -1, 
                           'About Sketchy', 
                           size = (440, 400))
        html = wx.html.HtmlWindow(self)
        html.SetPage(self.text)
        button = wx.Button(self, wx.ID_OK, "Okay")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()
