from __future__ import annotations

import tkinter as tk
import os

from core.services.storage_service import StorageService
from core.services.affaire_service import AffaireService
from gui.accueil_view import AccueilView


def main():
    # Dossier où sont stockées les affaires JSON
    base_path = os.path.join("data", "affaires")

    # Initialisation du stockage
    storage = StorageService(base_path)

    # Service métier principal
    service = AffaireService(storage)

    # Lancement interface graphique
    root = tk.Tk()
    root.title("AffairTrack")

    AccueilView(root, service)

    root.mainloop()

if __name__ == "__main__":
    main()
