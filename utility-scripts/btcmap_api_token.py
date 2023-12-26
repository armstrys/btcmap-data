
import os
import sys
from dotenv import load_dotenv


# Get the bearer token from the environment variable
load_dotenv()
BTCMAP_API_TOKEN = os.getenv("BTCMAP_API_TOKEN")

if not BTCMAP_API_TOKEN:
    print("Please set the BTCMAP_API_TOKEN environment variable.")
    sys.exit(1)