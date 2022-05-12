from fastapi import FastAPI
from endpoint import route
import uvicorn

app = FastAPI()

app.include_router(route)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
