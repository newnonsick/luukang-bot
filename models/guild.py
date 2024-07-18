class Guild:
    def __init__(self, guildId, chatHistoryExtend=[]):
        self.__guildId = guildId
        self.chatHistory = list()
        self.chatHistory.extend(chatHistoryExtend)


    def __str__(self):
        return self.guildId
    
    @property
    def guildId(self):
        return self.__guildId
    
    def addConversation(self, conversation):
        self.chatHistory.extend(conversation)
    
    def resetChatHistoy(self):
        self.chatHistory = list()