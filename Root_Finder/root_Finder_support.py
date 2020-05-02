#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 5.0.3
#  in conjunction with Tcl version 8.6
#    Apr 15, 2020 05:32:31 PM +0200  platform: Windows NT

import sys
from decimal import Decimal
from numpy import double
import time
import solutionTechniuqes as st
import graphPlotter as gp
import traceback
from reportlab.pdfgen import canvas
import PyPDF2

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True

from tkinter.filedialog import *


def set_Tk_var():
    global combobox
    combobox = tk.StringVar()
    global check68
    check68 = tk.BooleanVar()
    global expression
    expression = tk.StringVar()
    global iter
    iter = tk.StringVar()
    global precision
    precision = tk.StringVar()
    global upper
    upper = tk.StringVar()
    global lower
    lower = tk.StringVar()
    global guess1
    guess1 = tk.StringVar()
    global guess2
    guess2 = tk.StringVar()


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


def solve(txt, gph):
    for widget in gph.winfo_children():
        widget.destroy()
    txt.delete("1.0", tk.END)
    method = combobox.get().lower()
    try:
        exp = expression.get()
        i = int(iter.get())
        pre = double(precision.get())
        num_digits = abs(Decimal(precision.get()).as_tuple().exponent)
        solver = st.solution_techinques(exp)
        if method == 'bisection method' or method == 'regula-falsi method':
            tech = 0
            low = double(lower.get())
            up = double(upper.get())
            current = time.time() * 1000
            if method == 'bisection method':
                answer = solver.bisection(up, low, pre, i, num_digits)
            else:
                answer = solver.regulafalsi(up, low, pre, i, num_digits)
            s = print_indirect(txt, answer, current)
            # if s != -1:
            #     gp.graphPlotter(gph, tech, answer, solver)
        elif method == 'fixed point iteration method' or method == 'newton raphson method':
            guess = double(guess1.get())
            current = time.time() * 1000
            if method == 'fixed point iteration method':
                tech = 1
                answer = solver.FixedPoint(guess, pre, i, num_digits)
            else:
                tech = 2
                answer = solver.newtonRaphson(guess, pre, i, num_digits)
            s = print_fixed_newton(txt, answer, current)
            # if s != -1:
            #     gp.graphPlotter(gph, tech, answer, solver)
        else:
            tech = 3
            guess_1 = double(guess1.get())
            guess_2 = double(guess2.get())
            current = time.time() * 1000
            answer = solver.secant(guess_1, guess_2, pre, i, num_digits)
            s = print_secant(txt, answer, current)
            # if s != -1:
            #     gp.graphPlotter(gph, 3, answer, solver)
        if s != -1:
            if check68.get() == TRUE:
                w = write_in_file(s, answer, tech, exp)
                if w:
                    gp.graphPlotter(gph, tech, answer, solver, True, w[0].replace('.pdf', 'Figs.pdf'))
            else:
                txt.insert(tk.END, s)
                gp.graphPlotter(gph, tech, answer, solver, False, '')

    except Exception:
        traceback.print_exc()
        txt.insert(tk.END, 'Wrong input format')
    sys.stdout.flush()


def write_in_file(s, answer, tech, expression):
    filename = asksaveasfile(mode='w', filetypes=[('PDF File', '*.pdf')] , defaultextension=[('PDF File', '*.pdf')])
    if filename is None:
        return False
    pdf = canvas.Canvas(filename.name)
    pdf.setTitle('Root Finder Result')
    lines = s.split('\n')
    pdf.drawString(40, 800, 'Root Finder Results For: F(x) = ' + expression)
    pdf.drawString(40, 780, lines[0].replace('\t', '   '))
    pdf.drawString(40, 720, 'iter')
    for i in range(len(answer[0])):
        pdf.drawString(40, 700-(i * 20), '{}'.format(i+1))

    i = 0
    if tech == 0:
        pdf.drawString(70, 720, '(Upper, Lower) Bounds')
        pdf.drawString(300, 720, 'Xi')
        pdf.drawString(450, 720, 'Accuracy')
        for bound in answer[1]:
            pdf.drawString(70, 700-(i * 20), '({}, {})'.format(bound[0], bound[1]))
            pdf.drawString(300, 700 - (i * 20), '{}'.format(answer[0][i]))
            if i == 0:
                pdf.drawString(450, 700 - (i * 20), '---')
            else:
                pdf.drawString(450, 700 - (i * 20), '{}'.format(answer[2][i - 1]))
            i += 1
    elif tech == 1 or tech == 2:
        pdf.drawString(100, 720, 'Xi-1')
        pdf.drawString(300, 720, 'Xi')
        pdf.drawString(450, 720, 'Accuracy')
        for i in range(len(answer[0])):
            pdf.drawString(100, 700 - (i * 20), '{}'.format(answer[1][i]))
            pdf.drawString(300, 700 - (i * 20), '{}'.format(answer[0][i]))
            pdf.drawString(450, 700 - (i * 20), '{}'.format(answer[2][i]))
            i += 1
    else:
        pdf.drawString(70, 720, 'Xi-2')
        pdf.drawString(150, 720, 'Xi-1')
        pdf.drawString(300, 720, 'Xi')
        pdf.drawString(450, 720, 'Accuracy')
        for i in range(len(answer[0])):
            pdf.drawString(70, 700 - (i * 20), '{}'.format(answer[1][i][0]))
            pdf.drawString(150, 700 - (i * 20), '{}'.format(answer[1][i][1]))
            pdf.drawString(300, 700 - (i * 20), '{}'.format(answer[0][i]))
            pdf.drawString(450, 700 - (i * 20), '{}'.format(answer[2][i]))
            i += 1

    pdf.save()

    pages = []
    pdf_file_obj = open(filename.name, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
    i = 0
    while i < pdf_reader.getNumPages():
        pages.append(pdf_reader.getPage(i))
        i += 1
    pdf_file_obj.close()
    return [filename.name, pages]


def print_indirect(console, answer, current):
    if answer == 'No root in this interval':
        console.insert(tk.END, answer)
        return -1
    s = ''
    s += 'Calculated root: {}\t in: {} milliseconds\n\n'.format(answer[0][len(answer[0]) - 1],
                                                                time.time() * 1000 - current)
    s += 'Iter\t(Upper, Lower) Bounds\t\t\tXi\t\tAccuracy\n'
    i = 0
    for bound in answer[1]:
        if i == 0:
            s += '{}\t({}, {})\t\t\t{}\t\t---\n'.format(i + 1, bound[0], bound[1], answer[0][i])
        else:
            s += '{}\t({}, {})\t\t\t{}\t\t{}\n'.format(i + 1, bound[0], bound[1], answer[0][i], answer[2][i - 1])
        i += 1
    return s


def print_fixed_newton(console, answer, current):
    if answer == 'This method diverges' or answer == 'Overflow in math range':
        console.insert(tk.END, answer)
        return -1
    s = ''
    s += 'Calculated root: {}\t in: {} milliseconds\n\n'.format(answer[0][len(answer[0]) - 1],
                                                                time.time() * 1000 - current)
    s += 'Iter\tXi-1\t\tXi\t\tAccuracy\n'
    i = 0
    for guess in answer[1]:
        s += '{}\t{}\t\t{}\t\t{}\n'.format(i + 1, guess, answer[0][i], answer[2][i])
        i += 1
    return s


def print_secant(console, answer, current):
    if answer == 'This method diverges' or answer == 'Overflow in math range':
        console.insert(tk.END, answer)
        return -1
    s = ''
    s += 'Calculated root: {}\t in: {} milliseconds\n\n'.format(answer[0][len(answer[0]) - 1],
                                                                time.time() * 1000 - current)
    s += 'Iter\tXi-2\t\tXi-1\t\tXi\t\tAccuracy\n'
    i = 0
    for guess in answer[1]:
        s += '{}\t{}\t\t{}\t\t{}\t\t{}\n'.format(i + 1, guess[0], guess[1], answer[0][i], answer[2][i])
        i += 1
    return s


def read_file(txt):
    file = askopenfile()
    fh = open(file.name, 'r')
    for line in fh:
        words = line.lower().rstrip('\n').split('=')
        if words[0] == 'method':
            method = words[1][:len(words[1])]
            if method.__contains__('method'):
                combobox.set(method)
            else:
                combobox.set(method + ' method')
        elif words[0] == 'f(x)':
            expression.set(words[1][:len(words[1])])
        elif words[0] == 'iterations':
            iter.set(words[1][:len(words[1])])
        elif words[0] == 'precision':
            precision.set(words[1][:len(words[1])])
        elif words[0] == 'upper bound':
            upper.set(words[1][:len(words[1])])
        elif words[0] == 'lower bound':
            lower.set(words[1][:len(words[1])])
        elif words[0] == 'guess1':
            guess1.set(words[1][:len(words[1])])
        elif words[0] == 'guess2':
            guess2.set(words[1][:len(words[1])])
        else:
            txt.delete("1.0", tk.END)
            txt.insert(tk.END, 'Error reading file')

    sys.stdout.flush()


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


if __name__ == '__main__':
    import root_Finder

    root_Finder.vp_start_gui()
