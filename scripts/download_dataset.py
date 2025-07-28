import requests
import os

def requisicao(owner, repo):
    """
    Consulta a API do GitHub para obter informações da última release
    de um repositório específico.

    Parâmetros:
    - owner (str): Nome do proprietário do repositório (usuário ou organização).
    - repo (str): Nome do repositório.

    Retorno:
    - dict: Dados da resposta em formato JSON contendo informações da última release.
    """
    url_release = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    res = requests.get(url_release)
    return res.json()

def localizar(owner, repo, nome_arquivo, destino) -> None:
    """
    Baixa um arquivo específico (asset) da última release de um repositório do GitHub
    e o salva localmente em um diretório destino.

    Parâmetros:
    - owner (str): Nome do proprietário do repositório (usuário ou organização).
    - repo (str): Nome do repositório.
    - nome_arquivo (str): Nome exato do asset que será baixado.
    - destino (str): Caminho local onde o arquivo será salvo.
    """
    release_data = requisicao(owner, repo)
    asset_url = None

    for asset in release_data["assets"]:
        if asset["name"] == nome_arquivo:
            asset_url = asset["browser_download_url"]
            break

    if asset_url:
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        response = requests.get(asset_url)
        with open(destino, "wb") as f:
            f.write(response.content)

def main():
    """
    Função principal que define o repositório, nome do arquivo e destino.
    Executa o processo de download do asset da release.
    A fim de buscar o ultimo dataset gerado pela nossa pipeline de Dados.
    """
    owner = "tamires123-hub"
    repo = "pipeline_dadosESI"
    nome_arquivo = "dataset_filmes_class.csv"
    destino = "dados/dataset_filmes_class.csv"
    localizar(owner, repo, nome_arquivo, destino)

if __name__ == "__main__":
    main()
