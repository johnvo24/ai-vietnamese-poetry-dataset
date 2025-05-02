import utils.helper as helper
from core.poetryfix_gold_data.poetryfix_gold_data import *
import os
from dotenv import load_dotenv

# Generate poetryfix_gold_data dataset for training the policy model initially
# generate_dataset(poem_csv_filepath="dataset/raw/poem_dataset.csv", poetryfix_dataset_csv_filepath="dataset/raw/poetryfix_dataset.csv", save_step=25)

# Convert poetryfix_dataset to poetryfix_gold_dataset for SFT training
convert_poetryfix_dataset_to_gold_data(poetryfix_dataset_csv_filepath="dataset/raw/poetryfix_dataset.csv")