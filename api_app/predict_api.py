from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

from train_CB_api import train_model_CB_and_get_confusion_matrix

app = FastAPI()

# Ca să poți apela API-ul dintr-o pagină HTML (alt origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # sau pune domeniul tău aici
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/train")
def run_training():
    """
    Rulează antrenarea modelului și întoarce matricea de confuzie ca JSON.
    """
    cm = train_model_CB_and_get_confusion_matrix()  # cm = numpy array (3x3)
    # transformăm în listă de liste ca să fie JSON-serializabil
    return {
        "confusion_matrix": cm.tolist()
    }
    