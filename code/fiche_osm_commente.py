import markdown
import requests


def print_node_attributes(id: int) -> None:
    """Renvoie tous les attributs d'un noeud OpenStreetMap."""
    url = "https://www.openstreetmap.org/api/0.6/node/" + str(id) + ".json"
    response = requests.get(url).json()
    try:
        # Partie compliquee :
        # les attributs utiles sont dans tags, lui-meme dans elements.
        return response["elements"][0]["tags"]
    except:
        return "Cette id n'existe pas"


def get_node(id: int) -> dict:
    """Renvoie le nom du commerce si celui-ci existe."""
    url = "https://www.openstreetmap.org/api/0.6/node/" + str(id) + ".json"
    try:
        response = requests.get(url).json()

        # Partie compliquee :
        # certains noeuds n'ont pas de nom, donc get evite une erreur directe.
        return response["elements"][0]["tags"].get("name")
    except:
        return "SANS NOM"


def fiche_osm(fichier_md: str, id: int, fichier_html) -> None:
    """Cree une fiche Markdown puis une version HTML pour un noeud OSM."""
    contenu = ""
    contenu += "# " + get_node(id) + " lien osm :\n"

    # Partie compliquee :
    # il fallait parcourir toutes les cles du dictionnaire renvoye par OSM
    # pour generer automatiquement la fiche.
    for i in print_node_attributes(id):
        contenu += "* " + i + ": " + print_node_attributes(id)[i] + "\n"

    with open(fichier_md, "w") as f:
        f.write(contenu)

    with open(fichier_md, "r") as f:
        text = f.read()
        html = markdown.markdown(text)

    with open(fichier_html, "w") as f:
        f.write(html)
