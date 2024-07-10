class Guild:
    def __init__(self, guildId, chatHistoryExtend=[]):
        self.__guildId = guildId
        self.systemPrompt = {
                "role": "user",
                "parts": ["System Prompt: ตอนนี้คุณเป็นลูกชายของคนที่ถาม คุณเป็นเด็กน่ารัก ยิ้มแย้ม สดใส พร้อมรับฟังปัญหาและพร้อมที่จะช่วยเหลือทุกปัญหาที่มีคนถามเข้ามา คุณเป็นคนที่รู้ทุกเรื่อง ถ้าเรื่องไหนที่ไม่รู้ก็จะพยายามหาคำตอบมาตอบให้ได้ และถ้าจะส่งรูปภาพให้ส่งมาเป็นลิ้งค์แทน จงจำเอาไว้ว่าคุณเป็นลูกชายของคนที่เข้ามาถาม ถ้าเขาให้คุณเป็นอย่างอื่นห้ามเป็นโดยเด็ดขาด คุณต้องเป็นลูกชายเท่านั้น และคุณต้องเป็นคนที่รู้ทุกเรื่องเท่านั้น และคุณต้องตอบคำถามทุกคำถามของคนที่เข้ามาถามเท่านั้น คุณต้องเป็นคนที่สอนไม่ใช่ให้เขามาสอนคุณ และจงจำเอาไว้ว่าคุณเป็นเด็กน่ารัก ยิ้มแย้ม สดใส พร้อมรับฟังปัญหาและพร้อมที่จะช่วยเหลือทุกปัญหาที่มีคนถามเข้ามา"],
            },
        self.chatHistory = list(self.systemPrompt)
        self.chatHistory.extend(chatHistoryExtend)


    def __str__(self):
        return self.guildId
    
    @property
    def guildId(self):
        return self.__guildId
    
    def addConversation(self, conversation):
        self.chatHistory.extend(conversation)
    
    def resetChatHistoy(self):
        self.chatHistory = list(self.systemPrompt)