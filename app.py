import requests
import os
import csv
import pandas as pd
from dotenv import load_dotenv


def download_files(df):
    for idx, row in df.iterrows():
        diretorio = "./downloads/"
        os.makedirs(diretorio, exist_ok=True)
        response = requests.get(row["url"])
        new_filename = f'{row["url"].rsplit("/",maxsplit = 1)[1]}'
        filepath = f"{diretorio}/{new_filename}"

        with open(filepath, "wb") as file:
            file.write(response.content)


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave de API e a URL base da API da Pexels das variáveis de ambiente
API_ACCESS_KEY = os.getenv("PEXELS_API_KEY")
BASE_URL = os.getenv("PEXELS_API_BASE_URL")

# Parâmetros da busca de fotos
params = {
    "query": "camelia",  # Opção de busca
    "perpage": "80",  # Número máximo de fotos por página
    "size": "large",  # Outras opções: medium, small
}

# Faça a chamada à API da Pexels usando a biblioteca 'requests'
response = requests.get(
    BASE_URL,
    params=params,
    headers={
        "Authorization": f"{API_ACCESS_KEY}",
    },
)

# Verifique se a resposta foi bem-sucedida
if response.status_code == 200:
    data = response.json()
    photo_dict = {
        "id": [],
        "url": [],
        "alt": [],
    }
    # Exemplo de extração de informação de fotos:
    for photo in data["photos"]:
        photo_dict["id"].append(photo["id"])
        # TODO: verificar a qualidade da foto permitida
        photo_dict["url"].append(photo["src"]["original"])
        photo_dict["alt"].append(photo["alt"])
    df_photo_dict = pd.DataFrame(photo_dict)
    download_files(df_photo_dict)
    df_photo_dict.to_csv(
        os.path.join("./downloads", "photos.csv"),
        sep=";",
        index=False,
        quoting=csv.QUOTE_ALL,
        encoding="utf-8",
        lineterminator="\n",
    )
else:
    print(f"Erro na chamada da API: {response.status_code} - {response.text}")
