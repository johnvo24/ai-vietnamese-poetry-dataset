def get_init_step_prompt(err_poem):
  return f"""
Bài thơ sau có thể đang chứa lỗi. Hãy cố gắng phân tích và trả về nội dung ngắn gọn từ 1-2 câu về chủ đề của bài thơ lục bát sau đây. Tránh viết lại bài thơ:

{err_poem}

Chỉ trả về dưới dạng sau: <desc> "Mô tả ngắn gọn về chủ đề bài thơ" </desc>
"""

def get_prev_step_prompt(edited_poem, error_type, is_last_step):
  return f"""
Mô tả lỗi:
{'- SE (Structural Error): Thơ lục bát gồm các cặp câu 6-8 chữ. Câu 1 có 6 chữ, câu 2 có 8 chữ. Sai quy tắc này chính là lỗi cấu trúc.' if error_type == "SE" else ''}
{'- RE (Rhyme Error): Thơ lục bát có tiếng cuối câu 6 – tiếng thứ 6 câu 8 – tiếng cuối câu 8 cùng vần với nhau. Sai quy tắc này chính là lỗi vần.' if error_type == "RE" else ''}
{'- TE (Tone Error): Thanh trắc gồm các từ có dấu: sắc, hỏi, ngã, nặng. Thanh bằng gồm các từ có dấu huyền hoặc thanh ngang. Câu lục: Tiếng 2-4-6 theo thứ tự Bằng (B) - Trắc (T) - Bằng (B). Câu bát: Tiếng 2-4-6-8 theo B-T-B-B (hoặc biến thể: T-B-T-B).' if error_type == "TE" else ''}
{'- ME (Meaning Error): Nội dung thơ không rõ ràng hoặc lệch chủ đề.' if error_type == "ME" else ''}
{'- IE (Imagery Error): Hình ảnh thơ không rõ ràng, mơ hồ, khiên cưỡng, sáo rỗng, mâu thuẫn hoặc không gợi cảm xúc, khiến người đọc khó hình dung và cảm nhận được ý thơ.' if error_type == "IE" else ''}

Step structure (Bước suy luận sửa lỗi phải đủ các token sau và không tự thêm token nào khác nữa):
<error> {error_type}
<desc> Mô tả lỗi và ảnh hưởng của nó. 
<reason> Suy luận chi tiết ra hướng giải quyết. 
<action> Từ, cụm từ, câu thay thế <replace> Từ, cụm từ, câu cũ <line> Dòng số mấy <index> Vị trí thứ mấy của dòng. 
<effect> Hiệu quả sửa đổi và đánh giá chất lượng bài thơ sau bước sửa. {'(Nội dung này quan trọng để xác định rằng đã sửa xong bài thơ)' if is_last_step else ''}
{'<eos>' if is_last_step else '<eois>'}

Hãy đóng vai trò là một Data Engineer chuyên nghiệp. Hãy tạo một lỗi ngẫu nhiên bằng cách thay thế bất kỳ từ, cụm từ hoặc câu vào trong bài thơ đích, và sau đó sinh ra bước sửa thơ cho lỗi đó dựa trên cấu trúc trên.
Lưu ý: Không thay đổi số dòng của bài thơ.
Sau đây là bài thơ đích:

{edited_poem}

Chỉ trả về dưới dạng sau: <poem> "Bài thơ lỗi trong cặp token poem" </poem> <step>"Bước sửa thơ trong cặp token step" </step>
"""