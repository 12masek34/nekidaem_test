from fastapi_pagination import add_pagination
import uvicorn

from endpoint import app
from models.database import create_db
from models.load_data import load_data_db

if __name__ == "__main__":
    create_db()
    load_data_db()
    add_pagination(app)
    uvicorn.run(app, host="0.0.0.0", port=8000)
