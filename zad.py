from tkinter import * 
from tkinter.ttk import * 
import requests
import json
import io
from PIL import ImageTk, Image


def fetch_nasa_images(qeury):
    url = "https://images-api.nasa.gov/search";

    params_q = {
        'q': qeury
    };

    #popierz dane
    response = requests.get(url, params=params_q);


    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'nie udalo sie poprac danych, kod błedu {response.status_code}')





#applikacja
class Application(Frame):

    window = 0;

    #
    def __init__(self):

        #otwórz okno
        self.window = Tk();

        
        #text
        label = Label(text= "hello world");
        label.pack();
        
        search = Entry();
        search.pack();

        #przycisk
        button = Button(self.window ,text="otworz", command=lambda: self.Search(search.get()));
        button.pack();

        #Główna pętla
        self.window.mainloop();

    def Search(self, text):
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

            r = 0;
            c = 0;
            

            for item in items[:5]:
                
                if(c >= 3):
                    r +=1;
                    c = 0;
                
                item_data = item.get('data',[]);

                photo = '';
                sphoto = '';
                t = '';

                if item_data:
                    title = item_data[0].get('title', "brak tytulu");
                    t = title;
                    
                links = item.get('links', [])
                if links:
                    href = links[0].get('href', 'brak linku');
                    pil_image = requests.get(href).content;
                    
                    img = Image.open(io.BytesIO(pil_image))     
                    simg = img;
                    if(img.size[0] > 700):
                        simg = Image.open(io.BytesIO(pil_image)).resize((700, img.size[1]))
                    if(img.size[1] > 700):
                        simg = Image.open(io.BytesIO(pil_image)).resize((img.size[0]), 700)

                    photo = ImageTk.PhotoImage(img);
                    sphoto = ImageTk.PhotoImage(simg);
                    
                    print(href);
                

                l_img = Button(top, image=sphoto, command=lambda: self.apearImage(photo, t));
                l_title = Label(top , text=t);


                l_img.grid(row=((r+1)*2-2), column=c, sticky=EW);
                l_title.grid(row=((r+1)*2-1), column=c, sticky=EW);

                itemImages.append(sphoto);
                itemTitles.append(t);

                c+=1;
                    
                print("-"*40)
            top.mainloop();
        except Exception as e:
            print(f"Wystapil blad {e}");
    
    def apearImage(self, image, title):
        top = Toplevel(self.window);
        l_img = Label(top , image=image);
        l_img.pack();

        l_title = Label(top , text=title);
        l_title.pack();

        top.mainloop();



        












def main():

    app = Application();



if __name__ == "__main__":
    main();
