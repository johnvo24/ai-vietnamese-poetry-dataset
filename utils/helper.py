import time
import random
from utils.dataframe_helper import *
from utils.data_helper import *
from utils.adaptive_random import AdaptiveRandom
from services.gemini_api import GeminiAI

# Time
def delay(from_=0.5, to_=2.5):
  time.sleep(random.uniform(from_, to_))

def check_gemini_key(api_keys):
  gemini_ai = GeminiAI(api_keys=api_keys)
  for key in api_keys:
    try:
      gemini_ai.generate("check")
      print(f"{key} -> Usable")
    except Exception:
      print(f"{key} -> Limited")
