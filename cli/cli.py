import os
from datetime import datetime
from typing import Optional

from core.services.affaire_service import AffaireService
from core.services.storage_service import StorageService
from core.models.affaire import Affaire
from core.models.personne import Personne
from core.models.arme import Arme, ArmeValidationError


# =========================================================
#   OUTILS : DATE
# =========================================================

def parse_date_cli(text: str) -> datetime:
    """
    Parse une date au format strict YYYY-MM-DD HH:MM.
    Lève ValueError si invalide (jour 32, heure 25, etc.).
    """
    text = (text or "").strip()
    return datetime.strptime(text, "%Y-%m-%d %H:%M")


def input_date_cli(prompt: str, default: Optional[str] = None, allow_empty: bool = False) -> str:
    """
    Demande une date à l'utilisateur, valide le format et les bornes.
    Retourne une chaîne au format 'YYYY-MM-DD HH:MM' (pas un datetime).
    """
    while True:
        if default is not None:
            raw = input(f"{prompt} [{default}] : ").strip()
            if raw == "":
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


# =========================================================
#   MENUS : GESTION ARMES / PERSONNES
# =========================================================

def gerer_armes_cli(armes: list[Arme]) -> None:
    """Menu CLI pour gérer les armes (ajout / suppression)."""
    while True:
        print("\n🔫 Gestion des armes")
        if armes:
            for i, a in enumerate(armes, start=1):
                print(f"  {i}. {a.type_arme or '—'} – {a.nom_arme or '—'} (#{a.serie_id_arme or '—'})")
        else:
            print("  Aucune arme enregistrée.")

        print("\nActions :")
        print("  A - Ajouter une arme")
        print("  S - Supprimer une arme")
        print("  Q - Quitter")

        choix = input("Votre choix : ").strip().lower()

        if choix == "a":
            try:
                type_arme = input("Type d'arme : ").strip()
                nom_arme = input("Nom de l'arme : ").strip()
                serie = input("Numéro de série : ").strip()

                a = Arme()
                # IMPORTANT : nom + série puis type (car validation dans les setters)
                a.nom_arme = nom_arme
                a.serie_id_arme = serie
                a.type_arme = type_arme

                armes.append(a)
                print("✅ Arme ajoutée.")

            except ArmeValidationError as e:
                print(f"❌ Arme invalide : {e}")

        elif choix == "s":
            if not armes:
                print("❌ Aucune arme à supprimer.")
                continue

            idx = input("Numéro de l'arme à supprimer : ").strip()
            if not idx.isdigit():
                print("Veuillez entrer un numéro valide.")
                continue

            idx = int(idx)
            if 1 <= idx <= len(armes):
                suppr = armes.pop(idx - 1)
                print(f"🗑 Arme supprimée : {suppr.type_arme} – {suppr.nom_arme}")
            else:
                print("Numéro invalide.")

        elif choix == "q":
            break
        else:
            print("Choix invalide.")


def gerer_personnes_cli(personnes: list[Personne]) -> None:
    """Menu CLI pour gérer les personnes (ajout / suppression)."""
    roles = ["Victime", "Suspect", "Témoin", "Auteur présumé", "Officier", "Enquêteur", "Expert"]

    while True:
        print("\n👤 Gestion des personnes")
        if personnes:
            for i, p in enumerate(personnes, start=1):
                print(f"  {i}. {p.role} – {p.nom}")
        else:
            print("  Aucune personne enregistrée.")

        print("\nActions :")
        print("  A - Ajouter une personne")
        print("  S - Supprimer une personne")
        print("  Q - Quitter")

        choix = input("Votre choix : ").strip().lower()

        if choix == "a":
            role = input(f"Rôle ({', '.join(roles)}) : ").strip()
            if not role:
                role = "Témoin"

            nom = input("Nom : ").strip()
            if not nom:
                print("❌ Nom obligatoire.")
                continue

            # (tu peux compléter identité/adresse/contact plus tard via GUI)
            personnes.append(Personne(role=role, nom=nom))
            print("✅ Personne ajoutée.")

        elif choix == "s":
            if not personnes:
                print("❌ Aucune personne à supprimer.")
                continue

            idx = input("Numéro de la personne à supprimer : ").strip()
            if not idx.isdigit():
                print("Veuillez entrer un numéro valide.")
                continue

            idx = int(idx)
            if 1 <= idx <= len(personnes):
                suppr = personnes.pop(idx - 1)
                print(f"🗑 Personne supprimée : {suppr.role} – {suppr.nom}")
            else:
                print("Numéro invalide.")

        elif choix == "q":
            break
        else:
            print("Choix invalide.")


# =========================================================
#   AFFICHAGE DETAIL
# =========================================================

def afficher_armes(affaire: Affaire) -> None:
    print("Armes impliquées :")
    if affaire.armes:
        for i, a in enumerate(affaire.armes, start=1):
            print(f" - {i}. {a.type_arme or '—'} – {a.nom_arme or '—'} (N° série: {a.serie_id_arme or '—'})")
    else:
        print(" - Aucune arme enregistrée.")


def afficher_personnes(affaire: Affaire) -> None:
    if affaire.personnes:
        print("Personnes impliquées :")
        for p in affaire.personnes:
            print(f" - {p.role} – {p.nom}")
            if getattr(p, "identité", None):
                print(f"    Identité : {p.identité}")
            if getattr(p, "adresse", None):
                print(f"    Adresse : {p.adresse}")
            if getattr(p, "contact", None):
                print(f"    Contact : {p.contact}")
            if getattr(p, "liens", None):
                print(f"    Liens : {p.liens}")
            if getattr(p, "historique", None):
                print(f"    Notes : {p.historique}")
    else:
        print("Personnes impliquées : Aucune personne enregistrée.")


# =========================================================
#   MAIN
# =========================================================

def main():
    base_path = os.path.join("data", "affaires")
    service = AffaireService(StorageService(base_path))

    current_list: list[Affaire] = []

    while True:
        print("\n=== Menu AffairTrack CLI ===")
        print("Fonctionnement : choisir l'état (1-4) puis -> Détails/Modifier(6) ou Supprimer(7) -> n°")
        print("1. Afficher affaires en cours")
        print("2. Afficher affaires à surveiller")
        print("3. Afficher affaires gelées")
        print("4. Afficher affaires classées")
        print("5. Créer une nouvelle affaire")
        print("6. Sélectionner une affaire par numéro (détails/modification)")
        print("7. Supprimer une affaire")
        print("8. Quitter")
        choix = input("Votre choix : ").strip()

        # ----------------------------
        # LISTES / FILTRES
        # ----------------------------
        if choix in ("1", "2", "3"):
            affaires = service.get_all()
            en_cours, surveiller, gelee = service.trier_par_etat(affaires)

            if choix == "1":
                current_list = en_cours
                print("\n🟢 Affaires en cours :")
            elif choix == "2":
                current_list = surveiller
                print("\n🟡 Affaires à surveiller :")
            else:
                current_list = gelee
                print("\n🔵 Affaires gelées :")

            if not current_list:
                print("Aucune affaire.")
            else:
                for i, aff in enumerate(current_list, start=1):
                    print(
                        f"{i}. {aff.titre} — Lieu: {aff.lieu}, Type: {aff.type_affaire}, "
                        f"Responsable: {aff.responsables}, "
                        f"Victimes: {aff.nombre_victimes()}, Suspects: {aff.nombre_suspects()}, "
                        f"Témoins: {aff.nombre_temoins()}, Urgence: {aff.urgence}"
                    )

        elif choix == "4":
            affaires = service.get_all()
            classees = service.affaires_classees(affaires)
            current_list = classees
            print("\n🟣 Affaires classées :")
            if not classees:
                print("Aucune affaire classée.")
            else:
                for i, aff in enumerate(classees, start=1):
                    print(
                        f"{i}. {aff.titre} — Lieu: {aff.lieu}, Type: {aff.type_affaire}, "
                        f"Responsable: {aff.responsables}, "
                        f"Victimes: {aff.nombre_victimes()}, Suspects: {aff.nombre_suspects()}, "
                        f"Témoins: {aff.nombre_temoins()}, Urgence: {aff.urgence}"
                    )

        # ----------------------------
        # CREATION
        # ----------------------------
        elif choix == "5":
            print("\n*** Création d'une nouvelle affaire ***")

            titre = ""
            while not titre:
                titre = input("Titre de l’affaire (obligatoire) : ").strip()
                if not titre:
                    print("Le titre est obligatoire.")

            date = input_date_cli("Date et heure du signalement (YYYY-MM-DD HH:MM)")
            lieu = input("Lieu de l’incident : ").strip()

            types_affaires = ["Homicide", "Agression", "Vol", "Fraude", "Divers"]
            type_aff = input(f"Type d’affaire ({', '.join(types_affaires)} ou autre) : ").strip()
            if not type_aff:
                type_aff = "Divers"

            description = input("Description de l’affaire : ").strip()
            responsables = input("Responsable(s) de l’affaire : ").strip()

            etat_choix = {"1": "🟢 En cours", "2": "🟡 À surveiller", "3": "🔵 Gelée — manque d'informations"}
            etat_input = input("État initial [1=En cours, 2=À surveiller, 3=Gelée] (défaut 1) : ").strip()
            etat = etat_choix.get(etat_input, "🟢 En cours")

            urgence_choix = {"1": "⚪ Faible", "2": "🟡 Moyen", "3": "🟠 Élevé", "4": "🔴 Critique"}
            urg_input = input("Niveau d'urgence [1=Faible, 2=Moyen, 3=Élevé, 4=Critique] (défaut 1) : ").strip()
            urgence = urgence_choix.get(urg_input, "⚪ Faible")

            # ✅ Personnes (menu boucle)
            personnes: list[Personne] = []
            gerer_personnes_cli(personnes)

            # Photos (on garde ton fonctionnement simple)
            photos: list[str] = []
            while True:
                add_photo = input("Ajouter une photo/pièce jointe ? (o/n) : ").strip().lower()
                if add_photo in ("o", "oui"):
                    photo_path = input(" - Chemin ou nom du fichier : ").strip()
                    if photo_path:
                        photos.append(photo_path)
                        print(f"✅ Photo ajoutée : {photo_path}")
                    else:
                        print("Chemin vide, aucune photo ajoutée.")
                else:
                    break

            # ✅ Armes (menu boucle)
            armes: list[Arme] = []
            gerer_armes_cli(armes)

            nouvelle_affaire = Affaire(
                titre=titre,
                date=date,
                lieu=lieu,
                type_affaire=type_aff,
                description=description,
                responsables=responsables,
                personnes=personnes,
                photos=photos,
                armes=armes,   # ✅ AJOUT IMPORTANT
                etat=etat,
                urgence=urgence
            )

            service.save(nouvelle_affaire)
            print(f"✅ Affaire '{titre}' créée avec succès.")

        # ----------------------------
        # OUVRIR / MODIFIER
        # ----------------------------
        elif choix == "6":
            if not current_list:
                current_list = service.get_all()

            if not current_list:
                print("Aucune affaire disponible.")
                continue

            num = input("Numéro de l’affaire à ouvrir : ").strip()
            if not num.isdigit():
                print("Veuillez entrer un numéro valide.")
                continue

            idx = int(num)
            if not (1 <= idx <= len(current_list)):
                print("Numéro invalide.")
                continue

            affaire = current_list[idx - 1]

            print(f"\n*** Détails de l’affaire '{affaire.titre}' ***")
            print(f"Titre : {affaire.titre}")
            print(f"Date : {affaire.date or '—'}")
            print(f"Lieu : {affaire.lieu or '—'}")
            print(f"Type d’affaire : {affaire.type_affaire or '—'}")
            print(f"Responsable(s) : {affaire.responsables or '—'}")
            print(f"État : {affaire.etat}")
            print(f"Urgence : {affaire.urgence}")
            print(f"Description : {affaire.description or 'Aucune description fournie.'}")

            afficher_personnes(affaire)
            afficher_armes(affaire)

            if affaire.photos:
                print("Pièces jointes :")
                for ph in affaire.photos:
                    print(f" - {ph}")
            else:
                print("Pièces jointes : Aucune photo enregistrée.")

            modif = input("\nModifier cette affaire ? (o/n) : ").strip().lower()
            if modif not in ("o", "oui"):
                continue

            print("** Mode édition – appuyez Entrée pour conserver la valeur actuelle **")

            new_titre = input(f"Titre [{affaire.titre}] : ").strip()
            if new_titre:
                affaire.titre = new_titre

            new_date = input_date_cli("Date et heure (YYYY-MM-DD HH:MM)", default=affaire.date, allow_empty=False)
            if new_date:
                affaire.date = new_date

            new_lieu = input(f"Lieu [{affaire.lieu}] : ").strip()
            if new_lieu:
                affaire.lieu = new_lieu

            new_type = input(f"Type d’affaire [{affaire.type_affaire}] : ").strip()
            if new_type:
                affaire.type_affaire = new_type

            new_desc = input("Description (laisser vide si inchangée) : ").strip()
            if new_desc:
                affaire.description = new_desc

            new_resps = input(f"Responsable(s) [{affaire.responsables}] : ").strip()
            if new_resps:
                affaire.responsables = new_resps

            etat_map = {
                "1": "🟢 En cours",
                "2": "🟡 À surveiller",
                "3": "🔵 Gelée — manque d'informations",
                "4": "🟣 Affaire classée"
            }
            new_etat = input(f"État actuel [{affaire.etat}] (1-4, vide pour garder) : ").strip()
            if new_etat in etat_map:
                affaire.etat = etat_map[new_etat]

            urg_map = {"1": "⚪ Faible", "2": "🟡 Moyen", "3": "🟠 Élevé", "4": "🔴 Critique"}
            new_urg = input(f"Urgence actuelle [{affaire.urgence}] (1-4, vide pour garder) : ").strip()
            if new_urg in urg_map:
                affaire.urgence = urg_map[new_urg]

            # ✅ Gestion personnes (boucle)
            edit_p = input("Gérer les personnes maintenant ? (o/n) : ").strip().lower()
            if edit_p in ("o", "oui"):
                gerer_personnes_cli(affaire.personnes)

            # Photos (simple)
            if affaire.photos:
                print("Photos actuelles :")
                for i_ph, ph in enumerate(affaire.photos, start=1):
                    print(f"  {i_ph}. {ph}")
            photo_choix = input("Modifier pièces jointes ? (A=ajouter, R=retirer, autre pour ignorer) : ").strip().lower()
            if photo_choix == "a":
                ph_path = input(" - Chemin de la nouvelle photo : ").strip()
                if ph_path:
                    affaire.photos.append(ph_path)
                    print("✅ Photo ajoutée.")
            elif photo_choix == "r":
                rem_ph = input("Numéro de la photo à retirer : ").strip()
                if rem_ph.isdigit():
                    rem_ph = int(rem_ph)
                    if 1 <= rem_ph <= len(affaire.photos):
                        suppr = affaire.photos.pop(rem_ph - 1)
                        print(f"🗑 Photo supprimée : {suppr}")

            # ✅ Gestion armes (boucle)
            edit_a = input("Gérer les armes maintenant ? (o/n) : ").strip().lower()
            if edit_a in ("o", "oui"):
                gerer_armes_cli(affaire.armes)

            if not affaire.titre:
                print("❌ Titre vide après modification - opération annulée.")
            else:
                service.save(affaire)
                print("✅ Affaire mise à jour avec succès.")

        # ----------------------------
        # SUPPRIMER
        # ----------------------------
        elif choix == "7":
            if not current_list:
                current_list = service.get_all()

            if not current_list:
                print("Aucune affaire à supprimer.")
                continue

            num = input("Numéro de l’affaire à supprimer : ").strip()
            if not num.isdigit():
                print("Veuillez entrer un numéro valide.")
                continue

            index = int(num)
            if not (1 <= index <= len(current_list)):
                print("Numéro invalide.")
                continue

            affaire = current_list[index - 1]
            confirm = input(f"Confirmez-vous la suppression de '{affaire.titre}' ? (o/n) : ").strip().lower()
            if confirm in ("o", "oui"):
                service.delete(affaire)
                print("✅ Affaire supprimée.")
                try:
                    current_list.remove(affaire)
                except ValueError:
                    current_list = []
            else:
                print("Suppression annulée.")

        # ----------------------------
        # QUITTER
        # ----------------------------
        elif choix == "8":
            print("Au revoir !")
            break

        else:
            print("Choix non reconnu, veuillez entrer un numéro de 1 à 8.")


if __name__ == "__main__":
    main()
