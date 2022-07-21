from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Label, StringVar
from random import randint
import datetime

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")

window = Tk()

window.geometry("1920x1080")
window.configure(bg="#000000")
window.resizable(False, False)
window.attributes("-fullscreen", True)

countdown_shutdown = False

def all_children (window) :
    _list = window.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Game:
    def start(self, players, rounds):
        self.story = {"title": None, "sentences": [], "finished": ""}
        self.data = {"players": players, "rounds": rounds, "current_round": 1, "current_player": 0}
        self.openSwapMenu(window)

    def openMainMenu(self, window):
        widget_list = all_children(window)
        for item in widget_list:
            item.pack_forget()
        MainMenu(window)

    def openSwapMenu(self, window):
        self.data["current_player"] += 1
        if self.data["current_player"] > self.data["players"]:
            self.data["current_round"] += 1
            self.data["current_player"] = 1
            if self.data["current_round"] > self.data["rounds"]:
                self.openStoryEndMenu(window)
                return

        widget_list = all_children(window)
        for item in widget_list:
            item.pack_forget()
        SwapMenu(window)

    def openIngameMenu(self, window):
        widget_list = all_children(window)
        for item in widget_list:
            item.pack_forget()
        IngameMenu(window, self.story["title"])


    def openStoryEndMenu(self, window):
        widget_list = all_children(window)
        for item in widget_list:
            item.pack_forget()
        StoryEndMenu(window)

    def openStoryReadMenu(self, window):
        widget_list = all_children(window)
        for item in widget_list:
            item.pack_forget()
        StoryReadMenu(window)

session = Game()

class MainMenu:
    def __init__(self, window):
        def popup_bonus(players, rounds, isnumber):
            win = Toplevel()
            win.wm_title("Window")

            x = window.winfo_x()
            y = window.winfo_y()
            win.geometry("+%d+%d" % (x + 500, y + 400))

            if isnumber:
                if players < 2:
                    l = Label(win, text="Es müssen mindestens zwei Spieler mitspielen.", font=("Roboto", 48 * -1))
                    l.grid(row=0, column=0)
                if rounds < 1:
                    l = Label(win, text="Es muss mindestens eine Runde gespielt werden.", font=("Roboto", 48 * -1))
                    l.grid(row=0, column=0)
            else:
                l = Label(win, text="Du darfst nur Nummern eingeben.", font=("Roboto", 48 * -1))
                l.grid(row=0, column=0)

        players, rounds = StringVar(window), StringVar(window)

        def tryandstart(players, rounds):
            try:
                players, rounds = int(players), int(rounds)
                if players >= 2 and rounds >= 1:
                    session.start(players, rounds)
                    canvas.delete('all')
                else:
                    popup_bonus(players, rounds, True)
            except ValueError:
                popup_bonus(entry_1.get(), entry_2.get(), False)

        window.bind("<Escape>", lambda event: window.destroy())
        window.bind("<Return>", lambda event: tryandstart(players.get(), rounds.get()))

        canvas = Canvas(
            window,
            bg="#000000",
            height=1080,
            width=1920,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)

        background_image = PhotoImage(
            file=relative_to_assets("background.png"))

        canvas.create_image(0, 0, image=background_image,
                            anchor="nw")

        entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            953.0,
            852.0,
            image=entry_image_1
        )
        entry_1 = Entry(
            bd=0,
            bg="#D1E6D4",
            font=("Roboto", 85 * -1),
            justify="center",
            highlightthickness=0,
            textvariable=rounds
        )
        entry_1.place(
            x=789.0,
            y=771.0,
            width=328.0,
            height=160.0
        )

        entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        entry_bg_2 = canvas.create_image(
            953.0,
            590.0,
            image=entry_image_2
        )
        entry_2 = Entry(
            bd=0,
            bg="#D1E6D4",
            font=("Roboto", 85 * -1),
            justify="center",
            highlightthickness=0,
            textvariable=players
        )
        entry_2.place(
            x=789.0,
            y=509.0,
            width=328.0,
            height=160.0
        )

        canvas.create_text(
            800.0,
            700.0,
            anchor="nw",
            text="Runden (1+)",
            fill="#E0FF68",
            font=("Roboto", 48 * -1),
            justify="right"
        )

        canvas.create_text(
            800.0,
            435.0,
            anchor="nw",
            text="Spieler (2+)",
            fill="#E0FF68",
            font=("Roboto", 48 * -1),
            justify="center"
        )

        button_1 = Button(
            bg="#f77",
            text="[ESC] Verlassen",
            font=("Roboto", 36 * -1),
            borderwidth=5,
            highlightthickness=5,
            command=lambda: window.destroy(),
            relief="flat",
        )

        button_1.place(
            x=250.0,
            y=671.0,
            width=328.0,
            height=100.0
        )

        button_2 = Button(
            bg="#7f7",
            text="[Enter] Weiter",
            font=("Roboto", 36 * -1),
            borderwidth=5,
            highlightthickness=5,
            command=lambda: tryandstart(players.get(), rounds.get()),
            relief="flat"
        )
        button_2.place(
            x=1335.0,
            y=671.0,
            width=328.0,
            height=100.0
        )

        canvas.create_text(
            150.0,
            178.0,
            anchor="nw",
            text="Das Spielprinzip ist einfach. Der Spieler, der an der Reihe ist, darf den Bildschirm sehen.\n"
                 "Alle anderen Spieler müssen sich umdrehen. Jeder Spieler sieht nur den Titel und den\n"
                 "Satz, den der Spieler vor ihm geschrieben hat. Er hat 60 Sekunden um den nächsten Satz\n"
                 "zu schreiben. Am Ende wird ein zufälliger Spieler ausgewählt, der die Geschichte\n"
                 "vorlesen muss.",
            fill="#68FFF5",
            font=("Roboto", 36 * -1),
            justify="center"
        )

        canvas.create_text(
            485.0,
            956.0,
            anchor="nw",
            text="Jeder Spieler ist in jeder Runde einmal an der Reihe!",
            fill="#FF7A7A",
            font=("Roboto Bold", 36 * -1),
            justify="center"
        )

        canvas.create_text(
            600.0,
            100.0,
            anchor="nw",
            text="Willkommen bei SwapStory!",
            fill="#68FF89",
            font=("Roboto", 48 * -1),
            justify="center"
        )

        window.mainloop()

class SwapMenu:
    def __init__(self, window):
        window.bind("<Escape>", lambda event: session.openStoryEndMenu(window))
        window.bind("<Return>", lambda event: session.openIngameMenu(window))

        canvas = Canvas(
            window,
            bg="#000000",
            height=1080,
            width=1920,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)

        background_image = PhotoImage(
            file=relative_to_assets("background.png"))

        canvas.create_image(0, 0, image=background_image,
                            anchor="nw")

        button_1 = Button(
            bg="#f77",
            text="[ESC] Verlassen",
            font=("Roboto", 36 * -1),
            borderwidth=5,
            highlightthickness=5,
            command=lambda: session.openStoryEndMenu(window),
            relief="flat",
        )
        button_1.place(
            x=468.0,
            y=669.0,
            width=328.0,
            height=100.0
        )

        button_2 = Button(
            bg="#7f7",
            text="[Enter] Weiter",
            font=("Roboto", 36 * -1),
            borderwidth=5,
            highlightthickness=5,
            command=lambda: session.openIngameMenu(window),
            relief="flat",
        )
        button_2.place(
            x=1124.0,
            y=669.0,
            width=328.0,
            height=100.0
        )

        canvas.create_text(
            575.0,
            451.0,
            anchor="nw",
            text="Wir sind in der " + str(session.data["current_round"]) + ". von insgesamt " + str(session.data["rounds"]) + " Runden",
            fill="#E0FF68",
            font=("Roboto", 36 * -1),
            justify="center"
        )

        canvas.create_text(
            253.0,
            361.0,
            anchor="nw",
            text="Die Tastatur wird zum " + str(session.data["current_player"]) + ". mal von insgesamt " + str(session.data["players"]) + " mal in dieser Runde weitergegeben.",
            fill="#E0FF68",
            font=("Roboto", 36 * -1),
            justify="center"
        )

        canvas.create_text(
            720.0,
            281.0,
            anchor="nw",
            text="Spieler " + str(session.data["current_player"]) + " ist an der Reihe.",
            fill="#68FF89",
            font=("Roboto", 36 * -1),
            justify="center"
        )

        window.mainloop()

class IngameMenu:
    def __init__(self, window, title):
        countdown_timer = StringVar(window)

        def button_countdown(i, label):
            global countdown_shutdown
            if countdown_shutdown:
                countdown_shutdown = False
                return
            if i > 0:
                i -= 1
                label.set(i)
                window.after(1000, lambda: button_countdown(i, label))
            else:
                saveandopen()

        def tryandopen():
            now = entry_1.get("1.0", 'end-1c')
            if len(now) > 0:
                saveandopen()

        def saveandopen():
            global countdown_shutdown
            countdown_shutdown = True
            done = ""
            count = 0
            for i in entry_1.get("1.0", 'end-2c'):
                count += 1
                if count == 64:
                    done += "\n" + i
                    count = 0
                else:
                    done += i
            if title is None:
                session.story["title"] = done
            else:
                session.story["sentences"].append(done)
            session.openSwapMenu(window)

        window.bind("<Escape>", lambda event: session.openStoryEndMenu(window))
        window.bind("<Return>", lambda event: tryandopen())

        canvas = Canvas(
            window,
            bg="#000000",
            height=1080,
            width=1920,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)

        background_image = PhotoImage(
            file=relative_to_assets("background.png"))

        canvas.create_image(0, 0, image=background_image,
                            anchor="nw")

        entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            959.5,
            730.5,
            image=entry_image_1
        )
        entry_1 = Text(
            bd=0,
            bg="#D1E6D4",
            font=("Roboto", 36 * -1),
            highlightthickness=0,

        )
        entry_1.place(
            x=249.0,
            y=643.0,
            width=1421.0,
            height=173.0
        )

        entry_1.focus()

        canvas.create_text(
            242.0,
            100.0,
            anchor="nw",
            text="Du bist Spieler " + str(session.data["current_player"]) + ". Du musst dir diese Nummer merken.",
            fill="#68FF89",
            font=("Roboto", 36 * -1),
            justify="center"
        )

        button_1 = Button(
            bg="#f77",
            text="[ESC] Verlassen",
            font=("Roboto", 36 * -1),
            borderwidth=5,
            highlightthickness=5,
            command=lambda: session.openStoryEndMenu(window),
            relief="flat",
        )
        button_1.place(
            x=468.0,
            y=867.0,
            width=328.0,
            height=100.0
        )

        button_2 = Button(
            bg="#7f7",
            text="[Enter] Weiter",
            font=("Roboto", 36 * -1),
            borderwidth=5,
            highlightthickness=5,
            command=lambda: tryandopen(),
            relief="flat",
        )
        button_2.place(
            x=1124.0,
            y=867.0,
            width=328.0,
            height=100.0
        )


        button_3 = Button(
            bg="#77f",
            textvariable=countdown_timer,
            font=("Roboto", 36 * -1),
            borderwidth=5,
            relief="flat",
        )
        button_3.place(
            x=796.0,
            y=867.0,
            width=328.0,
            height=100.0
        )

        button_countdown(60, countdown_timer)

        if title is None:
            canvas.create_text(
                249.0,
                559.0,
                anchor="nw",
                text="Die Geschichte braucht einen Titel. Denke dir einen aus. (Max. 1 Zeile)",
                fill="#E0FF68",
                font=("Roboto", 36 * -1),
                justify="center"
            )

        else:
            canvas.create_text(
                249.0,
                559.0,
                anchor="nw",
                text="Denke dir den nächsten Satz aus. (Max. 2 Zeilen)",
                fill="#E0FF68",
                font=("Roboto", 36 * -1),
                justify="center"

            )

            if len(session.story["sentences"]) > 0:
                canvas.create_text(
                    249.0,
                    300.0,
                    anchor="nw",
                    text='Der letzte Satz ist:\n"' + str(session.story["sentences"][-1]) + '".',
                    fill="#68FFF5",
                    font=("Roboto", 36 * -1),
                    justify="center"
                )

            canvas.create_text(
                246.0,
                165.0,
                anchor="nw",
                text='Die Geschichte heißt:\n"' + str(session.story["title"]) +'".',
                fill="#68FFF5",
                font=("Roboto", 36 * -1),
                justify="center"
            )

        window.mainloop()

class StoryEndMenu:
    def __init__(self, window):
        story = '"' + str(session.story["title"]).replace("\n", "") + '" - Eine Geschichte von ' + str(
            session.data["players"]) + ' Spielern.\n'

        for i in session.story["sentences"]:
            print(i)

            first = i.split("\n")
            count = 0
            donei = ""
            for i in first:
                count += 1
                if count == 3:
                    donei += i + "\n"
                    count = 0
                else:
                    donei += i

            story += "".join([s for s in donei.strip().splitlines(True) if s.strip()]) + "\n"

        safe = str(str(session.story["title"]).replace("\n", "").replace("<", "").replace(">", "").replace("*", "")
              .replace(":", "").replace('"', "").replace("/", "").replace("\\", "").replace("|", "").replace("?", ""))

        try:
            open("Geschichten/{} - {}.txt".format(safe, str(datetime.datetime.now()).split(".")[0].replace(":", "_")),
                 "w+").write(str(story))
        except OSError:
            open("Geschichten/{} - {}.txt".format("Story Name Too Long", str(datetime.datetime.now()).split(".")[0].replace(":", "_")),
                 "w+").write(str(story))

        session.story["finished"] = story

        canvas = Canvas(
            window,
            bg="#000000",
            height=1080,
            width=1920,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        window.bind("<Return>", lambda event: 0)
        window.bind("<Escape>", lambda event: 0)

        canvas.place(x=0, y=0)

        background_image = PhotoImage(
            file=relative_to_assets("background.png"))

        canvas.create_image(0, 0, image=background_image,
                            anchor="nw")

        chosen_player = StringVar(window)
        chosen_player.set("Spieler ?")

        def countdown(i, label):
            if i == 0:
                canvas.create_text(
                    425.0,
                    100.0,
                    anchor="nw",
                    text="Alle Spieler müssen sich zum Bildschirm drehen.\nEin zufälliger Spieler wird jetzt ausgewählt.",
                    fill="#68FF89",
                    font=("Roboto", 48 * -1),
                    justify="center"
                )
                window.after(5000, lambda: countdown(i, label))
                i += 1

            elif 0 < i < 50:
                label.set("Spieler " + str(randint(1, session.data["players"])))
                i += 1
                window.after(100 + i, lambda: countdown(i, label))

            elif i >= 50:
                canvas.create_text(
                    650.0,
                    700.0,
                    anchor="nw",
                    text=str(label.get()) + " muss die Geschichte vorlesen.",
                    fill="#E0FF68",
                    font=("Roboto", 32 * -1),
                    justify="right"
                )
                window.after(500, lambda: ready_btn())
        def ready_btn():
            window.bind("<Return>", lambda event: session.openStoryReadMenu(window))
            button_3 = Button(
                bg="#7f7",
                text="[Enter] Bereit",
                font=("Roboto", 36 * -1),
                borderwidth=5,
                command=lambda: session.openStoryReadMenu(window),
                relief="flat",
            )
            button_3.place(
                x=800.0,
                y=900.0,
                width=328.0,
                height=100.0
            )

        button_3 = Button(
            bg="#77f",
            textvariable=chosen_player,
            font=("Roboto", 36 * -1),
            borderwidth=5,
            relief="flat",
        )
        button_3.place(
            x=800.0,
            y=435.0,
            width=328.0,
            height=100.0
        )

        countdown(0, chosen_player)
        window.mainloop()

class StoryReadMenu:
    def __init__(self, window):
        story = session.story["finished"]

        canvas = Canvas(
            window,
            bg="#000000",
            height=1080,
            width=1920,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)

        background_image = PhotoImage(
            file=relative_to_assets("background.png"))

        canvas.create_image(0, 0, image=background_image,
                            anchor="nw")

        chosen_player = StringVar(window)
        chosen_player.set("Spieler ?")

        window.bind("<Escape>", lambda event: session.openMainMenu(window))
        window.bind("<Return>", lambda event: session.openMainMenu(window))

        button_3 = Button(
            bg="#7f7",
            text="[Enter] Zum Menü",
            font=("Roboto", 36 * -1),
            borderwidth=5,
            command=lambda: session.openStoryReadMenu(window),
            relief="flat",
        )
        button_3.place(
            x=800.0,
            y=950.0,
            width=328.0,
            height=100.0
        )

        canvas.create_text(
            50.0,
            50.0,
            anchor="nw",
            text=str(story),
            fill="#68FFF5",
            font=("Roboto", 22 * -1),
            justify="center"
        )

        window.mainloop()

MainMenu(window)