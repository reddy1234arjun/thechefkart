
from fastapi import FastAPI, HTTPException
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import warnings
from fastapi.middleware.cors import CORSMiddleware
warnings.filterwarnings("ignore") 
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from routes import user,poster

#  Define the custom tags
tags_metadata = [{
        "name": "User",
        "description": "Operations related to user",
    },
    {
        "name":"post",
        "description":"Operations related to the post"
    }
   
]
   

app = FastAPI(
    title="thechefkart",
    openapi_url="/thechefkart.json",
    version="1.0.1",
    description="thechefkart APIs",
    redoc_url="/redoc/",  # Disable Redoc (built-in docs)
    docs_url="/docs/",  # Define a custom endpoint for docs
    openapi_tags=tags_metadata,  # Use the custom tags defined here
)

# Allow CORS for development (customize origins as needed)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000  # Adjust as needed
)


# API routes from User Management
app.include_router(poster.router)
app.include_router(user.router)

# Custom exception handler to handle exceptions globally
async def custom_exception_handler(request, exc):
    if isinstance(exc, HTTPException):
        return await http_exception_handler(request, exc)

    # For other exceptions, you can return a generic error response
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


app.add_exception_handler(Exception, custom_exception_handler)

