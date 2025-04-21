import os
from dotenv import load_dotenv
import utils.helper as helper

load_dotenv()
gemini_keys = os.getenv("GEMINI_KEYS").split(',')

