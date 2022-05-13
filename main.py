from fastapi_pagination import add_pagination
import uvicorn

from endpoint import app



if __name__ == "__main__":
    add_pagination(app)
    uvicorn.run(app, host="0.0.0.0", port=8000)
