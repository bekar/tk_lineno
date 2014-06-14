#!/usr/bin/env python

# A wrapper to show line numbers for Tkinter Text widgets.
# http://tkinter.unpythonic.net/wiki/A_Text_Widget_with_Line_Numbers

from tkinter import *

class LineNumbedText(Frame):
    UPDATE_PERIOD = 100 # mill seconds
    editors = []
    updateId = None

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.__class__.editors.append(self)
        self.lineNumbers = ''

        # The widgets vertical scrollbar
        self.vScrollbar = Scrollbar(self, orient=VERTICAL)
        self.vScrollbar.pack(fill='y', side=RIGHT)

        # The Text widget holding the line numbers.
        self.lnText = Text(self,
                width = 4,
                padx = 4,
                highlightthickness = 0,
                takefocus = 0,
                bd = 0,
                background = 'lightgrey',
                foreground = 'gray',
                state = 'disabled',
                wrap = NONE
        )

        self.lnText.bind('<Button-4>', lambda e: "break")
        self.lnText.bind('<Button-5>', lambda e: "break")

        self.lnText.pack(side=LEFT, fill='y')

        # The Main Text Widget
        self.text = Text(self,
                bd = 0,
                padx = 4,
                highlightthickness = 0
        )
        self.text.pack(side=LEFT, fill=BOTH, expand=1)

        self.text.config(yscrollcommand=self.vScrollbar.set)
        self.vScrollbar.config(command=self.text.yview)

        if self.__class__.updateId is None:
            self.updateAllLineNumbers()

    def getLineNumbers(self):
        x = 0
        line = '0'
        col = ln = ''
        self.lnText.config(font = self.text['font'])
        # assume each line is at least 6 pixels high
        step = 6

        lineMask = '    %s\n'
        indexMask = '@0,%d'

        for i in range(0, self.text.winfo_height(), step):
            ll, cc = self.text.index(indexMask % i).split('.')
            if line == ll:
                if col != cc:
                    col = cc
                    ln += '\n'
            else:
                line, col = ll, cc
                ln += (lineMask % line)[-5:]
        return ln

    def updateLineNumbers(self):
        tt = self.lnText
        ln = self.getLineNumbers()
        if self.lineNumbers != ln:
            self.lineNumbers = ln
            tt.config(state='normal')
            tt.delete('1.0', END)
            tt.insert('1.0', self.lineNumbers)
            tt.config(state='disabled')

    @classmethod
    def updateAllLineNumbers(cls):
        if len(cls.editors) < 1:
            cls.updateId = None
            return

        for ed in cls.editors:
            ed.updateLineNumbers()

        cls.updateId = ed.text.after(
            cls.UPDATE_PERIOD,
            cls.updateAllLineNumbers)

def demo(noOfLines):
    root.title("Example - Line Numbers For Text Widgets")
    ed = LineNumbedText(root)

    s = 'line '+ '.'*40+ ' %s'
    s = '\n'.join( s%i for i in range(1, noOfLines+1) )

    ed.text.insert(END, s)
    ed.pack(fill='both', expand=1)

if __name__ == '__main__':
    root = Tk()
    demo(9999)
    root.bind('<Key-Escape>', lambda event: quit())
    mainloop()
