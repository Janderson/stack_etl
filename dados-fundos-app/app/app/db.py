from pymongo import MongoClient

DB_URI = "mongodb://mongodb:27017"
def get_db():
    client = MongoClient(DB_URI)
    return client["dados_fundos"]

def collection_info_diario(year_month=None):
    db = get_db()
    collection = db["fi_info_diario"]
    collection.create_index([("CNPJ_FUNDO", 1), ("DT_COMPTC", 1)], unique=True)
    return collection

def collection_fi_data(year_month):
    db = get_db()
    collection = db[f"fi_data_{year_month}"]
    collection.create_index([("CNPJ_FUNDO", 1)], unique=True)
    return collection


def collection_cadastro():
    db = get_db()
    return db["fi_cadastro"]