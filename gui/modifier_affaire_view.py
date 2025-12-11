from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
from typing import Callable, Optional, List

from core.models.affaire import Affaire
from core.models.personne import Personne
from core.services.affaire_service import AffaireService


class ModifierAffaireView:
    """
    Vue permettant de modifier une affaire déjà existante.
    """

    def __init__(self, root: tk.Tk, service: AffaireService,
                 affaire: Affaire, on_done: Optional[Callable] = None):

        self.root = root
        self.service = service
        self.affaire_originale = affaire
        self.on_done = on_done

        # On travaille sur une copie modifiable
        self.affaire = Affaire.from_dict(affaire.to_dict(), path=affaire.path)

        # Pour manipuler l’UI
        self.personnes_widgets: List[tk.Frame] = []

        self.build()

    # ---------------------------------------------------------
    #   CONSTRUCTION DE LA FENÊTRE
    # ---------------------------------------------------------
    def build(self):
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Modifier l'affaire")
        self.popup.geometry("750x750")

        # -------- SCROLLABLE ZONE --------
        container = tk.Frame(self.popup)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        self.frame = tk.Frame(canvas)
        window_id = canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(window_id, width=e.width))

        # ---------------- Remplir le contenu ----------------
        self._build_form()

        # -------- Boutons bas --------
        btns = tk.Frame(self.popup)
        btns.pack(fill="x", pady=10)

        tk.Button(btns, text="💾 Enregistrer", bg="#cce5ff",
                  command=self.save).pack(side="right", padx=6)

        tk.Button(btns, text="✖ Annuler", bg="#f8d7da",
                  command=self.cancel).pack(side="right", padx=6)

        tk.Button(btns, text="↺ Réinitialiser", bg="#e2e3e5",
                  command=self.reset).pack(side="right", padx=6)

    # ---------------------------------------------------------
    #   FORMULAIRE PRINCIPAL
    # ---------------------------------------------------------
    def _build_form(self):
        # Section titre
        tk.Label(self.frame, text="Modifier l'affaire", font=("Arial", 18, "bold"),
                 bg="white").pack(anchor="w", pady=10)

        # Champs simples
        self.entry_titre = self._entry("Titre :", self.affaire.titre)
        self.entry_date = self._entry("Date :", self.affaire.date)
        self.entry_lieu = self._entry("Lieu :", self.affaire.lieu)
        self.entry_type = self._entry("Type :", self.affaire.type_affaire)
        self.entry_resp = self._entry("Responsables :", self.affaire.responsables)

        # État
        tk.Label(self.frame, text="État :").pack(anchor="w", pady=(8, 0))
        self.etat_var = tk.StringVar(value=self.affaire.etat)
        tk.OptionMenu(self.frame, self.etat_var,
                      "🟢 En cours",
                      "🟡 À surveiller",
                      "🔵 Gelée — manque d'informations",
                      "🟣 Affaire classée").pack(fill="x")

        # Urgence
        tk.Label(self.frame, text="Urgence :").pack(anchor="w", pady=(8, 0))
        self.urgence_ent = self._entry_raw(self.affaire.urgence)

        # Description
        tk.Label(self.frame, text="Description :").pack(anchor="w", pady=(8, 0))
        self.desc_txt = tk.Text(self.frame, height=5, wrap="word")
        self.desc_txt.pack(fill="x")
        self.desc_txt.insert("1.0", self.affaire.description)

        # ---------------------------------------------------------
        # PERSONNES
        # ---------------------------------------------------------
        tk.Label(self.frame, text="Personnes impliquées :", font=("Arial", 14, "bold")
                 ).pack(anchor="w", pady=(15, 5))

        self.personnes_container = tk.Frame(self.frame)
        self.personnes_container.pack(fill="x")

        for p in self.affaire.personnes:
            self._add_personne_widget(p)

        tk.Button(self.frame, text="Ajouter une personne",
                  command=self._add_personne_form).pack(pady=5)

        # ---------------------------------------------------------
        # PHOTOS
        # ---------------------------------------------------------
        tk.Label(self.frame, text="Photos / pièces jointes :", font=("Arial", 14, "bold")
                 ).pack(anchor="w", pady=(15, 5))

        self.photos_listbox = tk.Listbox(self.frame, height=4)
        self.photos_listbox.pack(fill="x", pady=5)

        for ph in self.affaire.photos:
            self.photos_listbox.insert(tk.END, ph)

        tk.Button(self.frame, text="Ajouter une photo", command=self.add_photo).pack(pady=5)

    # ---------------------------------------------------------
    #   HELPERS POUR LES CHAMPS
    # ---------------------------------------------------------
    def _entry(self, label: str, value: str):
        tk.Label(self.frame, text=label).pack(anchor="w", pady=(8, 0))
        entry = tk.Entry(self.frame)
        entry.pack(fill="x")
        entry.insert(0, value)
        return entry

    def _entry_raw(self, value: str):
        entry = tk.Entry(self.frame)
        entry.pack(fill="x")
        entry.insert(0, value)
        return entry

    # ---------------------------------------------------------
    #   PERSONNES : AJOUT / AFFICHAGE
    # ---------------------------------------------------------
    def _add_personne_widget(self, personne: Personne):
        row = tk.Frame(self.personnes_container)
        row.pack(fill="x", pady=3)

        lbl = tk.Label(row, text=f"{personne.role} – {personne.nom}")
        lbl.pack(side="left")

        tk.Button(row, text="Détails",
                  command=lambda p=personne: self._edit_personne(p)).pack(side="right", padx=5)

        self.personnes_widgets.append(row)

    def _add_personne_form(self):
        """Ajout d'une nouvelle personne via formulaire popup."""

        popup = tk.Toplevel(self.popup)
        popup.title("Ajouter une personne")
        popup.geometry("300x350")

        # Rôle
        tk.Label(popup, text="Rôle :").pack(anchor="w")
        role_var = tk.StringVar(value="Victime")
        tk.OptionMenu(popup, role_var, "Victime", "Suspect", "Témoin",
                      "Auteur présumé", "Officier").pack(fill="x")

        # Nom
        tk.Label(popup, text="Nom :").pack(anchor="w")
        entry_nom = tk.Entry(popup)
        entry_nom.pack(fill="x")

        # Bouton ajouter
        tk.Button(
            popup,
            text="Ajouter",
            command=lambda: self._confirm_add_personne(popup, role_var.get(), entry_nom.get())
        ).pack(pady=10)

    def _confirm_add_personne(self, popup, role, nom):
        nom = nom.strip()
        if not nom:
            messagebox.showerror("Erreur", "Le nom est obligatoire.")
            return

        p = Personne(role=role, nom=nom)
        self.affaire.personnes.append(p)

        self._add_personne_widget(p)

        popup.destroy()

    # ---------------------------------------------------------
    #   EDIT PERSONNE
    # ---------------------------------------------------------
    def _edit_personne(self, personne: Personne):
        popup = tk.Toplevel(self.popup)
        popup.title(f"Modifier : {personne.nom}")
        popup.geometry("400x500")

        entries = {}

        def field(label: str, key: str):
            tk.Label(popup, text=label).pack(anchor="w", pady=(6, 0))
            e = tk.Entry(popup)
            e.pack(fill="x")
            e.insert(0, getattr(personne, key))
            entries[key] = e

        field("Identité", "identité")
        field("Adresse", "adresse")
        field("Contact", "contact")

        # Liens
        tk.Label(popup, text="Liens :").pack(anchor="w", pady=(6, 0))
        txt_liens = tk.Text(popup, height=3)
        txt_liens.pack(fill="x")
        txt_liens.insert("1.0", personne.liens)

        # Historique
        tk.Label(popup, text="Historique :").pack(anchor="w", pady=(6, 0))
        txt_hist = tk.Text(popup, height=4)
        txt_hist.pack(fill="x")
        txt_hist.insert("1.0", personne.historique)

        def save():
            for key, entry in entries.items():
                setattr(personne, key, entry.get().strip())

            personne.liens = txt_liens.get("1.0", "end").strip()
            personne.historique = txt_hist.get("1.0", "end").strip()

            popup.destroy()

        tk.Button(popup, text="Enregistrer", command=save).pack(pady=10)

    # ---------------------------------------------------------
    #   PHOTOS
    # ---------------------------------------------------------
    def add_photo(self):
        fichier = filedialog.askopenfilename(
            title="Choisir une photo",
            filetypes=[("Images", "*.jpg *.png *.jpeg *.gif")]
        )
        if fichier:
            self.affaire.photos.append(fichier)
            self.photos_listbox.insert(tk.END, fichier)

    # ---------------------------------------------------------
    #   ANNULATION
    # ---------------------------------------------------------
    def cancel(self):
        if messagebox.askyesno("Annuler", "Voulez-vous annuler sans sauvegarder ?"):
            self.popup.destroy()

    # ---------------------------------------------------------
    #   RESET (RECHARGER L'AFFAIRE D'ORIGINE)
    # ---------------------------------------------------------
    def reset(self):
        if not messagebox.askyesno("Réinitialiser", "Recharger les données d'origine ?"):
            return

        # Recréer une copie à partir de l’original
        self.affaire = Affaire.from_dict(self.affaire_originale.to_dict(), path=self.affaire.path)

        # Reconstruire la vue
        self.popup.destroy()
        self.build()

    # ---------------------------------------------------------
    #   COLLECTE ET SAUVEGARDE FINALE
    # ---------------------------------------------------------
    def save(self):
        # Récupération des données
        self.affaire.titre = self.entry_titre.get().strip()
        self.affaire.date = self.entry_date.get().strip()
        self.affaire.lieu = self.entry_lieu.get().strip()
        self.affaire.type_affaire = self.entry_type.get().strip()
        self.affaire.responsables = self.entry_resp.get().strip()
        self.affaire.etat = self.etat_var.get().strip()
        self.affaire.urgence = self.urgence_ent.get().strip()
        self.affaire.description = self.desc_txt.get("1.0", "end").strip()

        if not self.affaire.titre:
            messagebox.showerror("Erreur", "Le titre est obligatoire.")
            return

        # Sauvegarde via le service
        self.service.save(self.affaire)

        messagebox.showinfo("Succès", "Affaire mise à jour.")
        self.popup.destroy()

        if self.on_done:
            self.on_done()
