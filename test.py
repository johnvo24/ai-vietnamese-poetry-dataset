from core.poetryfix_gold_data.poetryfix_gold_data import *
from utils.adaptive_random import AdaptiveRandom
import random

# print(generate_init_step(err_poem="Con cò mà đi ăn đêm\nĐậu phải cành mềm lộn cổ lên ao"))
# print(generate_prev_step(edited_poem="Con cò mà đi ăn đêm\nĐậu phải cành mềm lộn cổ lên ao", error_type="FE", is_last_step=True))
# reasoning_steps = generate_reasoning_chain(original_poem="Con cò mà đi ăn đêm\nĐậu phải cành mềm lộn cổ lên ao", num_steps=4)
# for step in reasoning_steps:
#   print(step)

# generate_dataset(poem_csv_filepath="dataset/raw/poem_dataset.csv", poetryfix_cot_gold_csv_filepath="dataset/raw/poetryfix_cot_gold.csv")

# helper.check_gemini_key(os.getenv("GEMINI_KEYS").split(','))

# df = pd.read_csv('dataset/raw/poem_dataset.csv')
# print(len(df))