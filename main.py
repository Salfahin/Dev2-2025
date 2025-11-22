import tkinter as tk
from gui.accueil import accueil

def main():
    fenetre = tk.Tk()
    fenetre.title("AffairTrack")
    fenetre.geometry("650x700")

    accueil(fenetre)

    fenetre.mainloop()


if __name__ == "__main__":
    main()