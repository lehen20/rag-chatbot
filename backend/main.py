from fastapi import FastAPI
from database import Base, engine
from routers import complaint_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Grievance Chatbot API")

# Include the router
app.include_router(complaint_router)

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)