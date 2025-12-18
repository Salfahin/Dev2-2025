# ======================================
    #   FILTRE
    # ======================================
    def trier_affaires(liste, critere):
        if critere == "ordre alphabétique":
            return sorted(liste, key=lambda a: a["titre"].lower())
        elif critere == "date":
            return sorted(liste, key=lambda a: a["date_dernier_mouvement"])
        elif critere == "lieu":
            return sorted(liste, key=lambda a: a["lieu"].lower())
        elif critere == "responsable":
            return sorted(liste, key=lambda a: a["responsable"].lower())
        elif critere == "urgence":
            return sorted(liste, key=lambda a: a.get("urgence", 0), reverse=True)
        return liste

    def rafraichir_tri(frame_parent, liste_affaires, critere):
        # Effacer contenu actuel
        for widget in frame_parent.winfo_children():
            widget.destroy()

        liste_triee = trier_affaires(liste_affaires, critere)
        afficher_cartes(frame_parent, liste_triee)

# ======================================
    # SECTIONS AVEC LISTES DÉROULANTES
    # ======================================

    # ----- AFFAIRES EN COURS -----
    frame_titre_en_cours = tk.Frame(frame_global, bg="#f0f0f0")
    frame_titre_en_cours.pack(fill="x", pady=(10, 5))

    tk.Label(
        frame_titre_en_cours,
        text="🟢 Affaires en cours",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0"
    ).pack(side="left")

    var_tri_en_cours = tk.StringVar(value="urgence")
    menu_en_cours = tk.OptionMenu(
        frame_titre_en_cours,
        var_tri_en_cours,
        "ordre alphabétique", "date", "lieu", "responsable", "urgence",
        command=lambda c: rafraichir_tri(frame_en_cours, en_cours, c)
    )
    menu_en_cours.pack(side="right")

    frame_en_cours = tk.Frame(frame_global, bg="#f0f0f0")
    frame_en_cours.pack(fill="x")
    afficher_cartes(frame_en_cours, en_cours)

    # ----- AFFAIRES À SURVEILLER -----
    frame_titre_surveiller = tk.Frame(frame_global, bg="#f0f0f0")
    frame_titre_surveiller.pack(fill="x", pady=(20, 5))

    tk.Label(
        frame_titre_surveiller,
        text="🟡 Affaires à surveiller",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0"
    ).pack(side="left")

    var_tri_surveiller = tk.StringVar(value="urgence")
    menu_surveiller = tk.OptionMenu(
        frame_titre_surveiller,
        var_tri_surveiller,
        "ordre alphabétique", "date", "lieu", "responsable", "urgence",
        command=lambda c: rafraichir_tri(frame_surveiller, surveiller, c)
    )
    menu_surveiller.pack(side="right")

    frame_surveiller = tk.Frame(frame_global, bg="#f0f0f0")
    frame_surveiller.pack(fill="x")
    afficher_cartes(frame_surveiller, surveiller)

    # ----- AFFAIRES GELEES -----
    frame_titre_gelee = tk.Frame(frame_global, bg="#f0f0f0")
    frame_titre_gelee.pack(fill="x", pady=(20, 5))

    tk.Label(
        frame_titre_gelee,
        text="🔵 Affaires gelées",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0"
    ).pack(side="left")

    var_tri_gelee = tk.StringVar(value="urgence")
    menu_gelee = tk.OptionMenu(
        frame_titre_gelee,
        var_tri_gelee,
        "ordre alphabétique", "date", "lieu", "responsable", "urgence",
        command=lambda c: rafraichir_tri(frame_gelee, gelee, c)
    )
    menu_gelee.pack(side="right")

    frame_gelee = tk.Frame(frame_global, bg="#f0f0f0")
    frame_gelee.pack(fill="x")
    afficher_cartes(frame_gelee, gelee)