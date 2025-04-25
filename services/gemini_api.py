from google import genai
from google.genai import types

class GeminiAI():
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.current_key_index = -1
        
    def _init_client(self):
        api_key = self.api_keys[self.current_key_index]
        self.client = genai.Client(api_key=api_key)
        # print(f"API Key: {api_key}")

    def switch_to_next_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self._init_client()

    def generate(self, prompt):
        self.switch_to_next_key()
        try:
            response =  self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=f"{prompt}",
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=1000
                ),
            )
            return response.text
        except Exception as e:
            self.switch_to_next_key()
            raise Exception(f"❌ Lỗi API: {e}")

# for i in range(0, 1):
#     print(generate(prompt="Viết bài thơ lục bát tặng mẹ ngày 8/3").text)
#     time.sleep(random.uniform(1, 2))
    
# geminiAI = GeminiAI()
# print(geminiAI.correct_spelling("(gửi Đà Lạt)\nThầm cám ơn người nhắc xứ mơ\nGóc phố còn nguyên, sương vẫn mờ\nQuanh co lối rẽ, từng con dốc\nHoa cỏ hiền ngoan dệt khúc thơ\nNhớ quá đi thôi, duới mái trường\nTung tăng buớm trắng - tóc thơm hương\nTa - người - đôi bạn - như đôi bướm\nDệt mộng mơ đầu, thương quá thương\nĐây hồ Tuyền Lâm, kia Cam Ly\nVui đùa bên nhau, chẳng chia lìa\nMong ngày thêm giờ, luôn dài mãi\nĐể hoàng hôn còn kết ý thi\nCuối tuần Thủy Tạ - ta bên nhau\nThanh Thủy - Đồi Cù - ướp tình đầu\nBên kia Dinh Thự - vua Bảo Đại\nTa dệt cùng người - mộng ước sau !\nBên Thung Lung Tình - cội tơ lòng\nTên ai khắc mãi, vách nhà không\nRung rinh hoa tím bên hồ ấy\nNhè nhẹ buông rơi, nắng chớm hồng\nĐà Lạt xưa rồi, xa quá xa\nBên khung trời ấy, có người - ta !\nMong ngày hội ngộ - duyên xưa, gặp\nTa ôm chầm đất - hôn nhạt nhòa\nPhố núi bây giờ, nhớ dáng hoa\nTa gửi tình mình giữa trăng ngà\nNhờ mây nhắn gió về nơi ấy\nGiữ lại mộng đầu, tuổi thơ qua\nCao nguyên phố mộng, lạnh mênh mông\nBên này xa xứ, ta lạnh lòng\nTim vừa lạnh giá, hồn hiu quạnh\nBởi mong ngày về - ngọt hương trong !\nDã Qùy - HBL").text)
# print(geminiAI.generate("Bình phương kết quả trên").text)