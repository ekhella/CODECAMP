import argparse
from datetime import datetime

def log_action(action, nom_fichier, details):
    """
    Enregistre l'action dans le fichier journal avec l'heure, l'action exécutée, et les détails du résultat.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('journal.txt', 'a') as f:
        f.write(f"[{timestamp}] Action: {action} | Fichier: {nom_fichier} | Détails: {details}\n")

def add_etiq(nom_fichier, id, nouvelles_etiquettes):
    """
    Ajoute une ou plusieurs étiquettes à une tâche existante.
    """
    tasks = read(nom_fichier)
    found = False
    with open(nom_fichier, 'w') as f:
        for task in tasks:
            if task[0] == id:
                    # Ajout des nouvelles étiquettes à la liste actuelle, en évitant les doublons
                etiquettes_actuelles = task[2].split("/")
                etiquettes_a_ajouter = [e.strip() for e in nouvelles_etiquettes.split("/") if e.strip()]
                etiquettes_finales = list(set(etiquettes_actuelles + etiquettes_a_ajouter))
                f.write(f"{id},{task[1]},{'/'.join(etiquettes_finales)}\n")
                found = True
                
            else:
                f.write(f"{task[0]},{task[1]},{task[2]}\n")
    if not found:
        print(f"Erreur : tâche {id} non trouvée.")
    log_action('add', nom_fichier, f"Etiquette ajoutée: {id}, {task[1]}, {etiquettes_finales}")


def rm_etiq(nom_fichier, id, etiquettes_a_supprimer):
    """
    Supprime une ou plusieurs étiquettes d'une tâche existante.
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
        print(f"Erreur : tâche {id} non trouvée.")
    log_action('add', nom_fichier, f"Etiquette supprimée: {id}, {task[1]}, {etiquettes_a_supprimer}")


def modif_etiq(nom_fichier, id, ancienne_etiquette, nouvelle_etiquette):
    """
    Remplace une étiquette spécifique par une nouvelle étiquette.
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
        print(f"Erreur : tâche {id} non trouvée.")
    log_action('add', nom_fichier, f"Etiquette modifiée: {id}, {task[1]}, {etiquettes_finales}")


def add(nom_fichier, description, etiquette):
    """
    Ajoute au fichier nom_fichier la description de la tâche et l'étiquette. 
    Si la description ou l'étiquette est vide, elles sont remplacées par "-".
    """
    
    # Récupérer un nouvel id
    id = get_id(nom_fichier)

    # Ajouter la nouvelle tâche au fichier
    with open(nom_fichier, 'a') as f:
        f.write(f"{id},{description},{etiquette}\n")

    log_action('add', nom_fichier, f"Tâche ajoutée: {id}, {description}, {etiquette}")
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
        print(f"Erreur : tâche {id} non trouvée.")
    log_action('add', nom_fichier, f"Tâche modifiée: {id}, {task[1]}, {nouvelle_etiquette}")

def rm(nom_fichier, id):
    tasks = read(nom_fichier)
    tasks = [task for task in tasks if task[0]!= id]
    tasks = [(int(task[0])-1 if task [0]> id else task[0], task[1], task[2]) for task in tasks]
    with open(nom_fichier, 'w') as f:
        for task in tasks:
            f.write(f"{task[0]},{task[1]},{task[2]} \n")
    log_action('add', nom_fichier, f"Tâche supprimée: {id}, {task[1]}, {task[2]}")
    return tasks

def show(nom_fichier):
    tasks = read(nom_fichier)

    # Calculer la longueur maximale pour chaque colonne
    max_id_length = max(len(task[0]) for task in tasks)  # Longueur max de l'id
    max_desc_length = max(len(task[1]) for task in tasks)  # Longueur max de la description
    max_etiquette_length = max(len(task[2]) for task in tasks)  # Longueur max de l'étiquette

    # Ajouter des longueurs minimales pour l'esthétique
    max_id_length = max(max_id_length, 2)
    max_desc_length = max(max_desc_length, 11)
    max_etiquette_length = max(max_etiquette_length, 9)

    # Imprimer l'en-tête avec les longueurs calculées
    print(f"+{'-' * (max_id_length + 2)}+{'-' * (max_desc_length + 2)}+{'-' * (max_etiquette_length + 2)}+")
    print(f"| {'id':<{max_id_length}} | {'description':<{max_desc_length}} | {'etiquette':<{max_etiquette_length}} |")
    print(f"+{'-' * (max_id_length + 2)}+{'-' * (max_desc_length + 2)}+{'-' * (max_etiquette_length + 2)}+")

    # Imprimer les lignes pour chaque tâche
    for task in tasks:
        print(f"| {task[0]:<{max_id_length}} | {task[1]:<{max_desc_length}} | {task[2]:<{max_etiquette_length}} |")

    # Imprimer la ligne de fin de tableau
    print(f"+{'-' * (max_id_length + 2)}+{'-' * (max_desc_length + 2)}+{'-' * (max_etiquette_length + 2)}+")
    log_action('add', nom_fichier, f"Show tableau")




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


parser = argparse.ArgumentParser(description="Gestionnaire de tâches")
subparsers = parser.add_subparsers(dest='command')

parser_add = subparsers.add_parser('add', help="Ajouter une tâche")
parser_add.add_argument('nom_fichier', help="Nom du fichier")
parser_add.add_argument('description', help="Description")
parser_add.add_argument('etiquette', nargs='?', default='', help="Étiquette (optionnelle)")

parser_add_etiq = subparsers.add_parser('add_etiq', help="Ajouter une ou plusieurs étiquettes")
parser_add_etiq.add_argument('nom_fichier', help="Nom du fichier")
parser_add_etiq.add_argument('id', help="Id de la tâche")
parser_add_etiq.add_argument('nouvelles_etiquettes', help="Étiquettes à ajouter (séparées par des slashs)")

parser_rm = subparsers.add_parser('rm', help="Retirer une tâche")
parser_rm.add_argument('nom_fichier', help="Nom du fichier")
parser_rm.add_argument('id', help="Id à retirer")

parser_rm_etiq = subparsers.add_parser('rm_etiq', help="Retirer une ou plusieurs étiquettes")
parser_rm_etiq.add_argument('nom_fichier', help="Nom du fichier")
parser_rm_etiq.add_argument('id', help="Id de la tâche")
parser_rm_etiq.add_argument('etiquettes_a_supprimer', help="Étiquettes à supprimer (séparées par des slashs)")

parser_modify = subparsers.add_parser('modify', help="Modifier la tâche")
parser_modify.add_argument('nom_fichier', help="Nom du fichier")
parser_modify.add_argument('id', help="Id")
parser_modify.add_argument('nouvelle_desc', help="Description à modifier")
parser_modify.add_argument('nouvelle_etiquette', nargs= '?', help="Étiquette à modifier")

parser_modif_etiq = subparsers.add_parser('modif_etiq', help="Modifier une étiquette spécifique")
parser_modif_etiq.add_argument('nom_fichier', help="Nom du fichier")
parser_modif_etiq.add_argument('id', help="Id de la tâche")
parser_modif_etiq.add_argument('ancienne_etiquette', help="Étiquette à modifier")
parser_modif_etiq.add_argument('nouvelle_etiquette', help="Nouvelle étiquette")

parser_show = subparsers.add_parser('show', help="Montrer les tâches")
parser_show.add_argument('nom_fichier', help="Nom du fichier")

args = parser.parse_args()
if args.command == 'add':
    add(args.nom_fichier, args.description, args.etiquette)
    # python3 task.py add lestaches.txt "Faire la vaisselle" "Maison"
elif args.command == 'modify':
    modify(args.nom_fichier, args.id, args.nouvelle_desc, args.nouvelle_etiquette)
    # python3 task.py modify lestaches.txt 3 "Faire le ménage" "Pro"
elif args.command == 'rm':
    rm(args.nom_fichier, args.id)
    # python3 task.py rm lestaches.txt 3
elif args.command == 'show':
    show(args.nom_fichier)
    # python3 task.py show lestaches.txt
elif args.command == 'add_etiq':
    add_etiq(args.nom_fichier, args.id, args.nouvelles_etiquettes)
    # python3 task.py add_etiq lestaches.txt 3 "Travail,Maison"
elif args.command == 'rm_etiq':
    rm_etiq(args.nom_fichier, args.id, args.etiquettes_a_supprimer)
    # python3 task.py rm_etiq lestaches.txt 3 "Travail"
elif args.command == 'modif_etiq':
    modif_etiq(args.nom_fichier, args.id, args.ancienne_etiquette, args.nouvelle_etiquette)
    # python3 task.py modif_etiq lestaches.txt 3 "Maison" "Pro"
else:
    parser.print_help()






