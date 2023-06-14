import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pyngrok import ngrok, conf
from dotenv import load_dotenv
import yaml

# Load environment variables
load_dotenv()

# Set the ngrok auth token and region
conf.get_default().auth_token = os.getenv("NGROK_AUTH_TOKEN")
# conf.get_default().region = os.getenv("NGROK_REGION")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    config_file = open('ngrok_app\\ngrok.yml')
    config = yaml.safe_load(config_file)
    
    # Open a ngrok tunnel
    # url = ngrok.connect(int(os.getenv("PORT")),).public_url
    print(f"Creando tunel...")
    url = ngrok.connect(**config['tunnels']['tunel_cm_esperanza']).public_url
    print(f"Public URL: {url}")

@app.get("/")
def read_root():
    return {"Hello": "world"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,port=int(os.getenv("NGROK_SERVER_PORT", 8000)))