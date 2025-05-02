from services.gemini_api import GeminiAI
from core.poetryfix_gold_data.prompt_templates import *
import re
from utils import helper
from utils.helper import AdaptiveRandom
import random
import pandas as pd
import copy

import os
from dotenv import load_dotenv
load_dotenv()

api_keys = os.getenv("GEMINI_KEYS").split(',')

gemini_ai = GeminiAI(api_keys=api_keys)

def generate_init_step(err_poem):
  prompt = get_init_step_prompt(err_poem=err_poem)
  try:
    response = gemini_ai.generate(prompt=prompt)
    desc_match = re.search(f"<desc>(.*?)</desc>", response, re.DOTALL)
    if desc_match:
      desc = desc_match.group(1).strip()
      return {"step": f"""<error> CONTEXT 
<desc> {desc}
<reason> 
<action> <replace> <line> <index> 
<effect> 
<eois>"""} 
    else: return None
  
  except Exception as e:
    # print(f"API ERROR: {e}")
    return None

def generate_prev_step(edited_poem, error_type, error_line, is_last_step):
  prompt = get_prev_step_prompt(edited_poem=edited_poem, error_type=error_type, error_line=error_line, is_last_step=is_last_step)
  try:
    response = gemini_ai.generate(prompt=prompt)
    poem_match = re.search(f"<poem>(.*?)</poem>", response, re.DOTALL)
    step_match = re.search(f"<step>(.*?)</step>", response, re.DOTALL)
    if poem_match and step_match:
      poem = poem_match.group(1).strip()
      step = step_match.group(1).strip()
      return {"poem": poem, "step": step}
    else: return None
  
  except Exception as e:
    # print(f"API ERROR: {e}")
    return None
  
def get_error_type(current_step, num_steps, adaptiveRandoms):
  adaptiveRandom1, adaptiveRandom2 = adaptiveRandoms
  if num_steps == 2:
    return adaptiveRandom1.choose() if random.uniform(0.0, 1.0) <= 0.5 else adaptiveRandom2.choose()
  elif num_steps == 3:
    if (current_step-1)/2 < 1/2: return adaptiveRandom1.choose() if random.uniform(0.0, 1.0) <= 0.7 else adaptiveRandom2.choose()
    else: return adaptiveRandom1.choose() if random.uniform(0.0, 1.0) <= 0.2 else adaptiveRandom2.choose()
  else:
    if (current_step-1)/(num_steps-1) < 1/3: return adaptiveRandom1.choose() if random.uniform(0.0, 1.0) <= 0.9 else adaptiveRandom2.choose()
    elif (current_step-1)/(num_steps-1) < 2/3: return adaptiveRandom1.choose() if random.uniform(0.0, 1.0) <= 0.3 else adaptiveRandom2.choose()
    else: return adaptiveRandom1.choose() if random.uniform(0.0, 1.0) <= 0.1 else adaptiveRandom2.choose()
  
  
def generate_reasoning_chain(original_poem, num_steps):
  reasoning_chain = []
  current_poem = original_poem

  adaptiveRandom1 = AdaptiveRandom(values=["SE", "RE", "TE"])
  adaptiveRandom2 = AdaptiveRandom(values=["ME", "IE"])

  # Generate Final step -> Inter step -> Init step
  error_type = get_error_type(current_step=num_steps-1, num_steps=num_steps, adaptiveRandoms=(adaptiveRandom1, adaptiveRandom2))
  error_line = (num_steps-1 + random.randint(-1, 2)) % (str(current_poem).count('\n')+1)
  error_line = (str(current_poem).count('\n')+1) if error_line == 0 else error_line
  final_step = None
  while not final_step:
    final_step = generate_prev_step(edited_poem=current_poem, error_type=error_type, error_line=error_line, is_last_step=True)
    helper.delay(0.1, 0.5)
  reasoning_chain.append({
    "original_poem": original_poem,
    "step_index": num_steps-1,
    "error_poem": final_step["poem"],
    "step_content": final_step["step"],
    "edited_poem": original_poem
  })
  current_poem = final_step["poem"]
  print(f"Final[{error_type},l{error_line}]", end=' -> ')

  for i in range(num_steps-2, 0, -1):
    error_type = get_error_type(current_step=i, num_steps=num_steps, adaptiveRandoms=(adaptiveRandom1, adaptiveRandom2))
    error_line = (i + random.randint(-1, 2)) % (str(current_poem).count('\n')+1)
    error_line = (str(current_poem).count('\n')+1) if error_line == 0 else error_line
    inter_step = None
    while not inter_step:
      inter_step = generate_prev_step(edited_poem=current_poem, error_type=error_type, error_line=error_line, is_last_step=False)
      helper.delay(0.1, 0.5)
    reasoning_chain.insert(0, {
      "original_poem": original_poem,
      "step_index": i,
      "error_poem": inter_step["poem"],
      "step_content": inter_step["step"],
      "edited_poem": current_poem
    })
    current_poem = inter_step["poem"]
    print(f"Inter[{error_type},l{error_line}]", end=' -> ')

  
  init_step = None
  while not init_step:
    init_step = generate_init_step(err_poem=current_poem)
    helper.delay(0.1, 0.5)
  reasoning_chain.insert(0, {
    "original_poem": original_poem,
    "step_index": 0,
    "error_poem": current_poem,
    "step_content": init_step["step"],
    "edited_poem": current_poem
  })
  print(f"Init[CONTEXT]", end=f' [{num_steps}]\n')


  return reasoning_chain

def generate_dataset(poem_csv_filepath: str, poetryfix_dataset_csv_filepath: str, save_step=25):
  # Read lucbat dataset
  df = pd.read_csv(poem_csv_filepath).dropna(subset=["content"]).drop_duplicates(subset="content")
  poems = df["content"].to_list()[100: 6000]

  # Read poetryfix_dataset.csv file
  if os.path.exists(poetryfix_dataset_csv_filepath):
    pfcg_df = pd.read_csv(poetryfix_dataset_csv_filepath)
  else:
    pfcg_df = pd.DataFrame(columns=["original_poem", "step_index", "error_poem", "step_content", "edited_poem"])
  print(f"DATASET: {pfcg_df.shape}")

  counter = 0
  for poem in poems:
    if poem in pfcg_df["original_poem"].values: continue
    # Count lines of the poem to determine num_steps
    line_count = poem.strip().count('\n') + 1
    weights = [25, 30, 30, 10, 4, 1] if line_count <= 2 else [15, 25, 25, 25, 8, 2] if line_count <= 4 else [10, 15, 20, 20, 20, 15]
    num_steps=random.choices([2, 3, 4, 5, 6, 7], weights=weights, k=1)[0]
    
    print(f"Generate CoT:", end=f'[{line_count} LINES] >>> ')
    chain = generate_reasoning_chain(original_poem=poem, num_steps=num_steps)
    chain_df = pd.DataFrame(chain)

    pfcg_df = pd.concat([pfcg_df, chain_df], axis=0, ignore_index=True)
    counter += 1
    if (counter >= save_step):
      pfcg_df.to_csv(poetryfix_dataset_csv_filepath, index=False, encoding='utf-8-sig')
      print(f"DATASET: {pfcg_df.shape}")
      counter = 0

  pfcg_df.to_csv(poetryfix_dataset_csv_filepath, index=False, encoding='utf-8-sig')

def convert_poetryfix_dataset_to_gold_data(poetryfix_dataset_csv_filepath):
  df = pd.read_csv(poetryfix_dataset_csv_filepath)
  grouped = df.groupby('original_poem')

  reasonings_dict = {
    poem.strip(): group[['step_index', 'error_poem', 'step_content', 'edited_poem']].sort_values('step_index').to_dict(orient='records') for poem, group in grouped
  }
  _reasonings_dict = copy.deepcopy(reasonings_dict)

  for key, steps in reasonings_dict.items():
    reasoning_memory = ""
    for idx, _ in enumerate(steps):
      try:
        pased_step = helper.parse_step(step_str=_reasonings_dict[key][idx]['step_content'], is_last_step=True) if idx == (len(steps)-1) else helper.parse_step(step_str=_reasonings_dict[key][idx]['step_content'], is_last_step=False)
        if idx == 0: 
          reasoning_memory = f"<reasoning_memory> Tóm tắt ngữ cảnh: {pased_step['desc']} <eois>"
          _reasonings_dict[key][idx]['error_poem'] = f"<sop> {_reasonings_dict[key][idx+1]['error_poem']} <eop>"
          _reasonings_dict[key][idx+1]['error_poem'] = f"<sop> {_reasonings_dict[key][idx+1]['error_poem']} <eop> {reasoning_memory}"
        elif idx != (len(steps)-1): 
          reasoning_memory = f"{reasoning_memory} Sửa lỗi {pased_step['error']}: Thay \"{pased_step['replace']}\" bằng \"{pased_step['action']}\" ở dòng {pased_step['line']} tại từ thứ {pased_step['index']} <eois>"
          _reasonings_dict[key][idx+1]['error_poem'] = f"<sop>{_reasonings_dict[key][idx+1]['error_poem']} <eop> {reasoning_memory}"
      except Exception as e:
        # Thieu key thi loai bo
        del _reasonings_dict[key]
        break

  rows = []
  for key, steps in _reasonings_dict.items():
    for step in steps:
      row = {"original_poem": key}
      row.update(step)
      rows.append(row)
  
  df_result = pd.DataFrame(rows)
  df_result.to_csv("dataset/processed/poetryfix_gold_data.csv", index=False)
  print(f"Dataset: {len(reasonings_dict.items())} => {len(_reasonings_dict.items())} poems ~ {len(df_result)} samples")