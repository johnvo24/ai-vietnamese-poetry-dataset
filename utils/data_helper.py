import re


def format_step(step: dict) -> str:
  """
  Convert step (dict) to string.
  """
  return (
    f"<error> {step['error']} "
    f"<desc> {step['desc']} "
    f"<reason> {step['reason']} "
    f"<action> {step['action']} "
    f"<replace> {step['replace']} "
    f"<line> {step['line']} "
    f"<index> {step['index']} "
    f"<effect> {step['effect']}"
  )


def parse_step(step_str: str) -> dict:
  """
  Parse tokens string to dict.
  """
  fields = ["error", "desc", "reason", "action", "replace", "line", "index", "effect"]
  step = {}
  # Regex để match từng trường theo pattern <field> content
  pattern = r"<(\w+)> (.*?)(?= <\w+>|$)"
  matches = re.findall(pattern, step_str, re.S)
  # Vòng lặp parsing
  for field, content in matches:
    if field in fields:
      step[field] = content.strip()
  # Kiểm tra nếu thiếu bất kỳ trường nào và ném lỗi
  missing_fields = [field for field in fields if field not in step]
  if missing_fields:
    raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
  
  return step

# step = {
#   "error": "TE",
#   "desc": "Từ ngữ chưa tạo hình ảnh rõ ràng.",
#   "reason": "Cần thay cụm từ mơ\n hồ bằng hình ảnh cụ thể.",
#   "action": "sáng rõ",
#   "replace": "mờ xa",
#   "line": "0",
#   "index": "4",
#   "effect": "Câu thơ trở nên trực quan và sống động hơn."
# }

# step_str = format_step(step)
# print(step_str)
# parsed_step = parse_step(step_str)
# print(parsed_step)