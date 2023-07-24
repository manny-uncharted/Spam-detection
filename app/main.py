import pathlib
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from cassandra.query import SimpleStatement
from cassandra.cqlengine.management import sync_table

# Internal classes
from . import (
    config,
    db,
    model,
    ml, 
    schema
    )

app = FastAPI()
settings = config.get_settings()


BASE_DIR = pathlib.Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR.parent / "models"
SMS_SPAM_MODEL_DIR = MODEL_DIR / "spam-sms"
MODEL_PATH = SMS_SPAM_MODEL_DIR / "spam-model.h5"
TOKENIZER_PATH = SMS_SPAM_MODEL_DIR / "spam-classifer-tokenizer.json"
METADATA_PATH = SMS_SPAM_MODEL_DIR / "spam-classifer-metadata.json"


"""Global variables to hold model instances"""
AI_MODEL = None
DB_SESSION = None
SMSInference = model.SMSInference

@app.on_event("startup")
def on_startup():
    global AI_MODEL, DB_SESSION
    AI_MODEL = ml.AIModel(
        model_path = MODEL_PATH,
        tokenizer_path = TOKENIZER_PATH,
        metadata_path = METADATA_PATH,
    )
    DB_SESSION = db.get_session()
    sync_table(SMSInference)



@app.post("/")
def read_index(q:Optional[str]=None):
    return {"hello": "world"}

@app.post("/")
def create_inference(query:schema.Query):
    global AI_MODEL
    preds_dict = AI_MODEL.predict_text(query.q)
    top = preds_dict.get('top') # {label: , conf}
    data = {"query": query.q, **top} # Packing the data we intend to store in our NOSQL db
    obj = SMSInference.objects.create(**data) # Saving the data to our database
    return obj

@app.get("/inferences")
def list_inferences():
    q = SMSInference.objects.all()
    print(q)
    return list(q)

@app.get("/inferences/{my_uuid}") # /?my_uuid=1234-1234-1234-1234
def read_inferences(my_uuid):
    obj = SMSInference.objects.get(uuid=my_uuid)
    return obj

def fetch_rows(
        stmt:SimpleStatement, 
        fetch_size:int = 25, 
        session=None):
    stmt.fetch_size = fetch_size
    result_set = session.execute(stmt)
    has_pages = result_set.has_more_pages
    yield "uuid,label,confidence,query,version\n"
    if has_pages:
        while has_pages:
            for row in result_set.current_rows:
                yield f"{row['uuid']},{row['label']},{row['confidence']},{row['query']},{row['model_version']}\n"
            has_pages = result_set.has_more_pages
            result_set = session.execute(stmt, paging_state=result_set.paging_state)
    # else:
    #     for row in result_set.current_rows:
    #         yield f"{row['uuid']},{row['label']},{row['confidence']},{row['query']},{row['model_version']}\n"
    #         print(f"Fetched row no pages: {row}")


@app.get("/dataset") # /?q=this is awesome
def export_inferences():
    global DB_SESSION
    cql_query = "SELECT * FROM spam_inferences.smsinference LIMIT 10000"
    statement = SimpleStatement(cql_query)
    # rows = DB_SESSION.execute(cql_query)
    return StreamingResponse(fetch_rows(statement, 10, DB_SESSION), media_type="text/csv")