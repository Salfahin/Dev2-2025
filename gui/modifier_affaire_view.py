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

    def __init__(
        self,
        root: tk.Tk,
        affaire: Affaire,
        service: AffaireService,
        on_done: Optional[Callable[[], None]] = None
    ):
        self.root = root
        self.service = service
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

        # Scrollable container (Canvas + Frame)
        container = tk.Frame(self.popup)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        def on_frame_configure(_event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        def on_canvas_configure(event):
            # Ajuste la largeur du frame interne à la largeur du canvas
            self.canvas.itemconfig(self.canvas_window, width=event.width)

        self.frame.bind("<Configure>", on_frame_configure)
        self.canvas.bind("<Configure>", on_canvas_configure)

        # (Optionnel) scroll molette Windows
        def _on_mousewheel(event):
            # event.delta >0 (haut) / <0 (bas)
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # ---- Champs principaux
        tk.Label(self.frame, text="Titre").pack(anchor="w", pady=(10, 0))
        self.titre_entry = tk.Entry(self.frame)
        self.titre_entry.pack(fill="x")
        self.titre_entry.insert(0, self.affaire.titre)

        tk.Label(self.frame, text="Date").pack(anchor="w", pady=(10, 0))
        self.date_entry = tk.Entry(self.frame)
        self.date_entry.pack(fill="x")
        self.date_entry.insert(0, self.affaire.date)

        tk.Label(self.frame, text="Lieu").pack(anchor="w", pady=(10, 0))
        self.lieu_entry = tk.Entry(self.frame)
        self.lieu_entry.pack(fill="x")
        self.lieu_entry.insert(0, self.affaire.lieu)

        tk.Label(self.frame, text="Type d'affaire").pack(anchor="w", pady=(10, 0))
        self.type_affaire_combo = ttk.Combobox(
            self.frame,
            values=[
                "Disparition inquiétante",
                "Vol",
                "Homicide",
                "Fraude",
                "Autre"
            ]
        )
        self.type_affaire_combo.pack(fill="x")
        self.type_affaire_combo.set(self.affaire.type_affaire)

        # ---- Urgence / Etat
        tk.Label(self.frame, text="Urgence").pack(anchor="w", pady=(10, 0))
        self.urgence_combo = ttk.Combobox(
            self.frame,
            values=["🔴 Élevée", "🟠 Moyenne", "⚪ Faible"]
        )
        self.urgence_combo.pack(fill="x")
        self.urgence_combo.set(self.affaire.urgence)

        # ---- État (OptionMenu)
        tk.Label(self.frame, text="État").pack(anchor="w", pady=(10, 0))

        etat_values = [
            "🟢 En cours",
            "🟡 À surveiller",
            "🔵 Gelée — manque d'informations",
            "🟣 Affaire classée",
        ]

        # Variable liée à l’OptionMenu
        self.etat_var = tk.StringVar()

        # Valeur par défaut (sécurité si valeur absente)
        if self.affaire.etat in etat_values:
            self.etat_var.set(self.affaire.etat)
        else:
            self.etat_var.set(etat_values[0])

        self.etat_menu = tk.OptionMenu(
            self.frame,
            self.etat_var,
            *etat_values
        )
        self.etat_menu.pack(fill="x")

        # ---- Responsables
        tk.Label(self.frame, text="Responsables").pack(anchor="w", pady=(10, 0))
        self.responsables_entry = tk.Entry(self.frame)
        self.responsables_entry.pack(fill="x")
        self.responsables_entry.insert(0, self.affaire.responsables)

        # ---- Description
        tk.Label(self.frame, text="Description").pack(anchor="w", pady=(10, 0))
        self.desc_txt = tk.Text(self.frame, height=6)
        self.desc_txt.pack(fill="both")
        self.desc_txt.insert("1.0", self.affaire.description)

        # ---------------------------------------------------------
        #   PERSONNES
        # ---------------------------------------------------------
        tk.Label(self.frame, text="Personnes impliquées", font=("Arial", 12, "bold")).pack(
            anchor="w", pady=(15, 5)
        )

        self.personnes_container = tk.Frame(self.frame)
        self.personnes_container.pack(fill="x")

        for p in self.affaire.personnes:
            self._add_personne_widget(p)

        tk.Button(self.frame, text="➕ Ajouter une personne", command=self._add_personne_form).pack(
            anchor="w", pady=(8, 0)
        )

        # ---------------------------------------------------------
        #   PHOTOS
        # ---------------------------------------------------------
        tk.Label(self.frame, text="Photos", font=("Arial", 12, "bold")).pack(
            anchor="w", pady=(15, 5)
        )

        self.photos_listbox = tk.Listbox(self.frame, height=5)
        self.photos_listbox.pack(fill="x")

        for ph in self.affaire.photos:
            self.photos_listbox.insert(tk.END, ph)

        tk.Button(self.frame, text="📷 Ajouter une photo", command=self.add_photo).pack(
            anchor="w", pady=(8, 0)
        )

        # ---------------------------------------------------------
        #   BOUTONS
        # ---------------------------------------------------------
        btns = tk.Frame(self.frame)
        btns.pack(fill="x", pady=15)

        tk.Button(btns, text="💾 Enregistrer", command=self.save).pack(side="right", padx=5)
        tk.Button(btns, text="Annuler", command=self.cancel).pack(side="right")

    # ---------------------------------------------------------
    #   OUTILS
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
    def _delete_personne(self, personne: Personne, row: tk.Frame):
        """Supprime une personne de l'affaire (modèle + UI)."""
        if not messagebox.askyesno(
            "Supprimer",
            f"Supprimer « {personne.role} – {personne.nom} » de l'affaire ?",
            parent=self.popup
        ):
            return

        # Retirer du modèle
        try:
            self.affaire.personnes.remove(personne)
        except ValueError:
            pass

        # Retirer de l’UI
        try:
            row.destroy()
        except Exception:
            pass

        # Nettoyage interne (optionnel mais propre)
        try:
            self.personnes_widgets.remove(row)
        except ValueError:
            pass

        # Remettre la fenêtre devant (confort)
        try:
            self.popup.lift()
            self.popup.focus_force()
        except Exception:
            pass

    def _add_personne_widget(self, personne: Personne):
        row = tk.Frame(self.personnes_container)
        row.pack(fill="x", pady=3)

        lbl = tk.Label(row, text=f"{personne.role} – {personne.nom}")
        lbl.pack(side="left")

        tk.Button(
            row, text="Détails",
            command=lambda p=personne: self._edit_personne(p)
        ).pack(side="right", padx=5)

        tk.Button(
            row, text="Supprimer", fg="red",
            command=lambda p=personne, r=row: self._delete_personne(p, r)
        ).pack(side="right", padx=5)

        self.personnes_widgets.append(row)

    def _add_personne_form(self):
        """Ajout d'une nouvelle personne via formulaire popup."""

        popup = tk.Toplevel(self.popup)
        popup.title("Ajouter une personne")
        popup.geometry("300x350")

        # Mettre la popup au-dessus
        popup.transient(self.popup)
        popup.grab_set()
        popup.lift()
        popup.focus_force()

        tk.Label(popup, text="Rôle").pack(anchor="w", pady=(10, 0))
        role_combo = ttk.Combobox(
            popup,
            values=["🟦 Victime", "🟥 Suspect", "🟨 Témoin", "🟩 Autre"]
        )
        role_combo.pack(fill="x")

        tk.Label(popup, text="Nom").pack(anchor="w", pady=(10, 0))
        nom_entry = tk.Entry(popup)
        nom_entry.pack(fill="x")

        def create():
            role = role_combo.get().strip()
            nom = nom_entry.get().strip()

            if not role or not nom:
                messagebox.showerror("Erreur", "Rôle et nom sont obligatoires.", parent=popup)
                return

            p = Personne(role=role, nom=nom)

            # Ajout au modèle
            self.affaire.personnes.append(p)

            # Ajout à l'UI
            self._add_personne_widget(p)

            popup.destroy()
            # remettre la fenêtre principale devant
            self.popup.lift()
            self.popup.focus_force()

        tk.Button(popup, text="Ajouter", command=create).pack(pady=15)

    def _edit_personne(self, personne: Personne):
        """Edition complète d'une personne (popup)"""
        popup = tk.Toplevel(self.popup)
        popup.title("Détails personne")
        popup.geometry("420x520")

        # Mettre la popup au-dessus
        popup.transient(self.popup)
        popup.grab_set()
        popup.lift()
        popup.focus_force()

        tk.Label(popup, text=f"{personne.role} – {personne.nom}", font=("Arial", 12, "bold")).pack(
            pady=(10, 5)
        )

        tk.Label(popup, text="Nom").pack(anchor="w", pady=(6, 0))
        nom_entry = tk.Entry(popup)
        nom_entry.pack(fill="x")
        nom_entry.insert(0, personne.nom)

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
        tk.Label(popup, text="Liens").pack(anchor="w", pady=(6, 0))
        liens_txt = tk.Text(popup, height=4)
        liens_txt.pack(fill="both")
        liens_txt.insert("1.0", personne.liens)

        # Historique
        tk.Label(popup, text="Historique").pack(anchor="w", pady=(6, 0))
        hist_txt = tk.Text(popup, height=6)
        hist_txt.pack(fill="both")
        hist_txt.insert("1.0", personne.historique)

        def save_personne():
            personne.nom = nom_entry.get().strip()
            for k, e in entries.items():
                setattr(personne, k, e.get().strip())
            personne.liens = liens_txt.get("1.0", "end").strip()
            personne.historique = hist_txt.get("1.0", "end").strip()

            popup.destroy()
            # remettre la fenêtre principale devant
            self.popup.lift()
            self.popup.focus_force()

            # Refresh de l'affichage des personnes (simple)
            for w in self.personnes_widgets:
                w.destroy()
            self.personnes_widgets.clear()
            for p in self.affaire.personnes:
                self._add_personne_widget(p)

        tk.Button(popup, text="Enregistrer", command=save_personne).pack(pady=10)

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
    #   SAUVEGARDE
    # ---------------------------------------------------------
    def save(self):
        # Récupération des champs
        self.affaire.titre = self.titre_entry.get().strip()
        self.affaire.date = self.date_entry.get().strip()
        self.affaire.lieu = self.lieu_entry.get().strip()
        self.affaire.type_affaire = self.type_affaire_combo.get().strip()
        self.affaire.urgence = self.urgence_combo.get().strip()
        self.affaire.etat = self.etat_var.get()
        self.affaire.responsables = self.responsables_entry.get().strip()
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
