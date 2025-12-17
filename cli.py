import os
from core.services.affaire_service import AffaireService
from core.services.storage_service import StorageService
from core.models.affaire import Affaire
from core.models.personne import Personne
from datetime import datetime
from typing import Optional


#Validation de la date et l'heure
def parse_date_cli(text: str) -> datetime:
    """
    Parse une date au format strict YYYY-MM-DD HH:MM.
    Lève ValueError si invalide (jour 32, heure 25, etc.).
    """
    text = (text or "").strip()
    return datetime.strptime(text, "%Y-%m-%d %H:%M")

#Bon format pour la date et l'heure
def input_date_cli(prompt: str, default: Optional[str] = None, allow_empty: bool = False) -> str:
    """
    Demande une date à l'utilisateur, valide le format et les bornes.
    Retourne une chaîne au format 'YYYY-MM-DD HH:MM' (pas un datetime) pour rester
    compatible avec votre modèle (Affaire.date est un str).
    """
    while True:
        if default:
            raw = input(f"{prompt} [{default}] : ").strip()
            if raw == "" and default is not None:
                raw = default
        else:
            raw = input(f"{prompt} : ").strip()

        if raw == "":
            if allow_empty:
                return ""
            print("❌ Date obligatoire. Format attendu : YYYY-MM-DD HH:MM")
            continue

        try:
            dt = parse_date_cli(raw)
            return dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            print("❌ Date invalide.")
            print("   Format attendu : YYYY-MM-DD HH:MM (ex: 2025-12-16 14:30)")
            print("   Rappel : jour 1-31, heure 0-23, minute 0-59.")




def main():
    # Initialisation des services avec le même dossier de données que la GUI
    base_path = os.path.join("data", "affaires")
    service = AffaireService(StorageService(base_path))
    
    current_list = []  # mémorise la dernière liste d’Affaire affichées (pour sélection/suppression)
    
    while True:
        # Affichage du menu principal
        print("\n=== Menu AffairTrack CLI ===")
        print("Fonctionnement : D'abord choisir l'état de l'affaire (1-4) puis -> Détails/Modifier(6) ou Supprimer(7) -> n° de l'affaire")
        print("1. Afficher affaires en cours")
        print("2. Afficher affaires à surveiller")
        print("3. Afficher affaires gelées")
        print("4. Afficher affaires classées")
        print("5. Créer une nouvelle affaire")
        print("6. Sélectionner une affaire par numéro (détails/modification)")
        print("7. Supprimer une affaire")
        print("8. Quitter")
        choix = input("Votre choix : ").strip()
        
        #------------------------------------------------------
        # AFFICHER LES 4 TYPES D'ETAT D'AFFAIRES
        #------------------------------------------------------

        if choix == '1':  # Afficher affaires en cours
            affaires = service.get_all()  # charge toutes les affaires:
            en_cours, surveiller, gelee = service.trier_par_etat(affaires)  # tri par état:contentReference[oaicite:31]{index=31}
            current_list = en_cours  # on mémorise cette liste courante
            print("\n🟢 Affaires en cours :")
            if not en_cours:
                print("Aucune affaire en cours.")
            else:
                for i, aff in enumerate(en_cours, start=1):
                    # Affichage résumé de l'affaire (numéro, titre, lieu, type, responsable, etc.)
                    victimes = aff.nombre_victimes()
                    suspects = aff.nombre_suspects()
                    temoins = aff.nombre_temoins()
                    print(f"{i}. {aff.titre} — Lieu: {aff.lieu}, Type: {aff.type_affaire}, "
                          f"Responsable: {aff.responsables}, "
                          f"Victimes: {victimes}, Suspects: {suspects}, Témoins: {temoins}, "
                          f"Urgence: {aff.urgence}")
        
        elif choix == '2':  # Afficher affaires à surveiller
            affaires = service.get_all()
            en_cours, surveiller, gelee = service.trier_par_etat(affaires)
            current_list = surveiller
            print("\n🟡 Affaires à surveiller :")
            if not surveiller:
                print("Aucune affaire à surveiller.")
            else:
                for i, aff in enumerate(surveiller, start=1):
                    print(f"{i}. {aff.titre} — Lieu: {aff.lieu}, Type: {aff.type_affaire}, "
                          f"Responsable: {aff.responsables}, "
                          f"Victimes: {aff.nombre_victimes()}, Suspects: {aff.nombre_suspects()}, "
                          f"Témoins: {aff.nombre_temoins()}, Urgence: {aff.urgence}")
        
        elif choix == '3':  # Afficher affaires gelées
            affaires = service.get_all()
            en_cours, surveiller, gelee = service.trier_par_etat(affaires)
            current_list = gelee
            print("\n🔵 Affaires gelées :")
            if not gelee:
                print("Aucune affaire gelée.")
            else:
                for i, aff in enumerate(gelee, start=1):
                    print(f"{i}. {aff.titre} — Lieu: {aff.lieu}, Type: {aff.type_affaire}, "
                          f"Responsable: {aff.responsables}, "
                          f"Victimes: {aff.nombre_victimes()}, Suspects: {aff.nombre_suspects()}, "
                          f"Témoins: {aff.nombre_temoins()}, Urgence: {aff.urgence}")
        
        elif choix == '4':  # Afficher affaires classées
            affaires = service.get_all()
            classees = service.affaires_classees(affaires)  # filtre les affaires classées:contentReference[oaicite:32]{index=32}
            current_list = classees
            print("\n🟣 Affaires classées :")
            if not classees:
                print("Aucune affaire classée.")
            else:
                for i, aff in enumerate(classees, start=1):
                    print(f"{i}. {aff.titre} — Lieu: {aff.lieu}, Type: {aff.type_affaire}, "
                          f"Responsable: {aff.responsables}, "
                          f"Victimes: {aff.nombre_victimes()}, Suspects: {aff.nombre_suspects()}, "
                          f"Témoins: {aff.nombre_temoins()}, Urgence: {aff.urgence}")
        
        #----------------------------------------------------------------
        # CREATION AFFAIRE
        #----------------------------------------------------------------

        elif choix == '5':  # Créer une nouvelle affaire
            # Saisie des champs principaux
            print("\n*** Création d'une nouvelle affaire ***")
            titre = ""
            while not titre:
                titre = input("Titre de l’affaire (obligatoire) : ").strip()
                if not titre:
                    print("Le titre est obligatoire, veuillez saisir un titre.")
            date = input_date_cli("Date et heure du signalement (YYYY-MM-DD HH:MM)")
            lieu = input("Lieu de l’incident : ").strip()
            # Type d'affaire (liste d'options suggérées)
            types_affaires = ["Homicide", "Agression", "Vol", "Fraude", "Divers"]
            type_aff = input(f"Type d’affaire ({', '.join(types_affaires)} ou autre) : ").strip()
            if not type_aff:
                type_aff = "Divers"
            # Description
            description = input("Description de l’affaire : ").strip()
            # Responsables
            responsables = input("Responsable(s) de l’affaire : ").strip()
            # État initial (menu numérique)
            etat_choix = { "1": "🟢 En cours", "2": "🟡 À surveiller", "3": "🔵 Gelée — manque d'informations" }
            etat_input = input("État initial [1=En cours, 2=À surveiller, 3=Gelée] (défaut 1) : ").strip()
            etat = etat_choix.get(etat_input, "🟢 En cours")
            # Urgence initiale (menu numérique)
            urgence_choix = { "1": "⚪ Faible", "2": "🟡 Moyen", "3": "🟠 Élevé", "4": "🔴 Critique" }
            urg_input = input("Niveau d'urgence [1=Faible, 2=Moyen, 3=Élevé, 4=Critique] (défaut 1) : ").strip()
            urgence = urgence_choix.get(urg_input, "⚪ Faible")
            # Personnes impliquées
            personnes = []
            while True:
                add_person = input("Ajouter une personne impliquée ? (o/n) : ").strip().lower()
                if add_person == 'o' or add_person == 'oui':
                    # Rôle de la personne (on propose quelques rôles courants)
                    roles = ["Victime", "Suspect", "Témoin", "Auteur présumé", "Officier"]
                    role = input(f" - Rôle de la personne ({', '.join(roles)}) : ").strip()
                    if not role:
                        role = "Témoin"  # rôle par défaut si vide
                    nom = input(" - Nom de la personne : ").strip()
                    if not nom:
                        print("Nom requis pour ajouter une personne. Abandon de l'ajout.")
                    else:
                        # On ne demande pas identité, adresse, etc. ici (elles pourront être modifiées plus tard)
                        personnes.append(Personne(role=role, nom=nom))
                        print(f"Personne ajoutée : {role} – {nom}")
                    continue  # redemander si on veut ajouter une autre personne
                break  # si l'utilisateur répond 'n', on sort de la boucle d'ajout
            # Photos / pièces jointes
            photos = []
            while True:
                add_photo = input("Ajouter une photo/pièce jointe ? (o/n) : ").strip().lower()
                if add_photo == 'o' or add_photo == 'oui':
                    photo_path = input(" - Chemin ou nom du fichier photo : ").strip()
                    if photo_path:
                        photos.append(photo_path)
                        print(f"Photo ajoutée : {photo_path}")
                    else:
                        print("Chemin de photo vide, aucune photo ajoutée.")
                    continue
                break
            # Création de l'objet Affaire et sauvegarde
            nouvelle_affaire = Affaire(
                titre=titre,
                date=date,
                lieu=lieu,
                type_affaire=type_aff,
                description=description,
                responsables=responsables,
                personnes=personnes,
                photos=photos,
                etat=etat,
                urgence=urgence
            )
            service.save(nouvelle_affaire)  # sauvegarde dans data/affaires (JSON):contentReference[oaicite:33]{index=33}
            print(f"Affaire '{titre}' créée avec succès.")
        
        #----------------------------------------------------------------
        # SELECTIONNER UNE AFFAIRE PAR SON NUM ET LA MODIFIER
        #----------------------------------------------------------------

        elif choix == '6':  # Sélectionner une affaire par son numéro
            if not current_list:
                # Si aucune liste courante, on charge toutes les affaires
                current_list = service.get_all()
                # On pourrait afficher toutes les affaires ici, mais on suppose que l'utilisateur a listé avant
            if not current_list:
                print("Aucune affaire disponible à sélectionner.")
                continue
            num = input("Numéro de l’affaire à ouvrir : ").strip()
            if not num.isdigit():
                print("Veuillez entrer un numéro valide.")
                continue
            idx = int(num)
            if idx < 1 or idx > len(current_list):
                print("Numéro invalide. Veuillez réessayer.")
                continue
            affaire = current_list[idx-1]
            # Affichage détaillé de l'affaire sélectionnée
            print(f"\n*** Détails de l’affaire '{affaire.titre}' ***")
            print(f"Titre : {affaire.titre}")
            print(f"Date : {affaire.date or '—'}")
            print(f"Lieu : {affaire.lieu or '—'}")
            print(f"Type d’affaire : {affaire.type_affaire or '—'}")
            print(f"Responsable(s) : {affaire.responsables or '—'}")
            print(f"État : {affaire.etat}")
            print(f"Urgence : {affaire.urgence}")
            print(f"Description : {affaire.description or 'Aucune description fournie.'}")
            # Personnes impliquées
            if affaire.personnes:
                print("Personnes impliquées :")
                for p in affaire.personnes:
                    print(f" - {p.role} – {p.nom}")
                    if p.identité:
                        print(f"    Identité : {p.identité}")
                    if p.adresse:
                        print(f"    Adresse : {p.adresse}")
                    if p.contact:
                        print(f"    Contact : {p.contact}")
                    if p.liens:
                        print(f"    Liens : {p.liens}")
                    if p.historique:
                        print(f"    Notes : {p.historique}")
            else:
                print("Personnes impliquées : Aucune personne enregistrée.")
            # Photos
            if affaire.photos:
                print("Pièces jointes :")
                for ph in affaire.photos:
                    print(f" - {ph}")
            else:
                print("Pièces jointes : Aucune photo enregistrée.")

            #------------------
            #MODIFIER L'AFFAIRE
            #------------------
            # Proposer modification éventuelle
            modif = input("\nModifier cette affaire ? (o/n) : ").strip().lower()
            if modif == 'o' or modif == 'oui':
                # Modification champ par champ
                print("** Mode édition – appuyez Entrée pour conserver la valeur actuelle **")
                new_titre = input(f"Titre [{affaire.titre}] : ").strip()
                if new_titre:
                    affaire.titre = new_titre
                new_date = input_date_cli("Date et heure (YYYY-MM-DD HH:MM)", default=affaire.date, allow_empty=False)
                affaire.date = new_date
                if new_date:
                    affaire.date = new_date
                new_lieu = input(f"Lieu [{affaire.lieu}] : ").strip()
                if new_lieu:
                    affaire.lieu = new_lieu
                new_type = input(f"Type d’affaire [{affaire.type_affaire}] : ").strip()
                if new_type:
                    affaire.type_affaire = new_type
                new_desc = input(f"Description (laisser vide si inchangée) : ").strip()
                if new_desc:
                    affaire.description = new_desc
                new_resps = input(f"Responsable(s) [{affaire.responsables}] : ").strip()
                if new_resps:
                    affaire.responsables = new_resps
                # État (choix numérique)
                etat_map = {"1": "🟢 En cours", "2": "🟡 À surveiller", "3": "🔵 Gelée — manque d'informations", "4": "🟣 Affaire classée"}
                new_etat = input(f"État actuel [{affaire.etat}] (1=En cours, 2=À surveiller, 3=Gelée, 4=Classée) : ").strip()
                if new_etat and new_etat in etat_map:
                    affaire.etat = etat_map[new_etat]
                # Urgence (choix numérique)
                urg_map = {"1": "⚪ Faible", "2": "🟡 Moyen", "3": "🟠 Élevé", "4": "🔴 Critique"}
                new_urg = input(f"Urgence actuelle [{affaire.urgence}] (1=Faible, 2=Moyen, 3=Élevé, 4=Critique) : ").strip()
                if new_urg and new_urg in urg_map:
                    affaire.urgence = urg_map[new_urg]
                # Modification de la liste des personnes
                if affaire.personnes:
                    print("Liste actuelle des personnes :")
                    for idx_p, pers in enumerate(affaire.personnes, start=1):
                        print(f"   {idx_p}. {pers.role} – {pers.nom}")
                pers_choix = input("Modifier les personnes ? (A=ajouter, R=retirer, autre pour ignorer) : ").strip().lower()
                if pers_choix == 'a':  # ajouter personne
                    role = input(" - Rôle de la nouvelle personne : ").strip()
                    if not role:
                        role = "Témoin"
                    nom = input(" - Nom de la nouvelle personne : ").strip()
                    if nom:
                        affaire.personnes.append(Personne(role=role, nom=nom))
                        print(f"Personne ajoutée : {role} – {nom}")
                elif pers_choix == 'r':  # retirer personne
                    rem_index = input("Numéro de la personne à retirer : ").strip()
                    if rem_index.isdigit():
                        rem_index = int(rem_index)
                        if 1 <= rem_index <= len(affaire.personnes):
                            pers = affaire.personnes.pop(rem_index-1)
                            print(f"Personne supprimée : {pers.role} – {pers.nom}")
                # Modification des photos
                if affaire.photos:
                    print("Photos actuelles :")
                    for idx_ph, ph in enumerate(affaire.photos, start=1):
                        print(f"   {idx_ph}. {ph}")
                photo_choix = input("Modifier les pièces jointes ? (A=ajouter, R=retirer, autre pour ignorer) : ").strip().lower()
                if photo_choix == 'a':
                    ph_path = input(" - Chemin de la nouvelle photo : ").strip()
                    if ph_path:
                        affaire.photos.append(ph_path)
                        print(f"Photo ajoutée : {ph_path}")
                elif photo_choix == 'r':
                    rem_ph = input("Numéro de la photo à retirer : ").strip()
                    if rem_ph.isdigit():
                        rem_ph = int(rem_ph)
                        if 1 <= rem_ph <= len(affaire.photos):
                            ph = affaire.photos.pop(rem_ph-1)
                            print(f"Photo supprimée : {ph}")
                # Enregistrer les modifications
                if not affaire.titre:
                    print("Titre vide après modification - opération annulée.")
                else:
                    service.save(affaire)  # sauvegarde les changements:contentReference[oaicite:34]{index=34}
                    print("Affaire mise à jour avec succès.")
        
        #-------------------------------------------------------------------
        # SUPPRIMER AFFAIRE
        #-------------------------------------------------------------------

        elif choix == '7':  # Supprimer une affaire
            if not current_list:
                affaires = service.get_all()
                current_list = affaires
            if not current_list:
                print("Aucune affaire à supprimer.")
                continue
            num = input("Numéro de l’affaire à supprimer : ").strip()
            if not num.isdigit():
                print("Veuillez entrer un numéro valide.")
                continue
            index = int(num)
            if index < 1 or index > len(current_list):
                print("Numéro invalide.")
                continue
            affaire = current_list[index-1]
            confirm = input(f"Confirmez-vous la suppression de '{affaire.titre}' ? (o/n) : ").strip().lower()
            if confirm == 'o' or confirm == 'oui':
                service.delete(affaire)  # suppression du fichier JSON:contentReference[oaicite:35]{index=35}
                print("Affaire supprimée.")
                # Mettre à jour la liste courante pour ne plus inclure cette affaire
                try:
                    current_list.remove(affaire)
                except ValueError:
                    current_list = []
            else:
                print("Suppression annulée.")
        
        #----------------------------------------------------------------
        #   QUITTER
        #----------------------------------------------------------------
        elif choix == '8':  # Quitter
            print("Au revoir !")
            break
        else:
            print("Choix non reconnu, veuillez entrer un numéro de 1 à 8.")

if __name__ == "__main__":
    main()
