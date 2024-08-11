from main import app
from fastapi import File, UploadFile
import pandas as pd
import shutil


@app.post("/get_route_plan")
async def get_route_plan(file: UploadFile = File(...)):
    with open(f"{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

        # Create a dataframe
        df = pd.read_excel(f"{file.filename}")
