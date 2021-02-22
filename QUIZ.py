from tkinter import Tk, Frame, Label, Button, Entry, PhotoImage
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
import operator
import tkinter
from pandas import DataFrame
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


class Button(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)#zmiana koloru po najechaniu na przycisk
        self.bind("<Leave>", self.on_leave)#zmiana koloru po wyjsciu z przycisku

    def on_enter(self, e):
        self["background"] = self["activebackground"]

    def on_leave(self, e):
        self["background"] = self.defaultBackground
        
class Question:
    def __init__(self, question, answers, correctLetter):
        self.question = question
        self.answers = answers
        self.correctLetter = correctLetter

    def check(self, letter, view):
        global right
        if(letter == self.correctLetter):
            label = Label(view, width = 60, text="Right!", bg="#69ffb9")
            right += 1
        else:
            label = Label(view, width = 60, text="Wrong!", bg="#e8503c")
            questionss = self.question
            f=open('incorrect.txt','r')
            lista=f.readlines()
            listap = []
            slownik = {}
            for x in lista:
                y = x.strip()
                listap.append(y)
            for c in range(0, len(listap), 2):
                    slownik[listap[c]]= int(listap[c+1])
            
            if questionss.rstrip() in slownik:
                j = slownik[questionss.rstrip()]
                slownik[questionss.rstrip()]= int(j) + 1
            else:
                slownik[questionss.rstrip()]= 1
            
            f.close()
            sortedDict = sorted(slownik.items(), key=operator.itemgetter(1,0), reverse=True)
            h=open('incorrect.txt','w')
            list2 = sortedDict
            for g in list2:
                for k in g:
                    h.write(str(k)+"\n")
            h.close()

        label.grid(row = 4, column = 1, columnspan=2, padx=20, pady=20)
        view.after(1000, lambda *args: self.unpackView(view))
        return

    def getView(self, window):
        view = Frame(window)
        view.configure(background='#0049ba')
        Label(view, width = 60, text=self.question, bg="#77abfc").grid(row = 1, column = 1, columnspan = 2)
        Button(view, width = 25, text=self.answers[0], activebackground="white", bg="#77abfc", command=lambda *args: self.check("A", view)).grid(row = 2, column = 1, padx=15, pady=15)
        Button(view, width = 25, text=self.answers[1], activebackground="white", bg="#77abfc", command=lambda *args: self.check("B", view)).grid(row = 2, column = 2, padx=15, pady=15)
        Button(view, width = 25, text=self.answers[2], activebackground="white", bg="#77abfc", command=lambda *args: self.check("C", view)).grid(row = 3, column = 1)
        Button(view, width = 25, text=self.answers[3], activebackground="white", bg="#77abfc", command=lambda *args: self.check("D", view)).grid(row = 3, column = 2)
        Label(view, width = 60, text="", bg="#77abfc",).grid(row = 4, column = 1, columnspan = 2, padx=20, pady=20)
        return view

    def unpackView(self, view):
        view.grid_forget()
        askQuestion()


def askQuestion():
    global questions, window, index, button, right, number_of_questions, entry, buttonn, description, label1, btGraph
    if(len(questions) == index + 1):
        Label(window, bg="#77abfc", text="Thank you for answering the questions. " + str(right) + " of " + str(number_of_questions) + "\n questions answered right").grid(column = 0, columnspan=2)
        buttonn = Button(window, width = 15, text="Ranking", bg="#77abfc", command=showRanking)
        buttonn.grid(column = 0, columnspan=2)
        btGraph = Button(window, width = 15, text="Wykres", bg="#77abfc", command=showGraph)
        btGraph.grid(column = 0, columnspan=2)
        name = s.get()
        f=open('records.txt','r')
        lista=f.readlines()
        listap = []
        slownik = {}
        for x in lista:
            y = x.strip()
            listap.append(y)
        for c in range(0, len(listap), 2):
                slownik[listap[c]]= int(listap[c+1])
        
        if name in slownik:
            j = slownik[name]
            slownik[name]= int(j) + int(right)
        else:
            slownik[name]= int(right)
        
        f.close()
        sortedDict = sorted(slownik.items(), key=operator.itemgetter(1,0), reverse=True)
        h=open('records.txt','w')
        list2 = sortedDict
        for g in list2:
            for k in g:
                h.write(str(k)+"\n")
        h.close()
        return
    entry.grid_forget()
    button.grid_forget()
    button2.grid_forget()
    description.grid_forget()
    index += 1
    questions[index].getView(window).grid()

def showRanking():
    buttonn.grid_forget()
    name = s.get()
    f=open('records.txt','r')
    lista=f.readlines()
    listap = []
    for x in lista:
        y = x.strip()
        listap.append(y)
    username = []
    results = []
    for el in range(0,len(listap),2):
        username.append(listap[el])
    for ell in range(1,len(listap),2):
        results.append(listap[ell])
        
    Label(window, bg="black", width = 30, text = "Username: ", fg = "white").grid(row = 1, column=0,sticky='we')
    Label(window, bg="black", width = 30, text = "Wynik: ", fg = "white").grid(row = 1, column=1,sticky='we')
    pos = username.index(name)
    for l in range(0,5):
        if username[l] == name:
            Label(window, bg="#ff6b75", width = 15, text = username[l]).grid(row = l+2, column = 0)
        else:
            Label(window, bg="#ceabff", width = 15, text = username[l]).grid(row = l+2, column = 0)
    for ll in range(0,5):
        if ll == int(pos):
            Label(window, bg="#ff6b75", width = 15, text = results[ll]).grid(row = ll+2, column = 1)
        else:
            Label(window, bg="#ceabff", width = 15, text = results[ll]).grid(row = ll+2, column = 1)
    f.close()


def questionEditor():
    global buttonAdd, buttonDel,buttonEdit, entryAdd, entry1,entry2, entry3,entry4,comboboxChange,entryAns,buttonWroc,combobox,combobox1,buttonAdd1, buttonZmiana, buttonZatwierdz, desc
    buttonAdd = Button(window, width = 15, height = 2, text="Dodaj", activebackground="green", command=addQuestion)
    buttonDel = Button(window, width = 15, height = 2, text="Usuń", activebackground="green", command=deleteQuestion)
    buttonEdit = Button(window, width = 15, height = 2, text="Edytuj", activebackground="green", command=changeQuestion)
    buttonAdd.grid(row = 2, column = 0, columnspan=4, sticky="W", padx="10")
    buttonDel.grid(row = 2, column = 0, columnspan=4, sticky="E", padx="10")
    buttonEdit.grid(row = 2, column = 0, columnspan=4, sticky="S", padx="10", pady="15")

    entry.grid_forget()
    button.grid_forget()
    button2.grid_forget()
    description.grid_forget()
    try:
        combobox1.grid_forget()
    except:
        pass
    try:
        combobox.grid_forget() 
        buttonWroc.grid_forget()
        desc.grid_forget()
    except:
        pass
    try:
        entry1.grid_forget()
        entry2.grid_forget()
        entry3.grid_forget()
        entry4.grid_forget()
        entryAns.grid_forget()
        buttonWroc.grid_forget()
        entryAdd.grid_forget()
        buttonAdd1.grid_forget()
    except:
        pass
    try:
        comboboxChange.grid_forget()
        buttonZmiana.grid_forget()
        buttonZatwierdz.grid_forget()
        entryAns.grid_forget()
        entry2.grid_forget()
        entry3.grid_forget()
        entry4.grid_forget()
        entry1.grid_forget()
        entryAdd.grid_forget()   
    except:
        pass


def callbackDel(eventObject):
    o = eventObject.widget.get()
    f=open('questions.txt','r+')
    lista=f.readlines()
    listap = []
    listaStrip = []
    f.close()
    
    h=open('questions.txt','w')   
    for x in range(0,len(lista),6):
        y = lista[x].strip()
        listap.append(y) 
        
    for element in lista:
        listaStrip.append(element.strip())
    index = listaStrip.index(o)  
    for ex in range(0,6):
        lista.pop(index)
        
    for ele in lista:
        h.write(ele)
    h.close()
    print("delete")
    
    
def deleteQuestion():
    global combobox, buttonWroc1, desc
    buttonWroc1 = Button(window, width = 15, height = 2, text="Wróć", activebackground="green", command=questionEditor)
    buttonWroc1.grid(row = 2, column = 0, columnspan=4, sticky="E", padx="10", pady = "15")
    desc = Label(window, width = 60, height = 2, text="Po wybraniu pytania zostanie on automatycznie usunięte.")
    desc.grid(row = 0, column = 0, columnspan = 2, sticky = "N",pady = "15")
    f=open('questions.txt','r')
    lista=f.readlines()
    listap = []
    f.close()
    for x in range(0,len(lista),6):
        y = lista[x].strip()
        listap.append(y)
    cb_value = tk.StringVar() # zmienna typu StringVar, która zostanie podpięta pod kontrolkę Combobox
    combobox = ttk.Combobox(window, textvariable = cb_value, width=50) # tworzenie kontrolki Combobox
    combobox.grid(row = 0, column = 0, columnspan=2, sticky = "W",padx="75", pady="10") # umieszczenie kontrolki na oknie głównym
    combobox['values'] = listap # ustawienie elementów zawartych na liście rozwijanej
    combobox.bind("<<ComboboxSelected>>", callbackDel)
    entry.grid_forget()
    button.grid_forget()
    button2.grid_forget()
    description.grid_forget()
    buttonAdd.grid_forget()
    buttonEdit.grid_forget()
    buttonDel.grid_forget()



def changeQuestion():
    global comboboxChange,lista, buttonZmiana
    buttonZmiana = Button(window, width = 15, height = 2, text="Zmien", activebackground="green") 
    buttonZmiana.grid(row = 2, column = 0, columnspan=4, sticky="S", padx="10", pady="15")
    buttonWroc = Button(window, width = 15, height = 2, text="Wróć", activebackground="green", command=questionEditor)
    buttonWroc.grid(row = 2, column = 1, columnspan=4, sticky="E", padx="10", pady="15")
    f = open("questions.txt","r")
    lista = f.readlines()
    f.close()
    listaPytan = []
    
    for x in range(0,len(lista),6):
        y = lista[x].strip()
        listaPytan.append(y)
    print(listaPytan)
    
    
    wartoscCombo = tk.StringVar()
    comboboxChange = ttk.Combobox(window, textvariable = wartoscCombo, width=50)
    comboboxChange.grid(row = 0, column = 0, columnspan=2, sticky = "N", pady="10")
    comboboxChange['values'] = listaPytan
    comboboxChange.bind("<<ComboboxSelected>>", changeQuestioncd)
    
    try:
        entry.grid_forget()
        button.grid_forget()
        button2.grid_forget()    
        description.grid_forget()   
        buttonAdd.grid_forget()   
        buttonDel.grid_forget()
        buttonEdit.grid_forget()
    except:
        pass
    try:
        buttonAdd1.grid_forget() 
    except:
        pass
    
def changeQuestioncd(eventObject):
    o = eventObject.widget.get() # pobrane pytanie
    global ss1,ans12,ans22,ans32,ans42,ansCorrect2, index, entryAdd,entry1,entry2,entry3,entry4,entryAns, buttonZatwierdz
    ss1 = StringVar()
    ans12 = StringVar()
    ans22 = StringVar()
    ans32 = StringVar()
    ans42 = StringVar()
    ansCorrect2 = StringVar()
    
    index = lista.index(o+"\n")
    
    
    entryAdd=Entry(window, textvariable=ss1, width=60)
    entryAdd.insert(0, lista[index])
    entryAdd.grid(row=0, columnspan=4, sticky="N", pady="20")
    
    entry1=Entry(window, textvariable=ans12)
    entry1.insert(0, lista[index+1])
    entry1.grid(row=0, columnspan=4, sticky="W", padx="20")

    entry2=Entry(window, textvariable=ans22)
    entry2.insert(0, lista[index+2])
    entry2.grid(row=0, columnspan=4, sticky="E", padx="20")

    entry3=Entry(window, textvariable=ans32)
    entry3.insert(0, lista[index+3])
    entry3.grid(row=0, columnspan=4, sticky="SW", pady="20", padx="20")
    
    entry4=Entry(window, textvariable=ans42)
    entry4.insert(0, lista[index+4])
    entry4.grid(row=0, columnspan=4, sticky="SE", pady="20", padx="20")
    
    entryAns=Entry(window, textvariable=ansCorrect2, width=5)
    entryAns.insert(0, lista[index+5])
    entryAns.grid(row=0, columnspan=4, sticky="S", pady="20")


    buttonZatwierdz = Button(window, width = 15, height = 2, text="Zatwierdz", activebackground="green", command=getChanges) 
    buttonZatwierdz.grid(row = 2, column = 0, columnspan=4, sticky="S", padx="10", pady = "15")    
    comboboxChange.grid_forget()
    buttonZmiana.grid_forget()
    
def getChanges():
    pytanie = ss1.get()
    odp1 = ans12.get()
    odp2 = ans22.get()
    odp3 = ans32.get()
    odp4 = ans42.get()
    odpowiedzPoprawna = ansCorrect2.get()
    lista[index] = pytanie
    lista[index+1] = odp1
    lista[index+2] = odp2
    lista[index+3] = odp3
    lista[index+4] = odp4
    lista[index+5] = odpowiedzPoprawna
    h = open("questions.txt","w")
    for x in lista:
        h.write(x.strip())
        h.write("\n")
    h.close()
    print("changed")


def addQuestion():
    global ss,ans1,ans2,ans3,ans4,ansCorrect,buttonWroc,entry1,entry2,entry3,entry4,entryAns,entryAdd, buttonAdd1
    buttonAdd.grid(row = 2, column = 0, columnspan=4, sticky="S", padx="10")
    ss = StringVar()
    ans1 = StringVar()
    ans2 = StringVar()
    ans3 = StringVar()
    ans4 = StringVar()
    ansCorrect = StringVar()
    entryAdd=Entry(window, textvariable=ss, width=40, justify="center")
    entryAdd.insert(0, "Wpisz pytanie")
    entryAdd.grid(row=0, columnspan=4, sticky="N", pady="30")
    
    entry1=Entry(window, textvariable=ans1, justify="center", width=30)
    entry1.insert(0, "Odp A")
    entry1.grid(row=0, columnspan=4, sticky="W", padx="25")

    entry2=Entry(window, textvariable=ans2, justify="center", width=30)
    entry2.insert(0, "Odp B")
    entry2.grid(row=0, columnspan=4, sticky="E", padx="25")

    entry3=Entry(window, textvariable=ans3, justify="center", width=30)
    entry3.insert(0, "Odp C")
    entry3.grid(row=0, columnspan=4, sticky="SW", pady="20", padx="25")
    
    entry4=Entry(window, textvariable=ans4, justify="center", width=30)
    entry4.insert(0, "Odp D")
    entry4.grid(row=0, columnspan=4, sticky="SE", pady="20", padx="25")
    
    entryAns=Entry(window, textvariable=ansCorrect, width=5, justify="center")
    entryAns.insert(0, "Litera")
    entryAns.grid(row=0, columnspan=4, sticky="S", pady="20")
    print(ss.get())

    
    buttonAdd1 = Button(window, width = 15, height = 2, text="Dodaj", activebackground="green") 
    buttonAdd1.grid(row = 2, column = 0, columnspan=4, sticky="S", padx="10", pady = "15")
    buttonWroc = Button(window, width = 15, height = 2, text="Wroc", activebackground="green", command=questionEditor) 
    buttonWroc.grid(row = 2, column = 1, columnspan=4, sticky="E", padx="10") 
    buttonAdd1.bind("<ButtonRelease-1>", addQuestionCd)
    entry.grid_forget()
    button.grid_forget()
    buttonAdd.grid_forget()
    button2.grid_forget()
    description.grid_forget()
    buttonEdit.grid_forget()
    buttonDel.grid_forget()
    
    
def addQuestionCd(eventObject):
     if ss.get() != "Wpisz pytanie":
        f=open("questions.txt","a")
        f.write(ss.get())
        f.write("\n")
        f.write(ans1.get())
        f.write("\n")
        f.write(ans2.get())
        f.write("\n")
        f.write(ans3.get())
        f.write("\n")
        f.write(ans4.get())
        f.write("\n")
        f.write(ansCorrect.get())
        f.write("\n")
        f.close()
        print("add")
     else:
         print("nie dodalo")
       
def showGraph():
    f=open('incorrect.txt','r+')
    lista=f.readlines()
    pytania = []
    odp = []

    for x in range(0,len(lista),2):
        pytania.append(lista[x].rstrip())
        odp.append(int(lista[x+1].rstrip()))

    print(pytania)
    data1 = {'Pytania': pytania,
             'Liczba błędnych': odp
            }
    df1 = DataFrame(data1,columns=['Pytania','Liczba błędnych'])
  
    root= tk.Tk() 
  
    figure1 = plt.Figure(figsize=(6,5), dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, root)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    df1 = df1[['Pytania','Liczba błędnych']].groupby('Pytania').sum()
    df1.plot(kind='bar', legend=True, ax=ax1)
    ax1.set_title('Pytania Vs. Liczba błędnych odpowiedzi')
    
    toolbar = NavigationToolbar2Tk(bar1, root)
    toolbar.update()
    bar1.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
     
    f.close()
    root.mainloop()

questions = []
file = open("questions.txt", "r")
line = file.readline()
while(line != ""):
    questionString = line
    answers = []
    for i in range(4):
        answers.append(file.readline())
    correctLetter = file.readline()
    correctLetter = correctLetter[:1]
    questions.append(Question(questionString, answers, correctLetter))
    line = file.readline()
file.close()
index = -1
right = 0
number_of_questions = len(questions)

window = tk.Tk(className='Python - Quiz')
window.minsize(470, 300)
window.maxsize(470, 300)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.configure(background='#02204f')
bg = PhotoImage(file = "resource\\Background2.png")
label1 = Label(window, image = bg) 
label1.place(x = 0, y = 0)
s = StringVar()
entry=Entry(window, textvariable=s, justify="center")
entry.insert(0, "Default User")
entry.grid(row=0, columnspan=4, sticky= "WE")
description = Label(window, bg="#ff6b75", width = 25, text="Wpisz swoją nazwę użytkownika: ")
description.grid(row = 0, columnspan=4, sticky= "N", pady=(90, 10))
button = Button(window, width = 15, height = 2, text="Rozpocznij", activebackground="green", command=askQuestion)
button2 = Button(window, width = 15, height = 2, text="Edytor zapytań", activebackground="green", command=questionEditor)
button.grid(row = 2, column = 0, columnspan=4, sticky="W", padx="70")
button2.grid(row = 2, column = 0, columnspan=4, sticky="E", padx="70")

window.mainloop()
