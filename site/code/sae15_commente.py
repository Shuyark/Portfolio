import markdown
import requests
from md_to_html_commente import convert_html


def response(id: int):
    """Recupere toutes les informations d'un commerce avec son identifiant OSM."""
    url = "https://www.openstreetmap.org/api/0.6/node/" + str(id) + ".json"
    response = requests.get(url)
    json_data = response.json()
    return json_data


def get_node(id: int) -> dict:
    """Renvoie le nom du commerce si celui-ci existe, sinon SANS NOM."""
    url = "https://www.openstreetmap.org/api/0.6/node/" + str(id) + ".json"
    try:
        response = requests.get(url).json()

        # Partie compliquee :
        # la reponse JSON contient des listes et des dictionnaires imbriques.
        # Il fallait comprendre le chemin ["elements"][0]["tags"]["name"].
        return response["elements"][0]["tags"].get("name")
    except:
        return "SANS NOM"


def print_node_attributes(id: int) -> None:
    """Renvoie tous les attributs d'un noeud choisi."""
    url = "https://www.openstreetmap.org/api/0.6/node/" + str(id) + ".json"
    response = requests.get(url).json()
    try:
        return response["elements"][0]["tags"]
    except:
        return "Cette id n'existe pas"


def node_to_md(data: dict, file_name: str) -> None:
    """Cree un fichier Markdown a partir des informations d'un noeud."""
    contenu = "# Node " + str(data.get("id")) + "\n\n"
    for cle, valeur in data.items():
        contenu += "* " + str(cle) + ": " + str(valeur) + "\n"
    with open(file_name, "w") as f:
        f.write(contenu)


demande = """[out:json][timeout:180];

area["name"="Normandie"]["admin_level"="4"]->.zone_de_recherche;

# Partie compliquee :
# il fallait d'abord trouver un sujet exploitable.
# J'ai choisi les supermarches en Normandie car le tag shop=supermarket
# permettait de recuperer des donnees assez precises.
nwr["shop"="supermarket"](area.zone_de_recherche);

out geom;
"""


def get_dataset(query: str) -> dict:
    url = "https://overpass-api.de/api/interpreter?data=" + str(query)
    r = requests.get(url)

    # Partie compliquee :
    # OpenStreetMap / Overpass etait parfois surcharge de requetes.
    # Quand le serveur repondait mal, le programme pouvait bloquer ici.
    rep = r.json()
    return rep


def compute_statist(data):
    """Calcule la repartition des principales enseignes de supermarches."""
    carrefour = 0
    leclerc = 0
    intermarche = 0
    lidl = 0
    auchan = 0

    for element in data["elements"]:
        # Partie compliquee :
        # tous les elements OpenStreetMap n'ont pas les memes informations.
        # Il faut verifier que les champs existent avant de les utiliser.
        if "tags" not in element:
            continue
        if "name" not in element["tags"]:
            continue

        nom = element["tags"]["name"].lower()

        # Partie compliquee :
        # les noms des magasins ne sont pas toujours ecrits exactement pareil.
        # On cherche donc des mots dans le nom complet.
        if "carrefour" in nom:
            carrefour += 1
        elif "leclerc" in nom:
            leclerc += 1
        elif "intermarche" in nom or "intermarché" in nom:
            intermarche += 1
        elif "lidl" in nom:
            lidl += 1
        elif "auchan" in nom:
            auchan += 1

    total = carrefour + leclerc + intermarche + lidl + auchan

    # Partie compliquee :
    # transformer les comptages en pourcentages rend le resultat plus clair.
    stat_carrefour = (carrefour * 100) / total
    stat_leclerc = (leclerc * 100) / total
    stat_intermarche = (intermarche * 100) / total
    stat_lidl = (lidl * 100) / total
    stat_auchan = (auchan * 100) / total

    return stat_carrefour, stat_leclerc, stat_intermarche, stat_lidl, stat_auchan


def stats_supermarches(query, fichier_md: str, fichier_html: str):
    c, l, i, li, a = compute_statist(get_dataset(query))
    stats = {"Carrefour": c, "Leclerc": l, "Intermarche": i, "Lidl": li, "Auchan": a}
    contenu = "# Supermarches en Normandie\n"
    contenu += "* lien osm :\n"

    # Partie compliquee :
    # il fallait generer un rapport automatiquement,
    # sans recopier les resultats a la main.
    for nom, valeur in stats.items():
        contenu += "* " + str(nom) + ": " + str(valeur) + "\n"

    with open(fichier_md, "w") as f:
        f.write(contenu)

    convert_html(fichier_md, fichier_html)

    return (
        "Resultats :",
        stats,
        "Le supermarche le plus present en Normandie est :",
        max(stats, key=stats.get),
    )
