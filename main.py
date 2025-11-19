import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.ttk as ttk

def changer_interface():
    # Effacer l’accueil
    for widget in fenetre.winfo_children():
        widget.destroy()

    fenetre.title("Nouvelle Affaire")

    titre = tk.Label(fenetre, text="Nouvelle Affaire", font=("Arial", 18))
    titre.pack(pady=10)

    frame = tk.Frame(fenetre)
    frame.pack(padx=20, pady=10, fill="both", expand=True)

    # >>> Titre de l’affaire
    tk.Label(frame, text="Titre de l’affaire :").grid(row=0, column=0, sticky="w")
    entry_titre = tk.Entry(frame, width=50)
    entry_titre.grid(row=0, column=1, pady=5, sticky="w")

    # >>> Date et heure du signalement
    tk.Label(frame, text="Date et heure du signalement :").grid(row=1, column=0, sticky="w")
    entry_date = tk.Entry(frame, width=50)
    entry_date.grid(row=1, column=1, pady=5, sticky="w")

    # >>> Lieu de l’incident
    tk.Label(frame, text="Lieu de l’incident :").grid(row=2, column=0, sticky="w")
    entry_lieu = tk.Entry(frame, width=50)
    entry_lieu.grid(row=2, column=1, pady=5, sticky="w")

    # >>> TYPE D’AFFAIRE (Combobox + catégories + emojis)
    tk.Label(frame, text="Type d’affaire :").grid(row=3, column=0, sticky="w")

    types_affaires = [

        "🔪 — Infractions contre la personne —",
        *sorted([
            "Homicide involontaire",
            "Homicide volontaire",
            "Mutilation / acte de barbarie",
            "Agression physique",
            "Agression sexuelle / Viol",
            "Disparition inquiétante",
            "Enlèvement / Séquestration",
            "Menaces de mort",
            "Suicide suspect / non élucidé",
            "Tentative de meurtre",
            "Violences conjugales",
        ]),

        "💼 — Infractions contre les biens —",
        *sorted([
            "Abus de confiance",
            "Contrefaçon / faux documents",
            "Détournement de fonds",
            "Escroquerie / fraude",
            "Extorsion",
            "Recel de biens volés",
            "Vandalisme / dégradation",
            "Vol à main armée",
            "Vol avec effraction (cambriolage)",
            "Vol de véhicule",
            "Vol simple",
        ]),

        "🔥 — Infractions graves / dangers publics —",
        *sorted([
            "Empoisonnement",
            "Explosion / sabotage",
            "Incendie volontaire (pyromanie)",
            "Menace d’attentat / acte terroriste",
            "Mise en danger de la vie d’autrui",
            "Possession d’armes illégales",
        ]),

        "🌐 — Cybercriminalité —",
        *sorted([
            "Accès frauduleux à un système",
            "Cyberharcèlement",
            "Diffusion de contenus illégaux",
            "Hameçonnage / fraude en ligne",
            "Piraterie informatique",
            "Usurpation d’identité",
        ]),

        "🏠 — Infractions familiales / civiles —",
        *sorted([
            "Abandon de famille",
            "Conflit de garde d’enfant",
            "Fugue de mineur",
            "Non-présentation d’enfant",
            "Violences intrafamiliales",
        ]),

        "🚔 — Atteintes à l’ordre public —",
        *sorted([
            "Conduite dangereuse / délit de fuite",
            "Consommation illégale de stupéfiants",
            "Corruption",
            "Infraction à la législation sur les étrangers",
            "Rixe / bagarre de rue",
            "Trafic de stupéfiants",
            "Trouble à l’ordre public",
            "Violation de domicile",
        ]),

        "⚠️ — Autres / inclassables —",
        *sorted([
            "Affaire confidentielle / sous scellé",
            "Affaire classée non élucidée (réouverture)",
            "Découverte de cadavre",
            "Demande d’assistance inter-service",
            "Enquête préventive / filature",
            "Faits inexpliqués / à déterminer",
        ]),

        "✏️ Autre (à préciser)"
    ]

    selected_type = tk.StringVar()
    menu_type = ttk.Combobox(frame, textvariable=selected_type, width=47)
    menu_type['values'] = types_affaires
    menu_type.set("Choisir ou écrire un type d’affaire…")
    menu_type.grid(row=3, column=1, pady=5, sticky="w")

    # >>> Premier agent
    tk.Label(frame, text="Premier agent sur place :").grid(row=4, column=0, sticky="w")
    entry_agent = tk.Entry(frame, width=50)
    entry_agent.grid(row=4, column=1, pady=5, sticky="w")

    # >>> Personnes impliquées (tous les rôles possibles)
    tk.Label(frame, text="Personnes impliquées :").grid(row=5, column=0, sticky="nw")

    # Frame pour aligner Role + Nom + Ajouter
    ligne_personne = tk.Frame(frame)
    ligne_personne.grid(row=5, column=1, sticky="w")

    # Liste des rôles
    roles = [
        "🟦 Victime",
        "🟥 Suspect",
        "👁️ Témoin",
        "🚓 Auteur présumé",
        "🧍 Personne d’intérêt",
        "🧑‍⚖️ Partie civile",
        "🧑‍⚕️ Intervenant externe",
        "👮 Officier en charge / enquêteur"
    ]

    selected_role = tk.StringVar(value=roles[0])

    # --- Menu déroulant (raccourci pour être plus compact)
    role_menu = ttk.Combobox(ligne_personne, textvariable=selected_role, width=22)
    role_menu['values'] = roles
    role_menu.pack(side="left", padx=2)

    # --- Champ nom (compact)
    entry_nom_personne = tk.Entry(ligne_personne, width=18)
    entry_nom_personne.pack(side="left", padx=5)

    # --- Zone d’affichage des personnes
    personnes_frame = tk.Frame(frame)
    personnes_frame.grid(row=6, column=1, pady=5, sticky="w")

    # --- Base de données temporaire
    personnes_data = []

    # POPUP DÉTAILS
    def ouvrir_popup(personne_dict):
        popup = tk.Toplevel(fenetre)
        popup.title(f"Détails - {personne_dict['role']} : {personne_dict['nom']}")
        popup.geometry("400x500")

        tk.Label(popup, text="Identité :").pack(anchor="w", padx=10, pady=5)
        entry_identite = tk.Entry(popup, width=40)
        entry_identite.pack(padx=10)
        entry_identite.insert(0, personne_dict["identité"])

        tk.Label(popup, text="Adresse :").pack(anchor="w", padx=10, pady=5)
        entry_adresse = tk.Entry(popup, width=40)
        entry_adresse.pack(padx=10)
        entry_adresse.insert(0, personne_dict["adresse"])

        tk.Label(popup, text="Contact :").pack(anchor="w", padx=10, pady=5)
        entry_contact = tk.Entry(popup, width=40)
        entry_contact.pack(padx=10)
        entry_contact.insert(0, personne_dict["contact"])

        tk.Label(popup, text="Liens avec d’autres personnes impliquées :").pack(anchor="w", padx=10, pady=5)
        entry_liens = tk.Text(popup, width=38, height=4)
        entry_liens.pack(padx=10)
        entry_liens.insert("1.0", personne_dict["liens"])

        tk.Label(popup, text="Historique des interactions :").pack(anchor="w", padx=10, pady=5)
        entry_historique = tk.Text(popup, width=38, height=6)
        entry_historique.pack(padx=10)
        entry_historique.insert("1.0", personne_dict["historique"])

        def save():
            personne_dict["identité"] = entry_identite.get()
            personne_dict["adresse"] = entry_adresse.get()
            personne_dict["contact"] = entry_contact.get()
            personne_dict["liens"] = entry_liens.get("1.0", "end").strip()
            personne_dict["historique"] = entry_historique.get("1.0", "end").strip()
            messagebox.showinfo("Enregistré", "Les informations ont été mises à jour.")
            popup.destroy()

        tk.Button(popup, text="Enregistrer", command=save).pack(pady=10)

    # AJOUT D’UNE PERSONNE
    def ajouter_personne():
        role = selected_role.get()
        nom = entry_nom_personne.get().strip()

        if nom == "":
            messagebox.showwarning("Erreur", "Veuillez indiquer un nom.")
            return

        personne_dict = {
            "role": role,
            "nom": nom,
            "identité": "",
            "adresse": "",
            "contact": "",
            "liens": "",
            "historique": ""
        }
        personnes_data.append(personne_dict)

        ligne = tk.Frame(personnes_frame)
        ligne.pack(fill="x", pady=2)

        tk.Label(ligne, text=f"{role} : {nom}", anchor="w").pack(side="left")
        tk.Button(ligne, text="Détails", command=lambda p=personne_dict: ouvrir_popup(p)).pack(side="right", padx=5)

        entry_nom_personne.delete(0, tk.END)

    # BOUTON ajouter (aligné juste à côté)
    btn_ajouter_personne = tk.Button(ligne_personne, text="Ajouter", command=ajouter_personne)
    btn_ajouter_personne.pack(side="left", padx=5)

    # >>> Description rapide (corrigé : déplacé à row=7)
    tk.Label(frame, text="Description / résumé rapide :").grid(row=7, column=0, sticky="nw")
    entry_desc = tk.Text(frame, width=38, height=5)
    entry_desc.grid(row=7, column=1, pady=5, sticky="w")

    # >>> Responsable(s)
    tk.Label(frame, text="Responsable(s) de l’affaire :").grid(row=8, column=0, sticky="w")
    entry_resp = tk.Entry(frame, width=50)
    entry_resp.grid(row=8, column=1, pady=5, sticky="w")

    # >>> Photos
    def ajouter_photo():
        fichier = filedialog.askopenfilename(
            title="Choisir une photo",
            filetypes=[("Images", "*.jpg *.png *.jpeg *.gif")]
        )
        if fichier:
            photos.append(fichier)
            liste_photos.insert(tk.END, fichier.split("/")[-1])

    tk.Label(frame, text="Pièces jointes (photos) :").grid(row=9, column=0, sticky="nw")
    photos = []
    btn_photo = tk.Button(frame, text="Ajouter une photo", command=ajouter_photo)
    btn_photo.grid(row=9, column=1, sticky="w")
    liste_photos = tk.Listbox(frame, width=45, height=3)
    liste_photos.grid(row=10, column=1, pady=5, sticky="w")

    # >>> État de l’enquête
    etats = ["🟢 En cours", "🟡 À surveiller", "🔵 Gelée — manque d'informations"]

    tk.Label(frame, text="État de l’enquête :").grid(row=11, column=0, sticky="w")
    selected_etat = tk.StringVar(value=etats[0])
    menu_etat = tk.OptionMenu(frame, selected_etat, *etats)
    menu_etat.grid(row=11, column=1, pady=5, sticky="w")

    # >>> Urgence
    niveaux_urgence = ["⚪ Faible", "🟡 Moyen", "🟠 Élevé", "🔴 Critique"]

    tk.Label(frame, text="Indicateur d’urgence :").grid(row=12, column=0, sticky="w")
    selected_urgence = tk.StringVar(value=niveaux_urgence[0])
    menu_urg = tk.OptionMenu(frame, selected_urgence, *niveaux_urgence)
    menu_urg.grid(row=12, column=1, pady=5, sticky="w")

    # --- Enregistrer ---
    def enregistrer():
        messagebox.showinfo("Affaire enregistrée", "L'affaire a été enregistrée avec succès !")

    btn_save = tk.Button(fenetre, text="Enregistrer l’affaire", command=enregistrer)
    btn_save.pack(pady=20)


# --- ACCUEIL ---
fenetre = tk.Tk()
fenetre.title("AffairTrack")
fenetre.geometry("650x700")

bouton = tk.Button(fenetre, text="Nouvelle Affaire", command=changer_interface)
bouton.pack(fill="x", padx=20, pady=20)

label1 = tk.Label(fenetre, text="Affaires en cours", anchor="w")
label1.pack(fill="x", padx=20, pady=20)

label2 = tk.Label(fenetre, text="Affaires à surveiller", anchor="w")
label2.pack(fill="x", padx=20, pady=20)

label3 = tk.Label(fenetre, text="Affaires gelées pour manque d'informations", anchor="w")
label3.pack(fill="x", padx=20, pady=20)

fenetre.mainloop()