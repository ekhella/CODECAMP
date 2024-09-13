import argparse
from datetime import datetime

def log_action(action, nom_fichier, details, resultat=None):
    """
    Enregistre l'action dans le fichier journal avec l'heure, l'action executee, et les details du resultat.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    resultat_str = f" | Resultat: {resultat}" if resultat else ""
    with open('journal.txt', 'a') as f:
        f.write(f"[{timestamp}] Action: {action} | Fichier: {nom_fichier} | Details: {details}{resultat_str}\n")



def add_etiq(nom_fichier, id, nouvelles_etiquettes):
    """
    Ajoute une ou plusieurs etiquettes à une tache existante.
    """
    tasks = read(nom_fichier)
    found = False
    with open(nom_fichier, 'w') as f:
        for task in tasks:
            if task[0] == id:
                    # Ajout des nouvelles etiquettes à la liste actuelle, en evitant les doublons
                etiquettes_actuelles = task[2].split("/")
                etiquettes_a_ajouter = [e.strip() for e in nouvelles_etiquettes.split("/") if e.strip()]
                etiquettes_finales = list(set(etiquettes_actuelles + etiquettes_a_ajouter))
                f.write(f"{id},{task[1]},{'/'.join(etiquettes_finales)}\n")
                found = True
                
            else:
                f.write(f"{task[0]},{task[1]},{task[2]}\n")
    if not found:
        print(f"Erreur : tache {id} non trouvee.")
    log_action('ajout etiquette', nom_fichier, f"etiquettes ajoutees: {id}, {etiquettes_finales}")




def rm_etiq(nom_fichier, id, etiquettes_a_supprimer):
    """
    Supprime une ou plusieurs etiquettes d'une tache existante.
    """
    tasks = read(nom_fichier)
    found = False
    with open(nom_fichier, 'w') as f:
        for task in tasks:
            if task[0] == id:
                etiquettes_actuelles = task[2].split("/")
                etiquettes_finales = [e for e in etiquettes_actuelles if e not in etiquettes_a_supprimer.split("/")]
                f.write(f"{id},{task[1]},{'/'.join(etiquettes_finales)}\n")
                found = True
            else:
                f.write(f"{task[0]},{task[1]},{task[2]}\n")
    if not found:
        print(f"Erreur : tache {id} non trouvee.")
    log_action('suppression etiquette', nom_fichier, f"etiquettes supprimees: {id}, {etiquettes_a_supprimer}")



def modif_etiq(nom_fichier, id, ancienne_etiquette, nouvelle_etiquette):
    """
    Remplace une etiquette specifique par une nouvelle etiquette.
    """
    tasks = read(nom_fichier)
    found = False
    with open(nom_fichier, 'w') as f:
        for task in tasks:
            if task[0] == id:
                etiquettes_actuelles = task[2].split("/")
                etiquettes_finales = [nouvelle_etiquette if e == ancienne_etiquette else e for e in etiquettes_actuelles]
                f.write(f"{id},{task[1]},{'/'.join(etiquettes_finales)}\n")
                found = True
            else:
                f.write(f"{task[0]},{task[1]},{task[2]}\n")
    if not found:
        print(f"Erreur : tache {id} non trouvee.")
    log_action('modification etiquette', nom_fichier, f"etiquette modifiee: {id}, ancienne: {ancienne_etiquette}, nouvelle: {nouvelle_etiquette}")



def add(nom_fichier, description, etiquette, dependencies=None, state='a faire'):
    """
    Ajoute une nouvelle tache avec ses dependances (optionnelles) et son etat initial.
    """
    id = get_id(nom_fichier)
    dependencies = dependencies or 'none'
    
    with open(nom_fichier, 'a') as f:
        f.write(f"{id},{description},{etiquette},{dependencies},{state}\n")

    log_action('add', nom_fichier, f"Tache ajoutee: {id}, {description}, {etiquette}, Dependances: {dependencies}, etat: {state}")
    return id

    


def modify(nom_fichier, id, nouvelle_description, nouvelle_etiquette):
    tasks= read(nom_fichier)
    found = False
    with open(nom_fichier, 'w') as f:
        for task in tasks:
            if task[0] == id:
                f.write(f"{id},{nouvelle_description},{nouvelle_etiquette}\n")
                found = True
            else:
                f.write(f"{task[0]},{task[1]},{task[2]} \n")
    if not found:
        print(f"Erreur : tache {id} non trouvee.")
    log_action('modification', nom_fichier, f"Tache modifiee: {id}, {nouvelle_description}, {nouvelle_etiquette}")


def update_task_state(nom_fichier, id, new_state):
    """
    Met à jour l'etat d'une tache après verification des dependances.
    """
    tasks = read(nom_fichier)
    found = False
    with open(nom_fichier, 'w') as f:
        for task in tasks:
            if task[0] == id:
                if new_state == 'in progress' and not are_dependencies_completed(tasks, task):
                    print(f"Erreur : Les dependances de la tache {id} ne sont pas encore terminees.")
                    f.write(f"{task[0]},{task[1]},{task[2]},{task[3]},{task[4]}\n")  # ecrire sans modification
                    continue

                if new_state == 'completed' and task[4] != 'in progress':
                    print(f"Erreur : La tache {id} doit être 'en cours' avant de pouvoir être 'terminee'.")
                    f.write(f"{task[0]},{task[1]},{task[2]},{task[3]},{task[4]}\n")  # ecrire sans modification
                    continue

                f.write(f"{id},{task[1]},{task[2]},{task[3]},{new_state}\n")
                found = True
            else:
                f.write(f"{task[0]},{task[1]},{task[2]},{task[3]},{task[4]}\n")
    if not found:
        print(f"Erreur : tache {id} non trouvee.")
    log_action('update', nom_fichier, f"etat de la tache mis à jour: {id}, {new_state}")

def are_dependencies_completed(tasks, task):
    """
    Verifie si les taches dont depend la tache courante sont terminees.
    """
    dependencies = task[3].split('/') if task[3] != 'none' else []
    for dep_id in dependencies:
        dep_task = next((t for t in tasks if t[0] == dep_id), None)
        if dep_task and dep_task[4] != 'completed':
            return False
    return True


def modif_etat(nom_fichier, id, nouvel_etat):
    """
    Met à jour le statut d'une tâche spécifiée, en vérifiant si les dépendances sont terminées
    avant de la passer à "en cours" ou tout autre statut.
    """
    try:
        # Lire toutes les lignes du fichier
        with open(nom_fichier, 'r') as file:
            lignes = file.readlines()

        # Trouver la tâche actuelle et ses dépendances
        tache_trouvee = False
        dependances = []
        statut_dependances_valide = True
        
        for ligne in lignes:
            colonnes = ligne.strip().split(',')
            if colonnes[0] == str(id):  # Identification de la tâche
                tache_trouvee = True
                dependances = colonnes[3].split('/') if colonnes[3] != 'none' else []
                
                # Vérification des dépendances seulement si on veut passer la tâche à "en cours"
                if nouvel_etat == "in progress":
                    for dep_id in dependances:
                        for ligne_dep in lignes:
                            colonnes_dep = ligne_dep.strip().split(',')
                            if colonnes_dep[0] == dep_id and colonnes_dep[4] != "completed":
                                statut_dependances_valide = False
                                print(f"Tâche {id} ne peut pas être mise à jour car la dépendance {dep_id} n'est pas terminée.")
                                break

                    # Si une dépendance n'est pas terminée, on sort de la boucle
                    if not statut_dependances_valide:
                        raise Exception(f"Toutes les dépendances de la tâche {id} doivent être complétées avant de passer la tâche à 'in progress'.")

        if not tache_trouvee:
            raise Exception(f"Tâche {id} introuvable dans {nom_fichier}.")

        # Si toutes les dépendances sont terminées, on met à jour l'état de la tâche
        with open(nom_fichier, 'w') as file:
            for ligne in lignes:
                colonnes = ligne.strip().split(',')
                if colonnes[0] == str(id):
                    colonnes[4] = nouvel_etat  # Mise à jour du statut
                    ligne = ','.join(colonnes) + '\n'
                file.write(ligne)

        print(f"Tâche {id} mise à jour avec le statut : {nouvel_etat}")

    except Exception as e:
        print(f"Erreur : {e}")


def add_dependency(nom_fichier, id, dependencies):
    """
    Ajoute une ou plusieurs dependances à une tache specifiee.
    """
    with open(nom_fichier, 'r') as file:
        lignes = file.readlines()
    
    with open(nom_fichier, 'w') as file:
        for ligne in lignes:
            colonnes = ligne.strip().split(',')
            if colonnes[0] == str(id):
                if colonnes[3] == 'none':
                    colonnes[3] = dependencies
                else:
                    colonnes[3] += '/' + dependencies  # Ajout de nouvelles dependances
                ligne = ','.join(colonnes) + '\n'
            file.write(ligne)
    print(f"Dependance(s) {dependencies} ajoutee(s) à la tache {id}")

def remove_dependency(nom_fichier, id, dependencies):
    """
    Supprime une ou plusieurs dependances d'une tache specifiee.
    """
    with open(nom_fichier, 'r') as file:
        lignes = file.readlines()
    
    with open(nom_fichier, 'w') as file:
        for ligne in lignes:
            colonnes = ligne.strip().split(',')
            if colonnes[0] == str(id):
                if colonnes[3] != 'none':
                    dep_list = colonnes[3].split('/')
                    dep_to_remove = dependencies.split('/')
                    colonnes[3] = '/'.join([dep for dep in dep_list if dep not in dep_to_remove]) or 'none'
                ligne = ','.join(colonnes) + '\n'
            file.write(ligne)
    print(f"Dependance(s) {dependencies} supprimee(s) de la tache {id}")




def rm(nom_fichier, id):
    tasks = read(nom_fichier)
    tasks_to_update = []
    found = False
    
    # Check and update dependent tasks
    for task in tasks:
        dependencies = task[3].split('/') if task[3] != 'none' else []
        if id in dependencies:
            dependencies.remove(id)
            task[3] = '/'.join(dependencies) if dependencies else 'none'
            tasks_to_update.append(task)

    tasks = [task for task in tasks if task[0] != id]
    
    with open(nom_fichier, 'w') as f:
        for task in tasks:
            f.write(f"{task[0]},{task[1]},{task[2]},{task[3]},{task[4]}\n")
    
    log_action('rm', nom_fichier, f"Tache supprimee: {id}")
    
    return tasks


def show(nom_fichier):
    tasks = read(nom_fichier)

    # Calculer la longueur maximale pour chaque colonne
    max_id_length = max(len(task[0]) for task in tasks)  # Longueur max de l'id
    max_desc_length = max(len(task[1]) for task in tasks)  # Longueur max de la description
    max_etiquette_length = max(len(task[2]) for task in tasks)  # Longueur max de l'etiquette
    max_depend_length = max(len(task[3]) for task in tasks)  # Longueur max des dependances
    max_state_length = max(len(task[4]) for task in tasks)  # Longueur max de l'etat

    # Ajouter des longueurs minimales pour l'esthetique
    max_id_length = max(max_id_length, 2)
    max_desc_length = max(max_desc_length, 11)
    max_etiquette_length = max(max_etiquette_length, 9)
    max_depend_length = max(max_depend_length, 9)
    max_state_length = max(max_state_length, 5)

    # Imprimer l'en-tête avec les longueurs calculees
    print(f"+{'-' * (max_id_length + 2)}+{'-' * (max_desc_length + 2)}+{'-' * (max_etiquette_length + 2)}+{'-' * (max_depend_length + 2)}+{'-' * (max_state_length + 2)}+")
    print(f"| {'id':<{max_id_length}} | {'description':<{max_desc_length}} | {'etiquette':<{max_etiquette_length}} | {'depend de':<{max_depend_length}} | {'etat':<{max_state_length}} |")
    print(f"+{'-' * (max_id_length + 2)}+{'-' * (max_desc_length + 2)}+{'-' * (max_etiquette_length + 2)}+{'-' * (max_depend_length + 2)}+{'-' * (max_state_length + 2)}+")

    # Imprimer les lignes pour chaque tache
    for task in tasks:
        print(f"| {task[0]:<{max_id_length}} | {task[1]:<{max_desc_length}} | {task[2]:<{max_etiquette_length}} | {task[3]:<{max_depend_length}} | {task[4]:<{max_state_length}} |")

    # Imprimer la ligne de fin de tableau
    print(f"+{'-' * (max_id_length + 2)}+{'-' * (max_desc_length + 2)}+{'-' * (max_etiquette_length + 2)}+{'-' * (max_depend_length + 2)}+{'-' * (max_state_length + 2)}+")
    log_action('show', nom_fichier, "Affichage des taches avec dependances et etat")





def get_id(nom_fichier) :
    tasks = read(nom_fichier)
    if tasks: # Sous-entendu if task is not None; sinon l'id qu'on va donner c'est 1
        return str(max(int(task[0]) for task in tasks) + 1)
    return "1"

def read(nom_fichier) : 
    liste=[]
    try:
        with open(nom_fichier, "r") as f:
            lines = f.readlines()
            for line in lines :
                 liste.append(line.strip().split(","))
        return liste
    except :
        return []


parser = argparse.ArgumentParser(description="Gestionnaire de taches")
subparsers = parser.add_subparsers(dest='command')

# Ajouter une tache
parser_add = subparsers.add_parser('add', help="Ajouter une tache")
parser_add.add_argument('nom_fichier', help="Nom du fichier")
parser_add.add_argument('description', help="Description")
parser_add.add_argument('etiquette', nargs='?', default='', help="etiquette (optionnelle)")

# Ajouter une dependance
parser_add = subparsers.add_parser('add_dep', help="Ajouter une dependance")
parser_add.add_argument('nom_fichier', help="Nom du fichier")
parser_add.add_argument('id', help="Id de la tache")
parser_add.add_argument('dependance', nargs='?', default='none', help="depende de la tache numero (id) (optionnelle)")

#Retirer une dependance
parser_rm_dep = subparsers.add_parser('rm_dep', help="Retirer une ou plusieurs dependances")
parser_rm_dep.add_argument('nom_fichier', help="Nom du fichier")
parser_rm_dep.add_argument('id', help="Id de la tache")
parser_rm_dep.add_argument('etiquettes_a_supprimer', help="etiquettes à supprimer (separees par des slashs)")

# Modifier un état de tache
parser_modif_statut = subparsers.add_parser('modif_etat', help="Modifier un état de tâche")
parser_modif_statut.add_argument('nom_fichier', help="Nom du fichier")
parser_modif_statut.add_argument('id', help="Id de la tache")
parser_modif_statut.add_argument('nouvel_etat', help="Nouvel etat")

# Ajouter une ou plusieurs etiquettes
parser_add_etiq = subparsers.add_parser('add_etiq', help="Ajouter une ou plusieurs etiquettes")
parser_add_etiq.add_argument('nom_fichier', help="Nom du fichier")
parser_add_etiq.add_argument('id', help="Id de la tache")
parser_add_etiq.add_argument('nouvelles_etiquettes', help="etiquettes à ajouter (separees par des slashs)")

# Retirer une tache
parser_rm = subparsers.add_parser('rm', help="Retirer une tache")
parser_rm.add_argument('nom_fichier', help="Nom du fichier")
parser_rm.add_argument('id', help="Id à retirer")

# Retirer une ou plusieurs etiquettes
parser_rm_etiq = subparsers.add_parser('rm_etiq', help="Retirer une ou plusieurs etiquettes")
parser_rm_etiq.add_argument('nom_fichier', help="Nom du fichier")
parser_rm_etiq.add_argument('id', help="Id de la tache")
parser_rm_etiq.add_argument('etiquettes_a_supprimer', help="etiquettes à supprimer (separees par des slashs)")

# Modifier une tache
parser_modify = subparsers.add_parser('modify', help="Modifier la tache")
parser_modify.add_argument('nom_fichier', help="Nom du fichier")
parser_modify.add_argument('id', help="Id")
parser_modify.add_argument('nouvelle_desc', help="Description à modifier")
parser_modify.add_argument('nouvelle_etiquette', nargs='?', default='', help="etiquette à modifier")

# Modifier une etiquette specifique
parser_modif_etiq = subparsers.add_parser('modif_etiq', help="Modifier une etiquette specifique")
parser_modif_etiq.add_argument('nom_fichier', help="Nom du fichier")
parser_modif_etiq.add_argument('id', help="Id de la tache")
parser_modif_etiq.add_argument('ancienne_etiquette', help="etiquette à modifier")
parser_modif_etiq.add_argument('nouvelle_etiquette', help="Nouvelle etiquette")

# Montrer les taches
parser_show = subparsers.add_parser('show', help="Montrer les taches")
parser_show.add_argument('nom_fichier', help="Nom du fichier")

args = parser.parse_args()
if args.command == 'add':
    add(args.nom_fichier, args.description, args.etiquette)
    # Exemple à taper en ligne de commande :
    # python3 task.py add lestaches.txt "Reunir les chiffres du trimestre" "Finance/Reporting"
elif args.command == 'modify':
    modify(args.nom_fichier, args.id, args.nouvelle_desc, args.nouvelle_etiquette)
    # Exemple à taper en ligne de commande :
    # python3 task.py modify lestaches.txt 3 "Reviser la presentation pour la reunion" "Management/Communication"
elif args.command == 'rm':
    rm(args.nom_fichier, args.id)
    # Exemple à taper en ligne de commande :
    # python3 task.py rm lestaches.txt 5
elif args.command == 'show':
    show(args.nom_fichier)
    # Exemple à taper en ligne de commande :
    # python3 task.py show lestaches.txt
elif args.command == 'add_etiq':
    add_etiq(args.nom_fichier, args.id, args.nouvelles_etiquettes)
    # Exemple à taper en ligne de commande :
    # python3 task.py add_etiq lestaches.txt 6 "Agile/Sprint"
elif args.command == 'rm_etiq':
    rm_etiq(args.nom_fichier, args.id, args.etiquettes_a_supprimer)
    # Exemple à taper en ligne de commande :
    # python3 task.py rm_etiq lestaches.txt 4 "Business Intelligence"
elif args.command == 'modif_etiq':
    modif_etiq(args.nom_fichier, args.id, args.ancienne_etiquette, args.nouvelle_etiquette)
    # Exemple à taper en ligne de commande :
    # python3 task.py modif_etiq lestaches.txt 2 "Design" "WebDesign"
elif args.command == 'modif_etat':
    modif_etat(args.nom_fichier, args.id, args.nouvel_etat)
    # Exemple à taper en ligne de commande :
    # python3 task.py modif_statut lestaches.txt 3 "in progress"
elif args.command == 'add_dep':
    add_dependency(args.nom_fichier, args.id, args.dependencies)
    # Exemple à taper en ligne de commande :
    # python3 task.py add_dep lestaches.txt 3 "1/2"
elif args.command == 'rm_dep':
    remove_dependency(args.nom_fichier, args.id, args.dependencies)
    # Exemple à taper en ligne de commande :
    # python3 task.py rm_dep lestaches.txt 3 "1"
else:
    parser.print_help()






