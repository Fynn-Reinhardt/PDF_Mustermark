# -*- coding: utf-8 -*-
""" GUI script to give easy access to the functions of pdf_mustermark_lib."""

import pdf_mustermark_lib as pml

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import threading
import time


# Class for the thread that the most intensive processing work will
# be done in, so the UI stays snappy (even though it will be hidden behind
# a loading screen for the duration of the process)
class runThread (threading.Thread):
    def __init__(self, pdfmu, reg, f_out, loading_frame, frame):
        threading.Thread.__init__(self)
        self.pdfmu = pdfmu
        self.reg = reg
        self.f_out = f_out
        self.loading_frame = loading_frame
        self.frame = frame
    def run(self):
        print("Start")
        self.pdfmu.mark_document(self.reg)
        self.pdfmu.save_close(self.f_out)
        print("Done")
        
        self.loading_frame.grid_forget()
        self.frame.grid(column=0, row=0, sticky="nsew")


def mark(f_in, f_out, reg):
    try:
        pdfmu = pml.PDFMustermark(f_in)
    except RuntimeError:
        messagebox.showerror(  # Show error message
            title="Input-Datei Error",
            message='Die Datei konnte nicht geöffnet werden.'
            )
        print("Error >:(")  # Show another error message
        return None  # Exit function, 'return' alone would also work

    # Test run to check if the file can save before starting a potentially
    # lenghty and computing power-intensive run through the document
    try:
        pdfmu.save_close(f_out)
    except RuntimeError:
        messagebox.showerror(  # Show error message
            title="Output-Datei Error",
            message=
            'Die Datei konnte nicht an dieser Stelle gespeichert werden.'
            )
        print("Error >:(")  # Show another error message
        return None  # Exit function, 'return' alone would also work

    # get dimensions of window contents
    w = frame.winfo_width()
    h = frame.winfo_height()

    frame.grid_remove()  # Hides UI while the program is working
    # loading screen
    loading_frame = ttk.Frame(root, padding="10")
    loading_frame.grid(column=0, row=0, sticky="nsew")
    loading_label = ttk.Label(loading_frame, text="Arbeitet...")
    loading_label.grid(column=0, row=0, sticky="nsew")
    # set size of loading screen to be identical to the previous window
    loading_frame.config(pad=((w-loading_label.winfo_reqwidth())/2,
                              (h-loading_label.winfo_reqheight())/2))

    newthread = runThread(pdfmu, reg, f_out, loading_frame, frame)
    newthread.start()


root = tk.Tk()
root.title("PDF Mustermark")

frame = ttk.Frame(root, padding="10")
frame.grid(column=0, row=0, sticky="nsew")

file_in = tk.StringVar()
file_in_entry = ttk.Entry(frame, textvariable=file_in)
file_in_entry.grid(column=1, row=0, sticky="we", padx=5, pady=5)

regex = tk.StringVar()
regex.set("(#[IVXLCDM]+[._]\d+\{sid\w{8}\}|#\d+[._]\d+\{sid\w{8}\}|#\d+\{sid\w{8}\})")
regex_entry = ttk.Entry(frame, textvariable=regex)
regex_entry.grid(column=1, row=1, sticky="we", columnspan=2,
                 padx=5, pady=5)

file_out = tk.StringVar()
file_out_entry = ttk.Entry(frame, textvariable=file_out)
file_out_entry.grid(column=1, row=2, sticky="we", padx=5, pady=5)

file_in_button = ttk.Button(frame, text="Öffnen",
    command=lambda: file_in.set(
        filedialog.askopenfilename(
            filetypes=(('pdf document', '*.pdf'),
                       ('all files', '*.*')),
            defaultextension='.pdf')
    ))
file_in_button.grid(column=2, row=0, sticky="e", padx=5, pady=5)

file_out_button = ttk.Button(frame, text="Öffnen",
    command=lambda: file_out.set(
        filedialog.asksaveasfilename(
            filetypes=(('pdf document', '*.pdf'),
                       ('all files', '*.*')),
            defaultextension='.pdf')
    ))

file_out_button.grid(column=2, row=2, sticky="e", padx=5, pady=5)

file_in_label = ttk.Label(frame, text="Input-Datei:")
file_in_label.grid(column=0, row=0, sticky="w", padx=5, pady=5)

file_out_label = ttk.Label(frame, text="Output-Datei:")
file_out_label.grid(column=0, row=2, sticky="w", padx=5, pady=5)

regex_label = ttk.Label(frame, text="RegEx Ausdruck:")
regex_label.grid(column=0, row=1, sticky="w", padx=5, pady=5)

file_out_button = ttk.Button(frame, text="Ausführen",
                             command=lambda: mark(file_in.get(),
                                                  file_out.get(),
                                                  regex.get()))
file_out_button.grid(column=0, row=4, sticky="", columnspan=3,
                     padx=5, pady=5)

root.mainloop()
