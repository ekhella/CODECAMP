import argparse

def add(nom_fichier, description, etiquette):
    """
    Ajoute au fichier nom_fichier la description de la tâche, retourne son identifiant ;
    """
    id = get_id(nom_fichier)
    with open(nom_fichier, 'a') as f:
        f.write(f"{id},{description}, {etiquette}\n")
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

def rm(nom_fichier, id):
    tasks = read(nom_fichier)
    tasks = [task for task in tasks if task[0]!= id]
    tasks = [(int(task[0])-1 if task [0]> id else task[0], task[1], task[2]) for task in tasks]
    with open(nom_fichier, 'w') as f:
        for task in tasks:
            f.write(f"{task[0]},{task[1]},{task[2]} \n")
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
parser_add.add_argument('etiquette', help="Étiquette")

parser_rm = subparsers.add_parser('rm', help="Retirer une tâche")
parser_rm.add_argument('nom_fichier', help="Nom du fichier")
parser_rm.add_argument('id', help="Id à retirer")

parser_modify = subparsers.add_parser('modify', help="Modifier la tâche")
parser_modify.add_argument('nom_fichier', help="Nom du fichier")
parser_modify.add_argument('id', help="Id")
parser_modify.add_argument('nouvelle_desc', help="Description à modifier")
parser_modify.add_argument('nouvelle_etiquette', help="Étiquette à modifier")

parser_show = subparsers.add_parser('show', help="Montrer les tâches")
parser_show.add_argument('nom_fichier', help="Nom du fichier")

args= parser.parse_args()
if args.command == 'add':
     add(args.nom_fichier, args.description, args.etiquette)
     # python3 task.py add lestaches.txt "Faire la vaisselle" "Maison"
elif args.command == 'modify':
     modify(args.nom_fichier, args.id, args.nouvelle_desc, args.nouvelle_etiquette)
     #python3 task.py modify lestaches.txt 3 "Faire le ménage" "Pro"
elif args.command == 'rm':
     rm(args.nom_fichier, args.id)
     #python3 task.py rm lestaches.txt 3
elif args.command == 'show':
    show(args.nom_fichier)
    #python3 task.py show lestaches.txt