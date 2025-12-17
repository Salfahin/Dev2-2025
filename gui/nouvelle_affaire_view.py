from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from typing import List, Callable, Optional

from core.models.affaire import Affaire
from core.models.personne import Personne
from core.services.affaire_service import AffaireService


# =========================================================
#   CATALOGUES MÉTIER
# =========================================================

class TypeAffaireCatalog:
    @staticmethod
    def all() -> list[str]:
        types = [
            "Meurtre / Homicide volontaire",
            "Tentative de meurtre",
            "Assassinat prémédité",
            "Enlèvement / Séquestration",
            "Agression",
            "Disparition inquiétante",
            "Décès suspect",
            "Intrusion inexpliquée",
            "Cambriolage",
            "Vol simple",
            "Vol de données sensibles",
            "Braquage",
            "Escroquerie / fraude",
            "Incendie volontaire",
            "Vandalisme",
            "Sabotage industriel",
            "Corruption",
            "Fuites d’informations",
            "Abus d’autorité",
            "Harcèlement en ligne",
            "Intrusion dans des systèmes",
            "Détournement d’identité numérique",
        ]
        return sorted(types)


class RolePersonneCatalog:
    @staticmethod
    def all() -> list[str]:
        roles = [
            "Victime",
            "Suspect",
            "Témoin",
            "Plaignant",
            "Enquêteur",
            "Expert",
            "Personne d’intérêt",
            "Avocat",
            "Agent de sécurité",
        ]
        return sorted(roles)


# =========================================================
#   VUE : NOUVELLE AFFAIRE
# =========================================================

class NouvelleAffaireView:
    """
    Vue permettant de créer une nouvelle affaire.
    """

    def __init__(
        self,
        root: tk.Tk,
        service: AffaireService,
        on_done: Optional[Callable] = None
    ):
        self.root = root
        self.service = service
        self.on_done = on_done

        self.personnes_data: List[Personne] = []
        self.photos: List[str] = []

        self.build()

    # ---------------------------------------------------------
    #   CONSTRUCTION DE LA FENÊTRE
    # ---------------------------------------------------------
    def build(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Nouvelle Affaire")

        wrapper = tk.Frame(self.root)
        wrapper.pack(expand=True)

        contenu = tk.Frame(wrapper)
        contenu.pack()

        tk.Label(contenu, text="Nouvelle Affaire", font=("Arial", 18)).pack(pady=10)

        frame = tk.Frame(contenu)
        frame.pack(padx=20, pady=10)

        self.entry_titre = self._champ(frame, "Titre de l’affaire :", 0)
        self.entry_date = self._champ(frame, "Date et heure du signalement :", 1)
        self.entry_lieu = self._champ(frame, "Lieu de l’incident :", 2)

        # ---------------------------------------------------------
        #   TYPE D’AFFAIRE (choisir OU écrire)
        # ---------------------------------------------------------
        tk.Label(frame, text="Type d’affaire :").grid(row=3, column=0, sticky="w", padx=5)

        self.selected_type = tk.StringVar()
        self.menu_type = ttk.Combobox(
            frame,
            textvariable=self.selected_type,
            values=TypeAffaireCatalog.all(),
            width=47
        )
        self.menu_type.set("Choisir ou écrire un type d’affaire")
        self.menu_type.grid(row=3, column=1, pady=5, sticky="w")

        # ---------------------------------------------------------
        #   PERSONNES IMPLIQUÉES
        # ---------------------------------------------------------
        tk.Label(frame, text="Personnes impliquées :").grid(row=4, column=0, sticky="nw", padx=5)

        personnes_frame = tk.Frame(frame)
        personnes_frame.grid(row=4, column=1, sticky="w")

        self.role_var = tk.StringVar(value="Victime")
        ttk.Combobox(
            personnes_frame,
            textvariable=self.role_var,
            values=RolePersonneCatalog.all(),
            width=22
        ).pack(side="left", padx=2)

        self.entry_nom = tk.Entry(personnes_frame, width=18)
        self.entry_nom.pack(side="left", padx=5)

        tk.Button(personnes_frame, text="Ajouter", command=self.add_personne).pack(side="left")

        self.frame_liste_personnes = tk.Frame(frame)
        self.frame_liste_personnes.grid(row=5, column=1, sticky="w")

        # ---------------------------------------------------------
        #   DESCRIPTION
        # ---------------------------------------------------------
        tk.Label(frame, text="Description :").grid(row=6, column=0, sticky="nw", padx=5)

        self.entry_desc = tk.Text(frame, width=38, height=5)
        self.entry_desc.grid(row=6, column=1, pady=5, sticky="w")

        self.entry_resp = self._champ(frame, "Responsable(s) :", 7)

        # ---------------------------------------------------------
        #   PHOTOS
        # ---------------------------------------------------------
        tk.Label(frame, text="Photos / pièces jointes :").grid(row=8, column=0, sticky="nw", padx=5)

        tk.Button(frame, text="Ajouter une photo", command=self.add_photo).grid(row=8, column=1, sticky="w")

        self.photos_listbox = tk.Listbox(frame, width=45, height=3)
        self.photos_listbox.grid(row=9, column=1, sticky="w")

        # ---------------------------------------------------------
        #   ÉTAT / URGENCE
        # ---------------------------------------------------------
        self.selected_etat = tk.StringVar(value="🟢 En cours")
        self.selected_urgence = tk.StringVar(value="⚪ Faible")

        tk.Label(frame, text="État :").grid(row=10, column=0, sticky="w")
        tk.OptionMenu(
            frame,
            self.selected_etat,
            "🟢 En cours",
            "🟡 À surveiller",
            "🔵 Gelée — manque d'informations"
        ).grid(row=10, column=1, sticky="w")

        tk.Label(frame, text="Urgence :").grid(row=11, column=0, sticky="w")
        tk.OptionMenu(
            frame,
            self.selected_urgence,
            "⚪ Faible",
            "🟡 Moyen",
            "🟠 Élevé",
            "🔴 Critique"
        ).grid(row=11, column=1, sticky="w")

        # ---------------------------------------------------------
        #   BOUTONS
        # ---------------------------------------------------------
        btns = tk.Frame(contenu)
        btns.pack(pady=20)

        tk.Button(btns, text="Annuler", fg="red", width=15, command=self.cancel).pack(side="left", padx=10)
        tk.Button(btns, text="Enregistrer l’affaire", width=20, command=self.save).pack(side="left", padx=10)

    # ---------------------------------------------------------
    #   UTILITAIRES
    # ---------------------------------------------------------
    def _champ(self, parent, label, row):
        tk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=5)
        entry = tk.Entry(parent, width=50)
        entry.grid(row=row, column=1, pady=5, sticky="w")
        return entry

    # ---------------------------------------------------------
    #   PERSONNES
    # ---------------------------------------------------------
    def add_personne(self):
        nom = self.entry_nom.get().strip()
        if not nom:
            messagebox.showwarning("Erreur", "Veuillez indiquer un nom.")
            return

        personne = Personne(role=self.role_var.get(), nom=nom)
        personne.details = {
            "identite": "",
            "adresse": "",
            "contact": "",
            "liens": "",
            "notes": "",
        }

        self.personnes_data.append(personne)

        row = tk.Frame(self.frame_liste_personnes)
        row.pack(fill="x", pady=2)

        tk.Label(row, text=f"{personne.role} : {personne.nom}", width=30, anchor="w").pack(side="left")
        tk.Button(row, text="Détails", command=lambda p=personne: self.open_personne_details(p)).pack(side="left", padx=5)

        self.entry_nom.delete(0, tk.END)

    def open_personne_details(self, personne: Personne):
        window = tk.Toplevel(self.root)
        window.title(f"Détails – {personne.nom}")
        window.grab_set()

        fields = [
            ("Identité", "identite"),
            ("Adresse", "adresse"),
            ("Contact", "contact"),
            ("Liens", "liens"),
            ("Notes", "notes"),
        ]

        widgets = {}

        for i, (label, key) in enumerate(fields):
            tk.Label(window, text=label + " :").grid(row=i, column=0, sticky="nw", padx=10, pady=5)

            if key == "notes":
                w = tk.Text(window, width=40, height=4)
                w.insert("1.0", personne.details.get(key, ""))
            else:
                w = tk.Entry(window, width=42)
                w.insert(0, personne.details.get(key, ""))

            w.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            widgets[key] = w

        def save_details():
            for key, widget in widgets.items():
                if isinstance(widget, tk.Text):
                    personne.details[key] = widget.get("1.0", "end").strip()
                else:
                    personne.details[key] = widget.get().strip()
            window.destroy()

        tk.Button(window, text="Enregistrer", command=save_details).grid(
            row=len(fields), column=1, pady=15, sticky="e"
        )

    # ---------------------------------------------------------
    #   PHOTOS
    # ---------------------------------------------------------
    def add_photo(self):
        fichier = filedialog.askopenfilename(
            title="Choisir une photo",
            filetypes=[("Images", "*.jpg *.png *.jpeg *.gif")]
        )
        if fichier:
            self.photos.append(fichier)
            self.photos_listbox.insert(tk.END, fichier.split("/")[-1])

    # ---------------------------------------------------------
    #   AFFAIRE
    # ---------------------------------------------------------
    def _collect_affaire(self) -> Affaire:
        titre = self.entry_titre.get().strip()
        if not titre:
            raise ValueError("Le titre est obligatoire.")

        return Affaire(
            titre=titre,
            date=self.entry_date.get().strip(),
            lieu=self.entry_lieu.get().strip(),
            type_affaire=self.selected_type.get(),
            description=self.entry_desc.get("1.0", "end").strip(),
            responsables=self.entry_resp.get().strip(),
            photos=self.photos.copy(),
            personnes=self.personnes_data.copy(),
            etat=self.selected_etat.get(),
            urgence=self.selected_urgence.get(),
        )

    # ---------------------------------------------------------
    #   SAUVEGARDE / ANNULATION
    # ---------------------------------------------------------
    def save(self):
        try:
            affaire = self._collect_affaire()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return

        self.service.save(affaire)
        messagebox.showinfo("Succès", "Affaire enregistrée.")

        if self.on_done:
            self.on_done()

    def cancel(self):
        if messagebox.askyesno("Annuler", "Voulez-vous annuler la création de l'affaire ?"):
            if self.on_done:
                self.on_done()
