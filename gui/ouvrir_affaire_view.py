from __future__ import annotations
from gui.theme import *

import tkinter as tk
from tkinter import messagebox
from typing import Optional, Callable

from core.models.affaire import Affaire
from core.services.affaire_service import AffaireService
from gui.modifier_affaire_view import ModifierAffaireView


class OuvrirAffaireView:
    """
    Popup affichant le détail complet d'une affaire.
    """

    def __init__(self, root: tk.Tk, service: AffaireService,
                 affaire: Affaire, on_done: Optional[Callable] = None):

        self.root = root
        self.service = service
        self.affaire = affaire
        self.on_done = on_done

        self.build()

    # ---------------------------------------------------------
    #   CONSTRUCTION DE LA POPUP
    # ---------------------------------------------------------
    def build(self):
        # Popup Toplevel
        self.popup = tk.Toplevel(self.root)
        self.popup.title(self.affaire.titre)
        self.popup.geometry("750x650")

        # Barre supérieure
        top = tk.Frame(self.popup, bg="#f8f8f8")
        top.pack(fill="x")

        tk.Label(
            top,
            text=self.affaire.titre,
            font=TITLE_FONT,
            bg=BG_MAIN
        ).pack(side="left", padx=15, pady=10)

        tk.Button(
            top,
            text="Modifier ✎",
            font=BUTTON_FONT,
            bg=PRIMARY, fg="white",
            command=self.open_modification
        ).pack(side="right", padx=15, pady=10)

        # -----------------------------------------------------
        #   SCROLLABLE AREA
        # -----------------------------------------------------
        container = tk.Frame(self.popup)
        container.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        canvas = tk.Canvas(container, bg="white")
        canvas.pack(side="left", fill="both", expand=True)

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=canvas.yview)

        self.frame = tk.Frame(canvas, bg="white")
        window_id = canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Auto-resize
        self.frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(window_id, width=e.width))

        # Gestion molette
        self.popup.bind("<MouseWheel>", lambda e: canvas.yview_scroll(-int(e.delta / 120), "units"))

        # Remplir contenu
        self._fill()

    # ---------------------------------------------------------
    #   REMPLISSAGE DU CONTENU
    # ---------------------------------------------------------
    def _title(self, text: str):
        tk.Label(self.frame, text=text, font=TITLE_FONT,
                 bg="white").pack(anchor="w", pady=(15, 5))

    def _line(self, text: str):
        tk.Label(self.frame, text=text, font=TEXT_FONT,
                 bg="white", wraplength=700, justify="left").pack(anchor="w", pady=3)

    def _fill(self):
        # ================== Informations générales ==================
        self._title("Informations générales")

        self._line(f"📅 Date : {self.affaire.date or '—'}")
        self._line(f"📍 Lieu : {self.affaire.lieu or '—'}")
        self._line(f"🧩 Type : {self.affaire.type_affaire or '—'}")
        self._line(f"👮 Responsable : {self.affaire.responsables or '—'}")
        self._line(f"📌 État : {self.affaire.etat}")
        self._line(f"📊 Urgence : {self.affaire.urgence}")

        # ================== Description ==================
        self._title("Description")
        self._line(self.affaire.description or "Aucune description fournie.")

        # ================== Personnes ==================
        self._title("Personnes impliquées")
        if not self.affaire.personnes:
            self._line("Aucune personne enregistrée.")
        else:
            for p in self.affaire.personnes:
                tk.Label(
                    self.frame,
                    text=f"{p.role} – {p.nom}",
                    font=("Arial", 13, "bold"),
                    bg="white"
                ).pack(anchor="w", pady=(10, 0))

                self._line(f"Identité : {p.identité or '—'}")
                self._line(f"Adresse : {p.adresse or '—'}")
                self._line(f"Contact : {p.contact or '—'}")
                self._line(f"Liens : {p.liens or '—'}")
                self._line(f"Notes : {p.historique or '—'}")

        # ================== Photos ==================
        self._title("Pièces jointes")
        if not self.affaire.photos:
            self._line("Aucune photo enregistrée.")
        else:
            for ph in self.affaire.photos:
                self._line(f"📷 {ph}")

        # ================== Bouton fermer ==================
        tk.Button(
            self.frame,
            text="Fermer",
            font=BUTTON_FONT, bg=DANGER, fg="white",
            command=self.popup.destroy
        ).pack(pady=20)

    # ---------------------------------------------------------
    #   OUVRIR LA VUE DE MODIFICATION
    # ---------------------------------------------------------
    def open_modification(self):
        ModifierAffaireView(
            root=self.root,
            service=self.service,
            affaire=self.affaire,
            on_done=self.after_modification
        )
        self.popup.destroy()

    # ---------------------------------------------------------
    #   CALLACK APRÈS MODIFICATION
    # ---------------------------------------------------------
    def after_modification(self):
        """Rafraîchit l'affichage de l'accueil ou liste si demandé."""
        if self.on_done:
            self.on_done()
