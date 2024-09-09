import argparse

def add(nom_fichier, description):
    """
    Ajoute au fichier nom_fichier la description de la tâche, retourne son identifiant ;
    """
    id = get_id(nom_fichier)
    with open(nom_fichier, 'a') as f:
        f.write(f"{id} {description}\n")
    return id

def modify(nom_fichier, id, nouvelle_description):
    tasks= read(nom_fichier)
    return None

def rm():
    return None

def show():
    return None

def get_id(nom_fichier) :
    tasks = read(nom_fichier)
    if tasks: # Sous-entendu if task is not None; sinon l'id qu'on va donner c'est 1
        return str(max(int(task[0]) for task in tasks) + 1)
    return "1"

def read(nom_fichier) : 
    liste=[]
    with open(nom_fichier, "r") as f:
            lines = f.readlines()
            for line in lines :
                 liste.append(line.strip().split(","))


parser = argparse.ArgumentParser(description="Gestionnaire de tâches")
subparsers = parser.add_subparsers(dest='command')
parser_add = subparsers.add_parser('add', help="Ajouter une tâche")
