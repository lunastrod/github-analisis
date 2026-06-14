import os
import requests
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN") 

if not TOKEN:
    print("Error: No se encontró la variable GITHUB_TOKEN en el archivo .env")
    exit(1)

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def obtener_repositorios():
    url = "https://api.github.com/user/repos"
    params = {"per_page": 100, "type": "all"}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al consultar la API: {response.status_code}")
        return []

def analizar_perfil():
    repos = obtener_repositorios()
    if not repos:
        return

    forks = []
    privados = []
    publicos = []

    for repo in repos:
        if repo["fork"]:
            forks.append(repo)
        elif repo["private"]:
            privados.append(repo)
        else:
            publicos.append(repo)

    privados.sort(key=lambda r: r["size"], reverse=True)
    publicos.sort(key=lambda r: r["size"], reverse=True)

    print(f"=== REPOSITORIOS FORK ({len(forks)}) ===")
    for repo in forks:
        print(f"Fork: {repo['name']}")
        print(f"   URL: {repo['html_url']}")
        print(f"   Tamaño: {repo['size']} KB")
        print("-" * 50)

    print(f"\n=== REPOSITORIOS PRIVADOS ORDENADOS POR TAMAÑO ({len(privados)}) ===")
    for repo in privados:
        print(f"Privado: {repo['name']}")
        print(f"   URL: {repo['html_url']}")
        print(f"   Tamaño: {repo['size']} KB")
        print("-" * 50)

    print(f"\n=== REPOSITORIOS PÚBLICOS ORDENADOS POR TAMAÑO ({len(publicos)}) ===")
    for repo in publicos:
        print(f"Público: {repo['name']}")
        print(f"   URL: {repo['html_url']}")
        print(f"   Tamaño: {repo['size']} KB")
        print("-" * 50)

if __name__ == "__main__":
    analizar_perfil()