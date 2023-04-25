import os, sys
from sylvaBrain import *
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
from sylvaBrain import *

class SylvaGUI:
    def __init__(self):
        self.background_color = '#385569'
        self.textbox_color = '#496b82'
        self.sentiment = Sentiment.neutral

        self.root = tk.Tk()
        self.root.resizable(False,False)
        self.root.title("Sylva")
        self.root.config(background=self.background_color)

        # Create avatar for Sylva
        self.avatar = ImageTk.PhotoImage(Image.open(os.path.join(sys.path[0],'pfp','neutral.png')).resize((512,512)))
        self.avatar_label = tk.Label(self.root,image=self.avatar, background=self.background_color)
        self.avatar_label.pack(side='top')

        self.status = tk.StringVar()
        self.info = tk.Label(self.root, bg=self.textbox_color, height=20,width=65,textvariable=self.status,justify="left", anchor="nw",wraplength=450)
        self.info.pack(side='top')

    def run(self):
        self.root.after(10000,self.think)          
        self.root.mainloop()

    def think(self):
        self.findNextQuestion()
        self.root.after(10000,self.think)

    def updateSentiment(self, sentiment:str):
        print(os.path.join(sys.path[0],'pfp',sentiment+'.png'))
        self.avatar = ImageTk.PhotoImage(Image.open(os.path.join(sys.path[0],'pfp',sentiment+'.png')).resize((512,512)))
        self.avatar_label.configure(image=self.avatar)

    def updateStatus(self, answer):
        self.status.set(answer)

    def findNextQuestion(self):
        try:
            sqliteConnection = sqlite3.connect(os.path.join(sys.path[0],'instance','sylva.sqlite'))
            cursor = sqliteConnection.cursor()

            res = cursor.execute('SELECT id, content, author_id FROM query WHERE answered=0 ORDER BY created')
            fetch = res.fetchone()

            if(fetch):
                res = cursor.execute('select username FROM user WHERE id=?',(fetch[2],))
                username = res.fetchone()
                [ans,sentiment] = self.processFetch(fetch,username[0])
                
                update = "UPDATE query SET answered=1, answer=? WHERE id=?"
                res=cursor.execute(update,(ans,str(fetch[0]),))
                sqliteConnection.commit()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def processFetch(self,fetch,username):
        ans = Sylva().respond(username,fetch[1])
        sentiment = Sylva().sentimentAnalysis(ans)
        self.updateSentiment(sentiment)
        self.updateStatus(ans)
        self.root.update()
        print(sentiment)
        Sylva().synthesize_text(ans)
        return [ans,sentiment]


    def exitSylva(self):
        self.root.destroy()


if __name__ == "__main__":
    myGUI = SylvaGUI()
    myGUI.run()