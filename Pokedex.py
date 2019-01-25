from Tkinter import *
from bs4 import BeautifulSoup
import urllib2
import ttk
import shelve
import os
from io import BytesIO
import urllib
from PIL import Image, ImageTk
import time

class Fetching():
    def pokemon_names_from_excel(self):
        with open('all_pokemon.txt', 'r') as f:
            self.list_pokemon = [line.strip() for line in f]
        # print self.list_pokemon
        self.fetching_data()
#------------------------------FETCHING DATA FROM WEBSITE OR IF WE HAVE DATA BASE FETCHING FROM DATA BASE------------------------
    def fetching_data(self):
        if os.path.exists("pokemon_database.db"):
            self.s = shelve.open('pokemon_database.db')
            self.progress_bar.create_rectangle(0, 0, 210, 25, fill="green")
            self.progress_bar.create_text(100, 13, fill="darkblue",
                                          text="Finished")
            print 'exist'
        else:
            print 'not exist'
            self.s = shelve.open('pokemon_database.db')
            self.dict = {}
            self.progress=0
              # progress size for each iteration
            for pokemon in range(len(self.list_pokemon)):
                self.progress+=1.5
                self.progress_bar.create_rectangle(0, 0, self.progress, 25,
                                                   fill="green")  # 0,0 = sol ust , 0,0 = sag alt
                self.root.update_idletasks()  # update the frame

                time.sleep(0.04)


                list_of_attr = []
                response = urllib2.urlopen("https://www.pokemon.com/us/pokedex/" + self.list_pokemon[pokemon])
                html_doc = response.read()
                # print html_doc
                soup = BeautifulSoup(html_doc, 'html.parser')
                # ---------------POKEMON'S NAME -------------------------------
                x = soup.title.string
                y = x.split('|')
                print y[0]
                # ---------------FINDING ID-----------------------------------
                find_id = soup.find_all("span", attrs={"class": "pokemon-number"})
                id = find_id[2]
                pokemon_id = id.text
                #----------------FINDING TYPE---------------------------------
                x = soup.find_all("div", attrs={"class": "pokedex-pokemon-attributes active"})
                # print x
                for i in x:
                    self.type = i.a.text
                # --------------FINDING PICTURE OF POKEMON
                denem = soup.find_all('section', attrs={'class': 'section pokedex-pokemon-details'})
                for i in denem:
                    self.link_of_photo = (i.img.get('src'))
                # ----------------FINDING ATTRIBUTES FOR EACH POKEMON----------
                find_attributes = soup.find_all(class_="attribute-value")
                for i in range(len(find_attributes)):
                    # print find_attributes[i].text
                    self.height = find_attributes[0].text
                    self.Category = find_attributes[3].text
                    self.Weight = find_attributes[1].text
                    self.Abilities = find_attributes[4].text
                #---------FINDING WEAKNESS-----------------------
                find_weakness = soup.find_all('div', attrs={'class': 'dtm-weaknesses'})
                for weakness in find_weakness:
                    self.weakness=weakness.a.text
                # print self.weakness
                list_of_attr.append(pokemon_id) # index 0
                list_of_attr.append(self.height) # index 1
                list_of_attr.append(self.Category) # index 2
                list_of_attr.append(self.Weight) # index 3
                list_of_attr.append(self.Abilities) # index 4
                list_of_attr.append(self.type) # index 5
                list_of_attr.append(self.link_of_photo) #index 6
                list_of_attr.append(self.weakness) #index7
                self.list_pokemon[pokemon] = self.list_pokemon[pokemon].upper()
                # self.dict[self.pokemon_names_list[pokemon]] = list_of_attr
                self.s[self.list_pokemon[pokemon]] = list_of_attr
        print self.s

        self.progress_bar.create_text(100, 13, fill="darkblue",
                                      text="Finished")
        # print self.s['IVYSAUR']
        #-------------------------CREATING TYPE LIST------------------------------
        self.type_list = ['All Types']
        for i,j in self.s.iteritems():
            if self.s[i][5] in self.type_list:
                continue
            else:
                self.type_list.append(self.s[i][5])
        print self.type_list
        self.combobox['values'] = self.type_list
        self.combobox.current(0)
    def searching_and_filtering(self): #-------------------SEARCHING AND FILTERING PART----------------------------
        self.listbox.delete(0,END)
        self.result_list=[]
        self.search_parameter=self.pokeentry.get()
        print self.search_parameter
        if self.search_parameter=='' or self.search_parameter==' ':
            print 'Please Fill the Enter Bar'
        else:
            self.search_parameter=self.search_parameter.upper()
            self.combobox_get=self.combobox.get()
            print "aradigim sey: "+ self.search_parameter
            for i in self.s.keys():
                if self.search_parameter in i:
                    if self.combobox_get=='All Types':
                        # print 'dogru'
                        self.result_list.append(i)
                    if self.combobox_get not in self.s[i]:
                        pass
                    else:
                        # print i
                        # print self.s[i]
                        self.result_list.append(i)

            print self.result_list
            self.labelTot = Label(self.frame_4, text='Total : ' + str(len((self.result_list))) + ' Result', fg='black',
                                  font='Helvetica 18 bold',
                                  bg='red')
            self.labelTot.grid(row=0, column=3)
            self.labelTotal.grid_remove()

            for j in self.result_list:
                self.listbox.insert(END,j)
    def get_pok_data(self):#####-------CREATING NEW FRAME AND SHOWING POKEMON DATAS*-------------------------
        #------------------COLOR DICTIONARY FOR TYPE COLORING-----------------------------------


        self.colordict={'Grass':'green3','Poison':'purple','Fire':'dark orange','Water':'RoyalBlue3',
                        'Bug':'dark green','Normal':'ivory4','Electric':'yellow','Ground':'DarkOrange4',
                        'Fairy':'HotPink1','Fighting':'OrangeRed2','Psychic':'deep pink','Ghost':'dark violet'
                        ,'Rock':'dark goldenrod','Ice':'sky blue','Dragon':'firebrick4'}
        for item in self.listbox.curselection():
            self.choosen_name=self.listbox.get(item)
        print self.s[self.choosen_name][0]
        self.frame_5 = Frame(bg='red', borderwidth=5, highlightbackground="black", highlightthickness=2)
        for r in range(12):
            self.frame_5.rowconfigure(r, weight=1)
        for c in range(10):
            self.frame_5.columnconfigure(c, weight=1)
        self.link_of_photo = self.s[self.choosen_name]
        self.pokemon_name_label=Label(self.frame_5,text=self.choosen_name,bg='red',font=("Helvetica", 16))
        self.pokemon_name_label.grid()

        self.pokemon_id_label=Label(self.frame_5,text=self.s[self.choosen_name][0],bg='red',font=("Helvetica", 16))
        self.pokemon_id_label.grid()

        self.frame_5.grid(row=0, column=16, rowspan=7, sticky=W + E + N + S, columnspan=15)

        url = self.s[self.choosen_name][6]
        self.u = urllib.urlopen(url)
        raw_data = self.u.read()
        self.u.close()
        print self.link_of_photo
        self.im = Image.open(BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(self.im)
        label = Label(self.frame_5,image=self.image,bg='red')
        label.grid()

        self.pokemon_type_label = Label(self.frame_5, text=self.s[self.choosen_name][5],bg=self.colordict[self.s[self.choosen_name][5]],font=("Helvetica", 16))
        self.pokemon_type_label.grid()

        self.pokemon_height_label = Label(self.frame_5, text=self.s[self.choosen_name][1],bg='red',font=("Helvetica", 16))
        self.pokemon_height_label.grid()

        self.pokemon_weight_label = Label(self.frame_5, text=self.s[self.choosen_name][3],bg='red',font=("Helvetica", 16))
        self.pokemon_weight_label.grid()

        self.pokemon_category_label = Label(self.frame_5, text=self.s[self.choosen_name][2],bg='red',font=("Helvetica", 16))
        self.pokemon_category_label.grid()

        self.pokemon_ability_label = Label(self.frame_5, text=self.s[self.choosen_name][4],bg='red',font=("Helvetica", 16))
        self.pokemon_ability_label.grid()

        self.pokemon_weakness_label=Label(self.frame_5, text=self.s[self.choosen_name][7],bg='red',font=("Helvetica", 16))
        self.pokemon_weakness_label.grid()
class myGUI(Frame, Fetching):  #############GUI CLASS
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.root=parent
        for r in range(7):
            parent.rowconfigure(r, weight=1)
        for c in range(15):
            parent.columnconfigure(c, weight=1)
        self.initUI()

    def initUI(self):
        # Frame1
        self.frame_1 = Frame(bg='red', highlightbackground="black", highlightthickness=2)
        for r in range(12):
            self.frame_1.rowconfigure(r, weight=1)
        for c in range(10):
            self.frame_1.columnconfigure(c, weight=1)
        self.label = Label(self.frame_1, text='POKEDEX', fg='white', font='Helvetica 18 bold', bg='red')
        self.label.grid(row=4, column=5, sticky=W + E + N + S)
        self.frame_1.grid(row=0, column=0, rowspan=1, sticky=W + E + N + S, columnspan=15)

        # FRAME2
        self.frame_2 = Frame(bg='red', highlightbackground="black", highlightthickness=2)
        for r in range(12):
            self.frame_2.rowconfigure(r, weight=1)
        for c in range(10):
            self.frame_2.columnconfigure(c, weight=1)
        self.buttonfetch_data = Button(self.frame_2, bg='yellow', fg='black', height=2, width=13,
                                       text='Fetch Pokemon\nData', command=self.pokemon_names_from_excel)
        self.buttonfetch_data.grid(row=5)
        self.progress_bar = Canvas(self.frame_2, bg='white', width=200, height=20, borderwidth=2)
        self.progress_bar.grid(row=5, column=3)
        self.frame_2.grid(row=1, column=0, rowspan=1, sticky=W + E + N + S, columnspan=15)
        # FRAME 3
        self.frame_3 = Frame(bg='red', highlightbackground="black", highlightthickness=2)
        for r in range(12):
            self.frame_3.rowconfigure(r, weight=1)
        for c in range(10):
            self.frame_3.columnconfigure(c, weight=1)
        self.label_search_and_filter = Label(self.frame_3, text='Searching&Filtering', fg='black',
                                             font='Helvetica 18 bold', bg='red')
        self.label_search_and_filter.grid(column=3)
        self.pokeentry = Entry(self.frame_3, width=50, relief='sunken')
        self.pokeentry.grid(row=1, column=3)
        self.label_filter_by_type = Label(self.frame_3, text='Filter by type', fg='black', bg='red',font=("Helvetica", 16))
        self.label_filter_by_type.grid(row=3, column=2)
        self.combobox = ttk.Combobox(self.frame_3, width=40)
        self.combobox.grid(row=5, column=2)
        self.button_search = Button(self.frame_3, bg='yellow', fg='black', height=1, width=17, text='Search',command=self.searching_and_filtering)
        self.button_search.grid(row=5, column=6)
        self.frame_3.grid(row=2, column=0, rowspan=1, sticky=W + E + N + S, columnspan=15)
        # FRAME 4
        self.frame_4 = Frame(bg='red', highlightbackground="black", highlightthickness=2)
        for r in range(12):
            self.frame_4.rowconfigure(r, weight=1)
        for c in range(10):
            self.frame_4.columnconfigure(c, weight=1)

        self.labelTotal = Label(self.frame_4, text='Total number of result', fg='black', font='Helvetica 18 bold',
                                bg='red')
        self.labelTotal.grid(row=0, column=3)

        self.listbox = Listbox(self.frame_4, width=40)
        self.listbox.grid(row=2, column=0, rowspan=5)

        self.button_getpokemondata = Button(self.frame_4, bg='yellow', fg='black', height=2, width=17,
                                            text='Get Pokemon\nData',command=self.get_pok_data)
        self.button_getpokemondata.grid(row=5, column=5)

        self.frame_4.grid(row=3, column=0, rowspan=4, sticky=W + E + N + S, columnspan=15)
def main():
    root = Tk()
    root.title('tk')
    root.geometry()
    app = myGUI(root)
    # app.pack(fill=BOTH, expand=True)
    root.mainloop()


main()
