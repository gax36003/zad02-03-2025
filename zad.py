from tkinter import * 
from tkinter.ttk import * 
import requests
import json
import io
from PIL import ImageTk, Image


def fetch_nasa_images(qeury):
    #link z którego są pobierane dane
    url = "https://images-api.nasa.gov/search";

    #parametry
    params_q = {
        'q': qeury
    };

    #popierz dane
    response = requests.get(url, params=params_q);

    #sprawdź czy pobranie danych działa
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'nie udalo sie poprac danych, kod błedu {response.status_code}')


#applikacja
class Application(Frame):
    #utworzenie zmiennej
    window = 0;

    #inicjalizacja klasy
    def __init__(self):

        #otwórz okno
        self.window = Tk();

        
        #text
        label = Label(text= "hello world");
        label.pack();
        
        search = Entry();
        search.pack();

        #przycisk do wyszukiwania
        button = Button(self.window ,text="otworz", command=lambda: self.Search(search.get()));
        button.pack();

        #Główna pętla window
        self.window.mainloop();

    def Search(self, text):
        #utwórz następne okno
        top = Toplevel(self.window);

        try:
            data = fetch_nasa_images(text);
            # print(data)
            items = data.get('collection', {}).get('items', []);
            # print(items)

            if not items:
                print("Brak wyników wyszukiwania");
                return # slowko skoku, ktore konczy dzialanie metody/funkcji
            #print(items)

            itemImages = [];
            itemTitles = [];

            #utwórz zmienne kolumny i wierszy dla obrazów
            r = 0;
            c = 0;
            
            #pętla która wyszukiwuje czy są obrazy
            for item in items[:5]:
                
                #sprawdź czy to następny wiersz
                if(c >= 3):
                    r +=1;
                    c = 0;
                
                item_data = item.get('data',[]);

                #utwórz zmienne obrazów i tytółu elementu
                photo = '';
                small_photo = '';
                t = '';

                #sprawdź czy 'data' istnieje
                if item_data:
                    title = item_data[0].get('title', "brak tytulu");
                    t = title;
                    
                links = item.get('links', [])
                if links:
                    href = links[0].get('href', 'brak linku');
                    pil_image = requests.get(href).content;
                    
                    #większa i mniejsza wersja obrazu
                    img = Image.open(io.BytesIO(pil_image))     
                    small_img = img;
                    
                    #obraz jest zmniejszany gdy jest za duży
                    if(img.size[0] > 700):
                        small_img = Image.open(io.BytesIO(pil_image)).resize((700, img.size[1]))
                    if(img.size[1] > 700):
                        small_img = Image.open(io.BytesIO(pil_image)).resize((img.size[0]), 700)

                    photo = ImageTk.PhotoImage(img);
                    small_photo = ImageTk.PhotoImage(small_img);
                    
                    #wyświetla linki do obrazów
                    print(href);
                    print("-"*40)
                
                #obrazy są jako przyciski. Wywołują metodę ApearImage
                l_img = Button(top, image=small_photo, command=lambda: self.ApearImage(photo, t));
                l_title = Label(top , text=t);

                #obrazy i tytuł zostają wywołane jako tabela dla lepszej widoczności
                l_img.grid(row=((r+1)*2-2), column=c, sticky=EW);
                l_title.grid(row=((r+1)*2-1), column=c, sticky=EW);

                itemImages.append(small_photo);
                itemTitles.append(t);

                #zwiększ kolumnę o jeden
                c+=1;
                    
            #Główna pętla top
            top.mainloop();
        #gdy nastąpi bład wyświetla się w konsoli "Wystapil blad"
        except Exception as e:
            print(f"Wystapil blad {e}");
    
    #pokacują się obrazy na osobnym oknie.
    def ApearImage(self, image, title):
        #utwórz następne okno
        top = Toplevel(self.window);

        l_img = Label(top , image=image);
        l_img.pack();

        l_title = Label(top , text=title);
        l_title.pack();

        #Główna pętla top
        top.mainloop();


def main():
    app = Application();


if __name__ == "__main__":
    main();
