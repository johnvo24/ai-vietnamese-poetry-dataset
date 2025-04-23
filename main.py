import utils.helper as helper
from core.poetryfix_cot_gold.poetryfix_cot_gold import *
import os
from dotenv import load_dotenv


generate_dataset(poem_csv_filepath="dataset/raw/poem_dataset.csv", poetryfix_cot_gold_csv_filepath="dataset/raw/poetryfix_cot_gold.csv")

