import json

with open("inputs.json") as f:
    config = json.load(f)

ACTIVE_DB = config["active_db"]
JWT_SECRET_KEY = config["jwt_secret_key"]
JWT_ALGORITHM = config["jwt_algorithm"]
TOKEN_EXPIRY_HOURS = config["token_expiry_hours"]

def build_connection_string(db_config, db_type):
    if db_type == "mysql":
        return f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    elif db_type == "postgresql":
        return f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    elif db_type == "sqlserver":
        return f"mssql+pyodbc://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?driver=ODBC+Driver+17+for+SQL+Server"
    else:
        raise ValueError("Unsupported database type")

if ACTIVE_DB == "mongodb":
    DB_CONFIG = config["mongodb"]
elif ACTIVE_DB in ["mysql", "postgresql", "sqlserver"]:
    DB_CONFIG = config[ACTIVE_DB]
    DB_CONFIG["connection_string"] = build_connection_string(DB_CONFIG, ACTIVE_DB)
else:
    raise ValueError("Unsupported database type")
