import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from data.stockage import sauvegarder_affaire


def nouvelle_affaire_interface(fenetre):

    for widget in fenetre.winfo_children():
        widget.destroy()

    fenetre.title("Nouvelle Affaire")

    titre = tk.Label(fenetre, text="Nouvelle Affaire", font=("Arial", 18))
    titre.pack(pady=10)

    frame = tk.Frame(fenetre)
    frame.pack(padx=20, pady=10, fill="both", expand=True)

    # === TITRE ===
    tk.Label(frame, text="Titre de l’affaire :").grid(row=0, column=0, sticky="w")
    entry_titre = tk.Entry(frame, width=50)
    entry_titre.grid(row=0, column=1, pady=5, sticky="w")

    # === DATE ===
    tk.Label(frame, text="Date et heure du signalement :").grid(row=1, column=0, sticky="w")
    entry_date = tk.Entry(frame, width=50)
    entry_date.grid(row=1, column=1, pady=5, sticky="w")

    # === LIEU ===
    tk.Label(frame, text="Lieu de l’incident :").grid(row=2, column=0, sticky="w")
    entry_lieu = tk.Entry(frame, width=50)
    entry_lieu.grid(row=2, column=1, pady=5, sticky="w")

    # === TYPES D’AFFAIRES TRÈS COMPLETS ===
    tk.Label(frame, text="Type d’affaire :").grid(row=3, column=0, sticky="w")

    types_affaires = [
        "🔪 — Infractions contre la personne —",
        *sorted([
            "Homicide involontaire", "Homicide volontaire", "Mutilation / acte de barbarie",
            "Agression physique", "Agression sexuelle / Viol", "Disparition inquiétante",
            "Enlèvement / Séquestration", "Menaces de mort", "Suicide suspect / non élucidé",
            "Tentative de meurtre", "Violences conjugales",
        ]),
        "💼 — Infractions contre les biens —",
        *sorted([
            "Abus de confiance", "Contrefaçon / faux documents", "Détournement de fonds",
            "Escroquerie / fraude", "Extorsion", "Recel de biens volés",
            "Vandalisme / dégradation",
            "Vol à main armée", "Vol avec effraction (cambriolage)",
            "Vol de véhicule", "Vol simple",
        ]),
        "🔥 — Infractions graves / dangers publics —",
        *sorted([
            "Empoisonnement", "Explosion / sabotage", "Incendie volontaire (pyromanie)",
            "Menace d’attentat / acte terroriste", "Mise en danger de la vie d’autrui",
            "Possession d’armes illégales",
        ]),
        "🌐 — Cybercriminalité —",
        *sorted([
            "Accès frauduleux à un système", "Cyberharcèlement",
            "Diffusion de contenus illégaux", "Hameçonnage / fraude en ligne",
            "Piraterie informatique", "Usurpation d’identité"
        ]),
        "🏠 — Infractions familiales / civiles —",
        *sorted([
            "Abandon de famille", "Conflit de garde d’enfant", "Fugue de mineur",
            "Non-présentation d’enfant", "Violences intrafamiliales",
        ]),
        "🚔 — Atteintes à l’ordre public —",
        *sorted([
            "Conduite dangereuse / délit de fuite", "Consommation illégale de stupéfiants",
            "Corruption", "Infraction à la législation sur les étrangers",
            "Rixe / bagarre de rue", "Trafic de stupéfiants",
            "Trouble à l’ordre public", "Violation de domicile",
        ]),
        "⚠️ — Autres / inclassables —",
        *sorted([
            "Affaire confidentielle / sous scellé",
            "Affaire classée non élucidée (réouverture)",
            "Découverte de cadavre", "Demande d’assistance inter-service",
            "Enquête préventive / filature", "Faits inexpliqués / à déterminer",
        ]),
        "✏️ Autre (à préciser)"
    ]

    selected_type = tk.StringVar()
    menu_type = ttk.Combobox(frame, textvariable=selected_type, width=47)
    menu_type["values"] = types_affaires
    menu_type.set("Choisir ou écrire un type d’affaire…")
    menu_type.grid(row=3, column=1, pady=5, sticky="w")

    # === PERSONNES IMPLIQUÉES (VERSION COMPLÈTE !) ===
    tk.Label(frame, text="Personnes impliquées :").grid(row=5, column=0, sticky="nw")

    personnes_frame = tk.Frame(frame)
    personnes_frame.grid(row=5, column=1, sticky="w")

    personnes_data = []

    roles = [
        "🟦 Victime", "🟥 Suspect", "👁️ Témoin", "🚓 Auteur présumé",
        "🧍 Personne d’intérêt", "🧑‍⚖️ Partie civile",
        "🧑‍⚕️ Intervenant externe", "👮 Officier en charge / enquêteur"
    ]

    selected_role = tk.StringVar(value=roles[0])
    role_menu = ttk.Combobox(personnes_frame, textvariable=selected_role, width=22)
    role_menu["values"] = roles
    role_menu.pack(side="left", padx=2)

    entry_nom = tk.Entry(personnes_frame, width=18)
    entry_nom.pack(side="left", padx=5)

    personnes_liste_frame = tk.Frame(frame)
    personnes_liste_frame.grid(row=6, column=1, pady=5, sticky="w")

    def ouvrir_popup(personne_dict):
        popup = tk.Toplevel(fenetre)
        popup.title(f"Détails - {personne_dict['role']} : {personne_dict['nom']}")
        popup.geometry("400x500")

        labels = ["Identité", "Adresse", "Contact"]
        keys = ["identité", "adresse", "contact"]
        entries = {}

        for label, key in zip(labels, keys):
            tk.Label(popup, text=label + " :").pack(anchor="w", padx=10, pady=5)
            e = tk.Entry(popup, width=40)
            e.pack(padx=10)
            e.insert(0, personne_dict[key])
            entries[key] = e

        tk.Label(popup, text="Liens :").pack(anchor="w", padx=10, pady=5)
        entry_liens = tk.Text(popup, width=38, height=4)
        entry_liens.pack(padx=10)
        entry_liens.insert("1.0", personne_dict["liens"])

        tk.Label(popup, text="Historique :").pack(anchor="w", padx=10, pady=5)
        entry_historique = tk.Text(popup, width=38, height=6)
        entry_historique.pack(padx=10)
        entry_historique.insert("1.0", personne_dict["historique"])

        def save():
            for k in keys:
                personne_dict[k] = entries[k].get()
            personne_dict["liens"] = entry_liens.get("1.0", "end").strip()
            personne_dict["historique"] = entry_historique.get("1.0", "end").strip()
            messagebox.showinfo("Enregistré", "Informations mises à jour.")
            popup.destroy()

        tk.Button(popup, text="Enregistrer", command=save).pack(pady=10)

    def ajouter_personne():
        nom = entry_nom.get().strip()
        if not nom:
            messagebox.showwarning("Erreur", "Veuillez indiquer un nom.")
            return

        personne = {
            "role": selected_role.get(),
            "nom": nom,
            "identité": "",
            "adresse": "",
            "contact": "",
            "liens": "",
            "historique": ""
        }
        personnes_data.append(personne)

        ligne = tk.Frame(personnes_liste_frame)
        ligne.pack(fill="x", pady=2)

        tk.Label(ligne, text=f"{personne['role']} : {nom}").pack(side="left")
        tk.Button(ligne, text="Détails", command=lambda p=personne: ouvrir_popup(p)).pack(side="right", padx=5)

        entry_nom.delete(0, tk.END)

    tk.Button(personnes_frame, text="Ajouter", command=ajouter_personne).pack(side="left", padx=5)

    # === DESCRIPTION ===
    tk.Label(frame, text="Description / résumé rapide :").grid(row=7, column=0, sticky="nw")
    entry_desc = tk.Text(frame, width=38, height=5)
    entry_desc.grid(row=7, column=1, pady=5, sticky="w")

    # === RESPONSABLES ===
    tk.Label(frame, text="Responsable(s) de l’affaire :").grid(row=8, column=0, sticky="w")
    entry_resp = tk.Entry(frame, width=50)
    entry_resp.grid(row=8, column=1, pady=5, sticky="w")

    # === PHOTOS ===
    tk.Label(frame, text="Pièces jointes (photos) :").grid(row=9, column=0, sticky="nw")
    photos = []

    def ajouter_photo():
        fichier = filedialog.askopenfilename(
            title="Choisir une photo",
            filetypes=[("Images", "*.jpg *.png *.jpeg *.gif")]
        )
        if fichier:
            photos.append(fichier)
            liste_photos.insert(tk.END, fichier.split("/")[-1])

    tk.Button(frame, text="Ajouter une photo", command=ajouter_photo).grid(row=9, column=1, sticky="w")

    liste_photos = tk.Listbox(frame, width=45, height=3)
    liste_photos.grid(row=10, column=1, pady=5, sticky="w")

    # === ÉTAT ===
    tk.Label(frame, text="État de l’enquête :").grid(row=11, column=0, sticky="w")
    selected_etat = tk.StringVar(value="🟢 En cours")
    tk.OptionMenu(frame, selected_etat, "🟢 En cours", "🟡 À surveiller", "🔵 Gelée — manque d'informations").grid(row=11, column=1, sticky="w")

    # === URGENCE ===
    tk.Label(frame, text="Indicateur d’urgence :").grid(row=12, column=0, sticky="w")
    selected_urgence = tk.StringVar(value="⚪ Faible")
    tk.OptionMenu(frame, selected_urgence, "⚪ Faible", "🟡 Moyen", "🟠 Élevé", "🔴 Critique").grid(row=12, column=1, sticky="w")

    # === BOUTONS ===
    btns = tk.Frame(fenetre)
    btns.pack(pady=20)

    def annuler():
        from gui.accueil import accueil
        if messagebox.askyesno("Annuler", "Voulez-vous vraiment annuler ?"):
            accueil(fenetre)

    tk.Button(btns, text="Annuler", fg="red", width=15, command=annuler).pack(side="left", padx=10)

    def enregistrer():
        if not messagebox.askyesno("Confirmation", "Voulez-vous vraiment enregistrer cette affaire ?"):
            return

        affaire = {
            "titre": entry_titre.get().strip(),
            "date": entry_date.get().strip(),
            "lieu": entry_lieu.get().strip(),
            "type_affaire": selected_type.get(),
            "personnes": personnes_data,
            "description": entry_desc.get("1.0", "end").strip(),
            "responsables": entry_resp.get().strip(),
            "photos": photos,
            "etat": selected_etat.get(),
            "urgence": selected_urgence.get()
        }

        if not affaire["titre"]:
            messagebox.showwarning("Erreur", "Le titre de l'affaire est obligatoire.")
            return

        chemin = sauvegarder_affaire(affaire)

        messagebox.showinfo("Affaire enregistrée", f"L'affaire a été sauvegardée :\n{chemin}")

        from gui.accueil import accueil
        accueil(fenetre)

    tk.Button(btns, text="Enregistrer l’affaire", width=20, command=enregistrer).pack(side="left", padx=10)