# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 09:53:39 2020

@author: 840394
"""
# SCRIPT TO BUILD THE GUI OF THE PROFILING TOOL

#pip install pandas
#pip install pandas_profiling
#pip install numpy
#pip install os
#pip install matplotlib.pyplot
#pip install matplotlib.figure
#pip install atplotlib.backends.backend_tkagg
#pip install tkinter

import pandas as pd
import pandas_profiling
#from pandas_profiling import ProfileReport

#import numpy as np
#import os
#import matplotlib.pyplot as plt
#from matplotlib.figure import Figure
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
from tkinter import filedialog
#from tkinter import messagebox


#% ROUTINE TO LOAD FILES
def openSample():
    global dfxls, filename1

    #routine to load the sample data file
    filename1 = filedialog.askopenfilename(initialdir="C:/", title="SELECT SAMPLE FILE", filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
#    os.system(r"notepad.exe " + filename1)
#    dfxls=pd.ExcelFile(filename1)
    dfxls = pd.read_csv(filename1)
    w.plb1.config(text=filename1, relief='groove', wraplength=600, background="white")
    w.plb1.place(x=135, y=30, width=800, height=30)
    
    

def openHeader():
    global columnsName
    
    #routine to load the Headers list
    filename2 = filedialog.askopenfilename(initialdir="C:/", title="SELECT HEADER LIST", filetypes=(("Text file", "*.txt"), ("all files", "*.*")))
#    os.system(r"notepad.exe " + filename2)
    a=open(filename2)
    content=a.read()
    columnsName=content.split("\n")
    a.close()
    w.plb21.config(text=filename2, relief='groove', wraplength=600, background="white")
    w.plb21.place(x=135, y=30, width=800, height=30)
    
def openType():
    global columnsType
    
    #routine to load the Data Type list
    filename3 = filedialog.askopenfilename(initialdir="C:/", title="SELECT DATA TYPE LIST", filetypes=(("Text file", "*.txt"), ("all files", "*.*")))
#    os.system(r"notepad.exe " + filename2)
    a=open(filename3)
    content=a.read()
    columnsType=content.split("\n")
    a.close()
    w.plb22.config(text=filename3, relief='groove', wraplength=600, background="white")
    w.plb22.place(x=135, y=70, width=800, height=30)

def openFormat():
    global columnsFormat
    
    #routine to load the Data FORMAT list
    filename4 = filedialog.askopenfilename(initialdir="C:/", title="SELECT DATA FORMAT LIST", filetypes=(("Text file", "*.txt"), ("all files", "*.*")))
#    os.system(r"notepad.exe " + filename2)
    a=open(filename4)
    content=a.read()
    columnsFormat=content.split("\n")
    a.close()
    w.plb23.config(text=filename4, relief='groove', wraplength=600, background="white")
    w.plb23.place(x=135, y=110, width=800, height=30)

def Profiling1():
    #the "test" varaible can be deleted since it is just a control variable to debug the code
#    global test, main_list
    global my_file
    global profile
    #code to clean the label entry
    w.label3.delete("1.0", tk.END)
    # check the match between the columns names
    MatchNames = list(set(columnsName) & set(list(dfxls.columns))) #safe the columns names that are equal 
    main_list = list(set(columnsName)-set(list(dfxls.columns))) +list(set(list(dfxls.columns))-set(columnsName)) #join all variables that dont match 
    #Condition to alert in case the number of Columns of the sample dataset doesnt match the number of header entries
    # initial condition checks for the case that the Sampled dataset has columns with the name 'row_id'
    if str(dfxls.columns[0]) == 'row_id':
        if len(columnsName) != len(list(dfxls.columns[1::])):
            textwarn = "######## WARNING ########\n Number of header entries = " + str(len(columnsName)) + "\nNumber of file columns = " + str((len(dfxls.columns[1::]))) + "\n### Please be aware that the number of input headers doesnt match with th number of columns of the table!!"
        else: 
            textwarn = "### All correct with the number of headers and the number of columns in the table! ###\n##################################################################\n"
    else:
        if len(columnsName) != len(list(dfxls.columns)):
            textwarn = "######## WARNING ########\n Number of header entries = " + str(len(columnsName)) + "\nNumber of file columns = " + str((len(dfxls.columns))) + "\n### Please be aware that the number of input headers doesnt match with th number of columns of the table!!  ###\n############################################################\n" 
        else:
            textwarn = "### All correct with the number of headers and the number of columns in the table! ###\n##################################################################\n"

    # code to check and output the columns from the header file and from the sampple data that dont match. The 'row_id' shall not be outputed
    if main_list is not None:
        textwarn2 = "The following Names dont match:\n"
        control = "b" 
        for i in range(0,len(main_list)):
            if main_list[i].lower() != 'row_id': # line to remove the 'row_id' from being outputed
                textwarn2 = textwarn2 + str(main_list[i]) + "; "
                control="a"
        if control == "a":
            textwarn2 = textwarn2 + '\n### Please note that the Profiling might be incorrect due to column Names inconsistencies!! ###\n'
    else:
        textwarn2 = " "
    textout= textwarn + textwarn2
    w.label3.config(font=("Helvetica",12))
    w.label3.insert(tk.END, textout)# , relief='groove', wraplength=600, background="white"
    w.label3.place(x=10,y=40, width=980, height=100)

    #% change/confirm data type columns for the columns that have equal names
    #rules can be made to different data types (e.g. int, char, date, etc) and data formats (e.g phone number, nif, email, etc)
    #still missing rules for 

    for i in range(0,len(MatchNames),1):# make sure that we cover all the matching entries
        idx=columnsName.index(MatchNames[i]) # take the index on the loaded dataset were the header matches
    
        #define rule to change the column to a Date format
        if columnsType[idx].upper()=='DATE':
            #insert rotine to check if the column has nay variation
            if dfxls[MatchNames[i]].std() == 0: #if variable has a std eaul 0 then define as "str"
                dfxls[MatchNames[i]]=dfxls[MatchNames[i]].astype(str)
            else: # otherwise define variable as date
                dfxls[MatchNames[i]]=dfxls[MatchNames[i]].astype(str)
                dfxls[MatchNames[i]]=dfxls[MatchNames[i]].astype('M8')
#       dfxls[MatchNames[i]]=pd.to_datetime(dfxls[MatchNames[i]], format='%Y%m%d')
        #make sure that the column is set to string
        if columnsType[idx].upper()=='VARCHAR':
            dfxls[MatchNames[i]]=dfxls[MatchNames[i]].astype(str)
        #make sure that the column is set to int
        if columnsType[idx].upper()=='INTEGER':
            dfxls[MatchNames[i]]=dfxls[MatchNames[i]].astype("int64")
    
    # run the profile report
    profile = pandas_profiling.ProfileReport(dfxls) #uncomment
#    profile = ProfileReport(dfxls)
    #   
    ## save the report as html file
    a=filename1.split(sep="/")
    my_path= '/'.join(map(str,a[0:-1]))
    my_file =  my_path + "/" + "ProfileReport.html"
#    profile.to_file(output_file = my_file)
    profile.to_file(output_file = "ProfileReport1.html")#uncomment

#def __main__():
#% BUILD THE WINDOW
#def main():
global w
w = tk.Tk()  # create window
w.configure(bg='lightgrey')
w.title("Galp CDO Profiling")

# frame for Load Sample Data
w.mF1 =tk.Frame(w, width=1000, height=80, bg='SlateGray1')
w.mF1.grid()
# frame for load headers, format, type
w.mF2 =tk.Frame(w, width=1000, height=145, bg='SlateGray2')
w.mF2.grid()

# frame To Run the Profilling
w.mF3 =tk.Frame(w, width=1000, height=145, bg='SlateGray3')
w.mF3.grid()

# configure a menu bar to refresh and/or destroy the window
w.menubar = tk.Menu(w)
# Adding File Menu and commands
w.Options = tk.Menu(w.menubar, tearoff=0)
#    w.menubar.add_cascade(label="Options", menu = Options)
w.menubar.add_cascade(label="Options", menu = w.Options)
#Options.add_command(label ='Refresh', command=window.update) # create a command to refresh all the variables and objects
w.Options.add_command(label ='Exit', command = w.destroy)

w.config(menu=w.menubar)


## Create block of peaces to load the sample data
# include a title for Load the Sampling File
w.label1 = tk.Label(w.mF1, text="LOAD SAMPLE DATA", bg="white").place(x=400,y=5, width=300, height=20)
# Label tooutput the file path of the Sample file
w.plb1 = tk.Label(w.mF1, text="")# plb1.place(x=135, y=30, width=800, height=30)
# create a browse button for user to load the sample data
w.s1 = tk.Button(w.mF1, text="Browse Sample File", command=openSample).place(x=10, y=30, width=120, height=30)


## Create block of peaces to load load headers, type, format
# include a title for Load the Sampling File
w.label2 = tk.Label(w.mF2, text="LOAD HEADERS, TYPE, FORMAT", bg="white").place(x=400,y=5, width=300, height=20)

# Label tooutput the file path of the Header file
w.plb21 = tk.Label(w.mF2, text="")
# Label tooutput the file path of the Type file
w.plb22 = tk.Label(w.mF2, text="")
# Label tooutput the file path of the Format file
w.plb23 = tk.Label(w.mF2, text="")

# create a browse button for user to load Header
w.s21 = tk.Button(w.mF2, text="Browse HEADER", command=openHeader).place(x=10, y=30, width=120, height=30)
# create a browse button for user to load Format
w.s22 = tk.Button(w.mF2, text="Browse TYPE", command=openType).place(x=10, y=70, width=120, height=30)
# create a browse button for user to load Type
w.s23 = tk.Button(w.mF2, text="Browse FORMAT", command=openFormat).place(x=10, y=110, width=120, height=30)

## Create block to Run the profiling and give user the status
# create a browse button for user to load Header
w.s31 = tk.Button(w.mF3, text="Run Profiling", command=Profiling1).place(x=480, y=5, width=120, height=30) #, command=XX

# include a title for Load the Sampling File
#label3 = tk.Label(mF3, text="")
w.label3 = tk.Text(w.mF3, font=("Helvetica", 32))

w.mainloop()
    

#if __name__ == '__main__':
#    main()