from fastapi import FastAPI
from api.auth import endpoints as auth_endpoints
from api.events import endpoints as event_endpoints
from api.events import endpoints as event_endpoints
from database import Base,engine
from loguru import logger
import sys
import datetime
from api.users import endpoints as user_endpoints
from api.tickets import endpoints as ticket_endpoints
from api.ticket_purchased import endpoints as tkt_purch_endpoints

# Define the log file format and rotation
log_format = "{time:MMMM D, YYYY > HH:mm:ss} |  {level} <level> {message}</level>"
log_file = f"logs/{datetime.datetime.now().strftime('%Y-%m-%d')}.log"

# Add logger configuration
logger.remove()
logger.add(log_file, format=log_format, rotation="1 day")


app = FastAPI()

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# Mounting authentication endpoints
app.include_router(auth_endpoints.router)
app.include_router(event_endpoints.router)
app.include_router(user_endpoints.router)
app.include_router(ticket_endpoints.router)
app.include_router(tkt_purch_endpoints.router)
# , prefix="/auth"
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

