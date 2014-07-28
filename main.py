#!/usr/bin/env python
''' Line Number Text with font resize binding '''

# A wrapper to show line numbers for Tkinter Text widgets.
# http://tkinter.unpythonic.net/wiki/A_Text_Widget_with_Line_Numbers
# https://github.com/bekar/tk_zoomText

from tkinter import *
from tkinter.ttk import *
import tkinter.font as tkFont

class LineNumbedText(Text):
    '''Text widget with the frame container in grid layout'''
    UPDATE_PERIOD = 100 # mill seconds

    def __init__(self, parent=None, **opts):
        self.container = Frame(parent)

        # self text widget
        Text.__init__(self, self.container, **opts)
        self.config(bd = 0, padx = 4, highlightthickness = 0)

        self.grid(row=0, column=1, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        self.lineNumbers = ''

        # The widgets vertical scrollbar
        self.vScrollbar = Scrollbar(self.container, orient="vertical")
        self.vScrollbar.grid(row=0, column=2, sticky="nsew")
        self.config(yscrollcommand=self.vScrollbar.set)
        self.vScrollbar.config(command=self.yview)

        # The Text widget holding the line numbers.
        self.lnText = Text(self.container,
                width = 4,
                padx = 4,
                highlightthickness = 0,
                takefocus = 0,
                bd = 0,
                background = '#eae8e3',
                foreground = 'gray',
                state = 'disabled',
                wrap = 'none'
        )
        self.lnText.grid(row=0, column=0, sticky="nsew")

        self.updateLineNumbers()

        self.bind_keys()

    def bind_keys(self):
        self.lnText.bind('<Button-4>', lambda e: "break")
        self.lnText.bind('<Button-5>', lambda e: "break")
        self.bind('<Control-Button-4>', lambda e: self.resize(1))
        self.bind('<Control-Key-plus>', lambda e: self.resize(1))
        self.bind('<Control-Button-5>', lambda e: self.resize(-1))
        self.bind('<Control-Key-minus>', lambda e: self.resize(-1))
        self.bind('<Control-0>', lambda e: self.font.config(size=self.size))

    def resize(self, d=1):
        '''Text() font resize for key binding Ctrl + {Scroll,+,-,0}'''

        self.config(state="normal")
        self.container.grid_propagate(False)

        font_names = [ self.tag_cget(t, "font") for t in self.tag_names() ]
        font_names.append(self['font'])

        for name in set(font_names):
            try:
                font = tkFont.nametofont(name)
                s = abs(font["size"]); #print(s)
                font.config(size=max(s+2*d, 8))
            except:
                continue

        self.config(state="disable")

    def pack(self, **opts):
        '''pseudo packing wrapper to access Frame'''
        args = ""
        for key in opts:
            args += ' %s="%s",'%(key, opts[key])

        exec("self.container.pack(%s)"%args[:-1])

    def getLineNumbers(self):
        x = 0
        line = '0'
        col = ln = ''
        self.lnText.config(font = self['font'])
        # assume each line is at least 6 pixels high
        step = 6

        lineMask = '    %s\n'
        indexMask = '@0,%d'

        for i in range(0, self.winfo_height(), step):
            ll, cc = self.index(indexMask % i).split('.')
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
            tt.delete('1.0', 'end')
            tt.insert('1.0', self.lineNumbers)
            tt.config(state='disabled')

        self.after(self.__class__.UPDATE_PERIOD,
                 self.updateLineNumbers)

def demo(noOfLines):
    root.title("Example - Line Numbers For Text Widgets")
    ed = LineNumbedText(root)

    s = 'line '+ '.'*40+ ' %s'
    s = '\n'.join( s%i for i in range(1, noOfLines+1) )

    ed.insert('end', s)
    ed.pack(fill='both', expand=1)

if __name__ == '__main__':
    root = Tk()
    demo(9999)
    root.bind('<Key-Escape>', lambda event: root.quit())
    root.mainloop()
