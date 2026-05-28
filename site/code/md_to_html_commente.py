import markdown


def convert_html(fichier_md: str, fichier_html: str):
    """Convertit un fichier Markdown en fichier HTML."""
    with open(fichier_md, "r") as f:
        text = f.read()

        # Partie compliquee :
        # il fallait comprendre que le Markdown n'est qu'un fichier texte,
        # puis utiliser une bibliotheque pour le transformer en HTML.
        html = markdown.markdown(text)

    with open(fichier_html, "w") as f:
        f.write(html)
