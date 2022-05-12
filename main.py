from fastapi_pagination import add_pagination
import uvicorn

from endpoint import app


add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
