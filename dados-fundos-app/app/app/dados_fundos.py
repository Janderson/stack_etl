import pandas as pd
import os, sys
from app.db import collection_fi_data, collection_info_diario, collection_cadastro
import requests

PATHDATA = "/app/data"
URL_INFO_DIARIO = "http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/{filename}"
URL_CADASTRO = "http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"

def download_csv(url, path):
    if os.path.isfile(path):
        return {"ok": False, "error": f"file {path} exist"}
    req = requests.get(url)
    print(f"downloading url: {url}")
    open(path, "wb").write(req.content)
    return {"ok": True}

def load_file_info_diario(year, month):
    filename = f"{PATHDATA}/inf_diario_fi_{year}{month}.csv"
    print(f"filename: {filename}")
    df = pd.read_csv(filename, sep=";")
    collection = collection_info_diario()
    try:
        collection.insert_many(df.to_dict("records"))
    except Exception as e:
        print(f"some error ocorrer: {e}")
    print(df.tail())

def download_diario_file(year, month):
    filename = f"inf_diario_fi_{year}{month}.csv"
    url = URL_INFO_DIARIO.format(filename=filename)
    path = f"{PATHDATA}/{filename}"
    print(download_csv(url, path))

def download_cadastro():
    filepath = f"{PATHDATA}/cadastro.csv"
    print(download_csv(URL_CADASTRO, filepath))
    collection_cadastro().drop()
    df = pd.read_csv(filepath, sep=";", encoding="latin")
    collection_cadastro().insert_many(df.to_dict("records"))

def clean_field(field):
    if str(field) == "NaN":
        return None
    return field

def convert_files_to_structure_db():
    pass
    #collection_cadastro().find({"CN"})
    docs = collection_info_diario().count()
    size = 1000
    cnpjs = collection_info_diario().distinct('CNPJ_FUNDO')
    
    for cnpj in cnpjs:
        results = list(collection_info_diario().find({"CNPJ_FUNDO": cnpj}))
        cadastro = get_cadastro(cnpj)
        fields_cadastro = ["TP_FUNDO", "CNPJ_FUNDO", "DENOM_SOCIAL", "ADMIN"]
        new_record = {}
        for field in fields_cadastro:
            if clean_field(cadastro[field]):
                new_record[field] = clean_field(cadastro[field])
        
        quotes = [build_quotes(record) for record in results]
        new_record["quotes"] = quotes
        try:
            collection_fi_data("all").update_one({"CNPJ_FUNDO": cnpj}, 
                                                 {'$set': new_record}, upsert=True)
            print(f"cnpj inserted: {cnpj}")
        except Exception as e:
            print(f"exp: {e}")

            

cadastros = {}
def get_cadastro(cnpj):
    it = list(collection_cadastro().find({'CNPJ_FUNDO': cnpj}))
    #if it:
    #    cadastros[cnpj] = it[0]
    return it[0]

def build_structure(cnpj, items):
    pass

from datetime import datetime
def ym_from_record(record):
    record["date"] = datetime.fromisoformat(record["DT_COMPTC"])
    return record["date"].strftime("%Y%m")

def build_quotes(record:dict):
    record.pop("_id")
    record.pop("CNPJ_FUNDO")
    record["date"] = datetime.fromisoformat(record.pop("DT_COMPTC"))
    return record

