import os

PORT = int(os.getenv("PORT", "8080"))
HOST = os.getenv("HOST", "127.0.0.1")
ENV  = os.getenv("ENV", "DEV")