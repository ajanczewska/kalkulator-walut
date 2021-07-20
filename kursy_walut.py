import tkinter as tk
import tkinter.ttk as ttk
import  urllib.request
import xmltodict

try:
    resource = urllib.request.urlopen("https://api.nbp.pl/api/exchangerates/tables/a?format=xml")
    content = resource.read()
    xmlFile = 'kursy_walut.xml' 
    with open(xmlFile, 'b+w') as openXml:
        openXml.write(content)
        openXml.close()
except urllib.error.URLError:
    xmlFile = 'kursy_walut.xml' 

    
with open(xmlFile, encoding='utf-8') as fd:
    kursy = {}
    kursy[('polski złoty', 'PLN')] = 1
    doc = xmltodict.parse(fd.read())
    for x in range(len(doc['ArrayOfExchangeRatesTable']['ExchangeRatesTable']['Rates']['Rate'])):
        currency = doc['ArrayOfExchangeRatesTable']['ExchangeRatesTable']['Rates']['Rate'][x]['Currency']
        code = doc['ArrayOfExchangeRatesTable']['ExchangeRatesTable']['Rates']['Rate'][x]['Code']
        mid = doc['ArrayOfExchangeRatesTable']['ExchangeRatesTable']['Rates']['Rate'][x]['Mid']
        kursy[(currency, code)] = mid
    fd.close()

class Aplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Przelicznik kursów walut')
        self.master.geometry('725x500')
        self.pack()
        self.craeted_comboboxes()
        self.created_entry()
        self.created_labels()
        self.created_button_count()
        self.created_button_quit()

    def created_labels(self):
        self.label = tk.Label(root, text='Wybierz walutę źródłową', font=('bold'))
        self.label.pack()
        self.label.place(x=80, y=20)

        self.label_doc = tk.Label(root, text='Wybierz walutę docelową',font=('bold'))
        self.label_doc.pack()
        self.label_doc.place(x=80, y=120)

        self.label_waluta = tk.Label(root, text='', font=('Arial', 8, 'italic'))
        self.label_waluta.pack()
        self.label_waluta.place(x=80, y=75)

        self.label_waluta_doc = tk.Label(root, text='', font=('Arial', 8, 'italic'))
        self.label_waluta_doc.pack()
        self.label_waluta_doc.place(x=80, y=175)

        self.label_liczba = tk.Label(root, text='', font=('Arial', 8, 'italic'))
        self.label_liczba.pack()
        self.label_liczba.place(x=80, y=265)

        self.wynikLabel = tk.Label(root)
        self.wynikLabel.pack()
        self.wynikLabel.place(x=80, y=350)


    def craeted_comboboxes(self):
        self.labelDescription = tk.StringVar()
        self.combobox = ttk.Combobox(root, textvariable=self.labelDescription, width=40, state='readonly', values=self.kursy_walut())
        self.combobox.pack()
        self.combobox.place(x=80, y=50)
        self.combobox.current()

        self.labelDescription_doc = tk.StringVar()    
        self.combobox_doc = ttk.Combobox(root, textvariable=self.labelDescription_doc, width=40, state='readonly', values=self.kursy_walut())
        self.combobox_doc.pack()
        self.combobox_doc.place(x=80, y=150)
        self.combobox_doc.current()
        
    def created_entry(self):
        self.entryDescription = tk.StringVar()
        self.descriptionEntry = tk.Label(root, textvariable=self.entryDescription, font=('bold'))
        self.entryDescription.set('Wprowadź kwotę')
        self.descriptionEntry.pack()
        self.descriptionEntry.place(x=80, y=210)

        self.textField = tk.Entry(root, width=40)
        self.textField.place(x=80, y=240)

    def created_button_count(self):
        self.bn = tk.Button(text='OBLICZ', font=('Roboto', 12, 'bold'), foreground='#0B2754', background='#CFDCF2')
        self.bn.pack()
        self.bn.place(x=80, y=290)
        self.bn.bind('<Button-1>', self.buttonClick)

    def created_button_quit(self):
        self.bn_quit = tk.Button(text='ZAKOŃCZ', command=root.quit, font=('Roboto', 8, 'bold'), foreground='#F02420', background='#CEC9C9')
        self.bn_quit.pack()
        self.bn_quit.place(x=80, y=410)
        

    def kursy_walut(self):
        kursy_walut_keys = []
        for (k, v) in kursy.items():
            kurs = k[0]
            kursy_walut_keys.append(kurs + ', ' + k[1])
        return kursy_walut_keys
        
    def buttonClick(self, event):
        self.bn.config(font=('Roboto', 12, 'bold'), foreground='#0B2754', background='#CFDCF2')
        self.wynikLabel.config(text='')
        value = self.textField.get()
        waluta = self.combobox.get()
        waluta_doc = self.combobox_doc.get()
        try:
            value = float(value)
            if waluta == '':
                self.label_waluta.config(text="Wybierz walutę!", foreground='red')
            else:
                self.label_waluta.config(text='')

            if waluta_doc == '':
                self.label_waluta_doc.config(text="Wybierz walutę!", foreground='red')
            else:
                self.label_waluta_doc.config(text='')

            if round(value, 2) != value or value <= 0:
                self.textField.config(background='#FAADAD')
                self.label_liczba.config(text="Liczba może mieć tylko 2 miejsca po przecinku, musi być większa od zera!", foreground='red')
            else:
                self.textField.config(background='white')
                self.label_liczba.config(text='')

            if (waluta != '') & (waluta_doc != '') & (round(value, 2) == value) & (value > 0):
                #zamieniamy string na krotkę, która jest kluczem w kursy
                kurs = kursy[waluta.split(',')[0], waluta.split(', ')[1]]
                kurs_doc = kursy[waluta_doc.split(',')[0], waluta_doc.split(', ')[1]]
                self.wynik = round((float(kurs)/float(kurs_doc))*value, 2)
                self.wynikLabel.config(text="Kwota wynosi: " + str(self.wynik) + " " + waluta_doc.split(', ')[1], foreground='green', font=('Roboto', 20, 'bold'))
                
        except ValueError:
            self.textField.config(background='#FAADAD')
            self.label_liczba.config(text="W tym polu należy wpisać liczbę!", foreground='red')
            if waluta == '':
                self.label_waluta.config(text="Wybierz walutę!", foreground='red')
            else:
                self.label_waluta.config(text='')
                
            if waluta_doc == '':
                self.label_waluta_doc.config(text="Wybierz walutę!", foreground='red')
            else:
                self.label_waluta_doc.config(text='')

root = tk.Tk()
app = Aplication(master=root)
app.mainloop()
