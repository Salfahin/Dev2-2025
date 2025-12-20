from __future__ import annotations
from gui.theme import *

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from typing import List, Callable, Optional, Set, Tuple

from core.models.affaire import Affaire
from core.models.personne import Personne
from core.services.affaire_service import AffaireService
import unicodedata
import re

def _safe_lower(s: str) -> str:
    return (s or "").strip().lower()


def _parse_date(s: str) -> Optional[datetime]:
    s = (s or "").strip()
    if not s:
        return None

    formats = [
        "%d-%m-%Y %H:%M",
        "%Y-%m-%d %H:%M",
        "%d-%m-%Y",
        "%Y-%m-%d",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    return None

def _parse_min(s: str) -> Optional[datetime]:
    dt = _parse_date(s)
    if not dt:
        return None
    # si pas d'heure → début de journée
    if len((s or "").strip()) == 10:
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return dt

def _parse_max(s: str) -> Optional[datetime]:
    dt = _parse_date(s)
    if not dt:
        return None
    # si pas d'heure → fin de journée
    if len((s or "").strip()) == 10:
        return dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    return dt



class FiltreFenetre(tk.Toplevel):
    """
    Popup de filtrage (style boutons), compatible avec ton AccueilView.
    - parent : root
    - service : AffaireService
    - on_apply : callback(list_affaires_filtrees)
    - on_reset : callback() => réaffiche tout
    """
    def __init__(
        self,
        parent: tk.Tk,
        service: AffaireService,
        on_apply: Callable[[List[Affaire]], None],
        on_reset: Callable[[], None]
    ):
        super().__init__(parent)
        self.service = service
        self.on_apply = on_apply
        self.on_reset = on_reset

        # --- critères actifs (on les cumule)
        self.kw: str | None = None
        self.lieu: str | None = None
        self.date_min: datetime | None = None
        self.date_max: datetime | None = None
        self.selected_person_names: set[str] = set()  # noms normalisés


        self.title("🔍 Filtrer les affaires")
        self.geometry("600x520")
        self.resizable(False, False)
        self.grab_set()

        #tout les filtres séléctionnés
        self.resume_lbl = tk.Label(self, text="Aucun filtre actif", fg="gray")
        self.resume_lbl.pack(pady=(10, 0))

        #les buttons du pop-up
        tk.Button(self, text="🔎 Mot-clé", bg=PRIMARY, fg="white", command=self.filtre_mot_cle)\
            .pack(fill="x", pady=5, padx=10)

        tk.Button(self, text="👤 Par personne (Victime/Suspect/Témoin)", bg=PRIMARY, fg="white", command=self.filtre_personnes)\
            .pack(fill="x", pady=5, padx=10)

        tk.Button(self, text="📍 Par lieu", bg=PRIMARY, fg="white", command=self.filtre_lieu)\
            .pack(fill="x", pady=5, padx=10)

        tk.Button(self, text="📅 Entre deux dates", bg=PRIMARY, fg="white", command=self.filtre_dates)\
            .pack(fill="x", pady=5, padx=10)

        tk.Label(self, text="").pack()

        #button réinitialiser
        tk.Button(
            self,
            text="♻️ Réinitialiser", bg=SUCCESS, fg="white",
            command=self.reset
        ).pack(fill="x", pady=5, padx=10)

        
        tk.Button(self, text="✅ Appliquer filtre", bg=SUCCESS, fg="white", command=self.apply_filters)\
            .pack(fill="x", pady=5, padx=10)


    # ------------------------
    # FILTRE : MOT CLE
    # ------------------------
    def filtre_mot_cle(self):
        texte = simpledialog.askstring("Recherche", "Mot à chercher :", parent=self)
        if not texte:
            return

        q = _norm(texte)
        resultats = []

        for a in self.service.get_all():
            hay = _norm(affaire_full_text(a))
            if q in hay:
                resultats.append(a)

        self.kw = texte.strip()
        self.update_resume()
        messagebox.showinfo("Filtre ajouté", "Mot-clé enregistré. Clique sur ✅ Appliquer filtre.", parent=self)



    # ------------------------
    # FILTRE : LIEU
    # ------------------------
    def filtre_lieu(self):
        lieu = simpledialog.askstring("Lieu", "Lieu (contient) :", parent=self)
        if not lieu:
            return

        q = _safe_lower(lieu)
        resultats = [
            a for a in self.service.get_all()
            if q in _safe_lower(getattr(a, "lieu", ""))
        ]

        self.lieu = lieu.strip()
        self.update_resume()
        messagebox.showinfo("Filtre ajouté", "Lieu enregistré. Clique sur ✅ Appliquer filtre.", parent=self)


    # ------------------------
    # FILTRE : DATES
    # ------------------------
    def filtre_dates(self):
        dmin = simpledialog.askstring(
            "Filtrer",
            "Date minimum (JJ-MM-AAAA ou YYYY-MM-DD)\nLaisser vide pour aucune :",
            parent=self
        )
        if dmin == "":
            dmin = None

        dmax = simpledialog.askstring(
            "Filtrer",
            "Date maximum (JJ-MM-AAAA ou YYYY-MM-DD)\nLaisser vide pour aucune :",
            parent=self
        )
        if dmax == "":
            dmax = None

        date_min = _parse_min(dmin) if dmin else None
        date_max = _parse_max(dmax) if dmax else None


        if (dmin and not date_min) or (dmax and not date_max):
            return messagebox.showerror(
                "Erreur",
                "Date invalide.\nFormats acceptés : JJ-MM-AAAA ou YYYY-MM-DD",
                parent=self
            )

        resultats: List[Affaire] = []
        for a in self.service.get_all():
            date_aff = _parse_date(getattr(a, "date", "") or "")
            if not date_aff:
                continue

            if date_min and date_aff < date_min:
                continue
            if date_max and date_aff > date_max:
                continue

            resultats.append(a)

        self.date_min = date_min
        self.date_max = date_max
        self.update_resume()
        messagebox.showinfo("Filtre ajouté", "Dates enregistrées. Clique sur ✅ Appliquer filtre.", parent=self)


    # ========================
    # FILTRE PAR PERSONNES (multi select + recherche)
    # ========================
    def filtre_personnes(self):
        affaires = self.service.get_all()

        # 1) collecter toutes les personnes uniques (role + nom)
        personnes = []
        seen = set()

        for a in affaires:
            for p in (getattr(a, "personnes", []) or []):
                role = (getattr(p, "role", "") or "").strip()
                nom = (getattr(p, "nom", "") or "").strip()
                if not nom:
                    continue
                key = (role, _norm(nom))
                if key in seen:
                    continue
                seen.add(key)
                personnes.append((role, nom))

        if not personnes:
            messagebox.showinfo("Info", "Aucune personne trouvée dans les affaires.", parent=self)
            return

        personnes.sort(key=lambda x: _norm(x[1]))

        # 2) popup
        popup = tk.Toplevel(self)
        popup.title("Filtrer par personnes")
        popup.geometry("420x520")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        # 3) recherche
        tk.Label(popup, text="Rechercher (nom/prénom) :").pack(anchor="w", padx=10, pady=(10, 0))
        search_var = tk.StringVar()
        search_entry = tk.Entry(popup, textvariable=search_var)
        search_entry.pack(fill="x", padx=10)

        # 4) zone scrollable
        container = tk.Frame(popup)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scroll.set)

        inner = tk.Frame(canvas)
        inner_id = canvas.create_window((0, 0), window=inner, anchor="nw")
        
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(inner_id, width=e.width))
        
        # Molette : active seulement quand la souris est sur la liste
        def _wheel(event):
            if getattr(event, "delta", 0):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                return "break"
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
                return "break"
            if event.num == 5:
                canvas.yview_scroll(1, "units")
                return "break"

        def _bind_wheel(_e=None):
            canvas.bind_all("<MouseWheel>", _wheel)
            canvas.bind_all("<Button-4>", _wheel)
            canvas.bind_all("<Button-5>", _wheel)

        def _unbind_wheel(_e=None):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        canvas.bind("<Enter>", _bind_wheel)
        canvas.bind("<Leave>", _unbind_wheel)
        inner.bind("<Enter>", _bind_wheel)
        inner.bind("<Leave>", _unbind_wheel)

        # 5) QCM : une case par personne
        vars_by_person = {}

        def refresh_list(*_):
            for w in inner.winfo_children():
                w.destroy()

            q = _norm(search_var.get())

            for role, nom in personnes:
                label = f"{role} – {nom}"
                if q and q not in _norm(label):
                    continue

                var = vars_by_person.setdefault((role, nom), tk.BooleanVar(value=False))
                ttk.Checkbutton(inner, text=label, variable=var).pack(anchor="w", pady=2)

        def apply_filter():
            selected = {
                _norm(nom)
                for (role, nom), var in vars_by_person.items()
                if var.get()
            }
            if not selected:
                messagebox.showinfo("Info", "Sélectionne au moins une personne.", parent=popup)
                return

            # On stocke et on NE filtre PAS ici
            self.selected_person_names = selected
            self.update_resume()

            popup.destroy()
            messagebox.showinfo("Filtre ajouté", "Personnes enregistrées. Clique sur ✅ Appliquer filtre.", parent=self)


        # 6) boutons
        actions = tk.Frame(popup)
        actions.pack(fill="x", padx=10, pady=(0, 10))

        tk.Button(actions, text="Tout cocher",
            command=lambda: [v.set(True) for v in vars_by_person.values()]).pack(side="left")

        tk.Button(actions, text="Tout décocher",
            command=lambda: [v.set(False) for v in vars_by_person.values()]).pack(side="left", padx=6)

        tk.Button(actions, text="✅ Filtrer", command=apply_filter).pack(side="right")

        # recherche dynamique
        search_var.trace_add("write", refresh_list)

        refresh_list()
        search_entry.focus_set()

    def update_resume(self):
        parts = []
        if self.kw:
            parts.append(f"Mot-clé: {self.kw}")
        if self.lieu:
            parts.append(f"Lieu: {self.lieu}")
        if self.date_min or self.date_max:
            dm = self.date_min.strftime("%d-%m-%Y") if self.date_min else "—"
            dx = self.date_max.strftime("%d-%m-%Y") if self.date_max else "—"
            parts.append(f"Dates: {dm} → {dx}")
        if self.selected_person_names:
            parts.append(f"Personnes: {len(self.selected_person_names)} sélectionnée(s)")

        self.resume_lbl.config(text=" | ".join(parts) if parts else "Aucun filtre actif")

    def apply_filters(self):
        affaires = self.service.get_all()

            # On applique tous les critères (intersection)
        out = []
        for a in affaires:
            # mot-clé (sur tout le texte)
            if self.kw:
                if _norm(self.kw) not in _norm(affaire_full_text(a)):
                    continue

            # lieu
            if self.lieu:
                if _norm(self.lieu) not in _norm(getattr(a, "lieu", "") or ""):
                    continue

            # dates
            if self.date_min or self.date_max:
                da = _parse_date(getattr(a, "date", "") or "")
                if not da:
                    continue
                if self.date_min and da < self.date_min:
                    continue
                if self.date_max and da > self.date_max:
                    continue

            # personnes
            if self.selected_person_names:
                noms_aff = {
                    _norm(getattr(p, "nom", "") or "")
                    for p in (getattr(a, "personnes", []) or [])
                }
                if noms_aff.isdisjoint(self.selected_person_names):
                    continue

            out.append(a)

        self.on_apply(out)
        self.destroy()


        


    #réinitialiser filtre
    def reset(self):
        """
        Annule tous les filtres, remet l’affichage normal
        et ferme la fenêtre de filtrage.
        """
        # Réaffiche toutes les affaires
        self.on_reset()

        # Ferme la fenêtre de filtrage
        self.destroy()


def _norm(s: str) -> str:
    """
    Normalisation forte :
    - minuscule (case-insensitive)
    - suppression accents
    - normalisation apostrophes typographiques
    - suppression ponctuation
    - espaces propres
    """
    if not s:
        return ""

    # minuscules robustes
    s = s.casefold()

    # normalisation unicode
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")

    # apostrophes typographiques → apostrophe simple
    s = s.replace("’", "'").replace("‘", "'")

    # supprimer toute ponctuation (garde lettres & chiffres)
    s = re.sub(r"[^a-z0-9\s]", " ", s)

    # espaces propres
    s = re.sub(r"\s+", " ", s).strip()

    return s


def affaire_full_text(a) -> str:
    parts = []

    # Champs de l'affaire
    for attr in ("titre", "date", "lieu", "type_affaire", "responsables",
                 "description", "etat", "urgence"):
        parts.append(str(getattr(a, attr, "") or ""))

    # Personnes
    for p in (getattr(a, "personnes", []) or []):
        for attr in ("role", "nom", "identité", "adresse", "contact", "liens", "historique"):
            parts.append(str(getattr(p, attr, "") or ""))

    # Photos (optionnel)
    for ph in (getattr(a, "photos", []) or []):
        parts.append(str(ph or ""))

    return "\n".join(parts)