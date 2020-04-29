
from tkinter import Scrollbar,TclError,Canvas 
import tkinter.ttk as ttk
import os
import sys
class AutoScrollbar(Scrollbar): 
    def set(self, lo, hi): 
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self) 
        else:
            self.grid()
            Scrollbar.set(self, lo, hi) 
    def pack(self, **kw):
        raise (TclError, "cannot use pack with this widget") 
    def place(self, **kw):
        raise (TclError, "cannot use place with this widget")

def focusTree(tree, ObjectID):
    if len(tree.parent(ObjectID))>0:
        tree.item(tree.parent(ObjectID), open=True) 
        tree.focus_set()
        tree.selection_set(ObjectID) 
        tree.focus(ObjectID)
    else:
        tree.focus_set() 
        tree.selection_set(ObjectID) 
        tree.focus(ObjectID)
        
def ScrollableFrame(treeValuesFrame, orientation) :
    canvas =Canvas(treeValuesFrame) 
    canvas.grid(row=0,column=0, sticky='nsew') 
    canvas.grid_columnconfigure(0,weight=1) 
    if orientation== 'vertical':
        scrollbar = AutoScrollbar(treeValuesFrame, orient=orientation, command=canvas.yview) 
        canvas.configure(yscrollcommand=scrollbar.set) 
        x=treeValuesFrame.grid_size()[0]
        scrollbar.grid(row=0, column=x, sticky='ns') 
        if orientation== 'horizontal':
            scrollbar = AutoScrollbar(treeValuesFrame, orient=orientation, command=canvas.xview) 
            canvas.configure(xscrollcommand=scrollbar.set) 
            scrollbar.grid(column=0, sticky='we')
    if orientation== 'both':
        scrollbar = AutoScrollbar(treeValuesFrame, orient="vertical", command=canvas.yview) 
        canvas.configure(yscrollcommand=scrollbar.set) 
        x=treeValuesFrame.grid_size()[0] 
        scrollbar.grid(row=0, column=x, sticky='ns') 
        scrollbar = AutoScrollbar(treeValuesFrame, orient="horizontal", command=canvas.xview) 
        canvas.configure(xscrollcommand=scrollbar.set) 
        scrollbar.grid(column=0, sticky='we')

    scrollable_frame = ttk.Frame(canvas) 
    scrollable_frame.grid_columnconfigure(0, weight=1) 
    scrollable_frame.grid(column=0, row=0, sticky='nsew') 
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("alt"))) 
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    return scrollable_frame

def scrollableTree(treeFrame,orientation) :
    tree=ttk.Treeview(treeFrame) 
    if orientation== 'vertical':
        yscrollbar=AutoScrollbar(treeFrame,orient=orientation,command=tree.yview) 
        tree.configure(yscrollcommand=yscrollbar.set) 
        yscrollbar.grid(row=0, column=1, sticky='ns')
        yscrollbar.configure(command=tree.yview) 
    if orientation== 'horizontal':
        xscrollbar =AutoScrollbar(treeFrame,orient=orientation, command=tree.xview) 
        tree.configure(xscrollcommand=xscrollbar.set) 
        tree.column("#0", stretch=True, minwidth=1000) 
        xscrollbar.grid(row=1, column=0, sticky='we')
        xscrollbar.configure(command=tree.xview)
    if orientation== 'both':
        yscrollbar =AutoScrollbar(treeFrame, orient='vertical', command=tree.yview) 
        tree.configure(yscrollcommand=yscrollbar.set) 
        yscrollbar.grid(row=0, column=1, sticky='ns') 
        yscrollbar.configure(command=tree.yview) 
        xscrollbar=AutoScrollbar(treeFrame, orient='horizontal', command=tree.xview) 
        tree.configure(xscrollcommand=xscrollbar.set) 
        tree.column("#0", stretch=True,minwidth=1000) 
        xscrollbar.grid(row=1, column=0, sticky= 'we') 
        xscrollbar.configure(command=tree.xview)
    return tree


def get_correct_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
