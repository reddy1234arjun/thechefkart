import os
import logging
import re
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(filename='chefcart.log', level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv("credentials.env")

DATABASE_URL = os.getenv('DATABASE_URL')

logger.info("This is an info message")
