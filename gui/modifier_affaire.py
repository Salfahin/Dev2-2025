import tkinter as tk
from tkinter import messagebox
import json

def modif_affaire(path, parent_popup, ouvrir_affaire):
    """
    Ouvre une fenêtre d'édition pour l'affaire située à `path`.
    parent_popup : la fenêtre d'affichage (Toplevel) à fermer/recharger après sauvegarde.
    ouvrir_affaire : fonction permettant de recharger l'affichage après sauvegarde.
    """
    # charger le fichier
    try:
        with open(path, "r", encoding="utf-8") as f:
            affaire = json.load(f)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir l'affaire :\n{e}")
        return

    # garder une copie originale pour annuler / revert
    try:
        _original_data = json.loads(json.dumps(affaire))  # deep copy simple
    except Exception:
        _original_data = affaire.copy()

    # ======== Toplevel ========
    edit = tk.Toplevel()
    edit.title("Modifier l'affaire")
    edit.geometry("720x720")

    # ======== Zone scrollable pour les champs ========
    scroll_frame = tk.Frame(edit)
    scroll_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(scroll_frame)
    scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ======== Helper pour Entry ========
    def add_entry(label_text, initial=""):
        tk.Label(scrollable_frame, text=label_text, anchor="w").pack(anchor="w", pady=(6, 0))
        ent = tk.Entry(scrollable_frame)
        ent.pack(fill="x")
        ent.insert(0, initial if initial is not None else "")
        return ent

    titre_ent = add_entry("Titre :", affaire.get("titre", ""))
    date_ent = add_entry("Date :", affaire.get("date", ""))
    lieu_ent = add_entry("Lieu :", affaire.get("lieu", ""))
    type_ent = add_entry("Type d'affaire :", affaire.get("type_affaire", ""))
    resp_ent = add_entry("Responsables :", affaire.get("responsables", ""))
    etat_ent = add_entry("État :", affaire.get("etat", ""))
    urg_ent = add_entry("Niveau d'urgence :", affaire.get("urgence", ""))

    tk.Label(scrollable_frame, text="Description :").pack(anchor="w", pady=(8, 0))
    desc_txt = tk.Text(scrollable_frame, height=6, wrap="word")
    desc_txt.pack(fill="both", expand=False)
    desc_txt.insert("1.0", affaire.get("description", ""))

    tk.Label(scrollable_frame, text="Personnes (JSON) — liste d'objets [{...}] :").pack(anchor="w", pady=(8, 0))
    personnes_txt = tk.Text(scrollable_frame, height=14, wrap="none")
    personnes_txt.pack(fill="both", expand=True)
    personnes_txt.insert("1.0", json.dumps(affaire.get("personnes", []), ensure_ascii=False, indent=2))

    # ======== Fonctions internes ========
    def _build_new_data_from_widgets():
        new = {
            "titre": titre_ent.get().strip(),
            "date": date_ent.get().strip(),
            "lieu": lieu_ent.get().strip(),
            "type_affaire": type_ent.get().strip(),
            "responsables": resp_ent.get().strip(),
            "etat": etat_ent.get().strip(),
            "urgence": urg_ent.get().strip(),
            "description": desc_txt.get("1.0", "end").strip(),
        }

        personnes_raw = personnes_txt.get("1.0", "end").strip()
        if personnes_raw == "":
            new["personnes"] = []
        else:
            new["personnes_raw"] = personnes_raw

        return new

    def on_save(event=None):
        new = _build_new_data_from_widgets()
        if "personnes_raw" in new:
            try:
                personnes_parsed = json.loads(new["personnes_raw"])
                if not isinstance(personnes_parsed, list):
                    raise ValueError("Le champ 'personnes' doit être une liste JSON.")
                new["personnes"] = personnes_parsed
            except Exception as e:
                messagebox.showerror("Erreur JSON", f"Impossible de parser le champ 'personnes' :\n{e}")
                return

        affaire_copy = affaire.copy()
        affaire_copy.update({k: v for k, v in new.items() if k != "personnes_raw"})

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(affaire_copy, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer l'affaire :\n{e}")
            return

        messagebox.showinfo("Succès", "Affaire enregistrée.")
        edit.destroy()
        try:
            parent_popup.destroy()
        except Exception:
            pass
        try:
            ouvrir_affaire(path)
        except Exception:
            pass

    def on_cancel(event=None):
        current = _build_new_data_from_widgets()
        orig_personnes_str = json.dumps(_original_data.get("personnes", []), ensure_ascii=False, indent=2).strip()
        current_personnes_str = current.get("personnes_raw", json.dumps(current.get("personnes", []), ensure_ascii=False, indent=2)).strip()

        modified = (
            current.get("titre", "") != (_original_data.get("titre", "") or "") or
            current.get("date", "") != (_original_data.get("date", "") or "") or
            current.get("lieu", "") != (_original_data.get("lieu", "") or "") or
            current.get("type_affaire", "") != (_original_data.get("type_affaire", "") or "") or
            current.get("responsables", "") != (_original_data.get("responsables", "") or "") or
            current.get("etat", "") != (_original_data.get("etat", "") or "") or
            current.get("urgence", "") != (_original_data.get("urgence", "") or "") or
            current.get("description", "") != (_original_data.get("description", "") or "") or
            orig_personnes_str != current_personnes_str
        )

        if modified:
            if not messagebox.askyesno("Annuler", "Des modifications ont été effectuées.\nVoulez-vous quitter sans sauvegarder ?"):
                return
        edit.destroy()

    def on_revert():
        titre_ent.delete(0, "end"); titre_ent.insert(0, _original_data.get("titre", "") or "")
        date_ent.delete(0, "end"); date_ent.insert(0, _original_data.get("date", "") or "")
        lieu_ent.delete(0, "end"); lieu_ent.insert(0, _original_data.get("lieu", "") or "")
        type_ent.delete(0, "end"); type_ent.insert(0, _original_data.get("type_affaire", "") or "")
        resp_ent.delete(0, "end"); resp_ent.insert(0, _original_data.get("responsables", "") or "")
        etat_ent.delete(0, "end"); etat_ent.insert(0, _original_data.get("etat", "") or "")
        urg_ent.delete(0, "end"); urg_ent.insert(0, _original_data.get("urgence", "") or "")
        desc_txt.delete("1.0", "end"); desc_txt.insert("1.0", _original_data.get("description", "") or "")
        personnes_txt.delete("1.0", "end"); personnes_txt.insert("1.0",
            json.dumps(_original_data.get("personnes", []), ensure_ascii=False, indent=2))

    # ======== Zone des boutons fixes ========
    btn_frame = tk.Frame(edit, pady=10)
    btn_frame.pack(fill="x")

    tk.Button(btn_frame, text="💾 Enregistrer", width=14, bg="#cce5ff", command=on_save).pack(side="right", padx=6)
    tk.Button(btn_frame, text="✖ Annuler", width=12, bg="#f8d7da", command=on_cancel).pack(side="right", padx=6)
    tk.Button(btn_frame, text="↺ Revenir", width=10, bg="#e2e3e5", command=on_revert).pack(side="right", padx=6)

    # ======== Raccourcis clavier ========
    edit.bind("<Escape>", on_cancel)
    edit.bind("<Control-s>", on_save)
    edit.bind("<Command-s>", on_save)

    # focus sur le champ titre
    titre_ent.focus_set()
