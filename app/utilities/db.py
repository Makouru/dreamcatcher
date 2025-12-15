import re
import motor.motor_asyncio

from utilities.logger import log

class Database():
    def __init__(self):
        self.client = None
        self.db = None
        self.webhooks = None
        self.muted = None

    async def connect(self, host='database', port=27017):
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(f'mongodb://{host}:{port}')
            self.db = self.client['dreamcatcher']

            # init collections
            self.webhooks = self.db["webhooks"]
            self.muted = self.db["muted"]

            return True
        except Exception as e:
            log.error(f"Failed to connect to database via mongodb://{host}:{port} - {str(e)}")
            return False
        
    async def save_webhook_payload(self, payload: dict):
        try:
            result = await self.webhooks.insert_one(payload)
            return result.inserted_id
        except Exception as e:
            log.error(f"Failed to save webhook: {str(e)}")
            return None
        
    def extract_first_sentence(self, message: str) -> str:
        match = re.search(r'[!?]|\.(?!\d)(?=\s+[A-Z]|$)', message)
        if match:
            return message[:match.end()].strip()
        return message.strip()

    async def save_message_to_muted(self, message: str):
        try:
            message_already_muted = await self.message_is_muted(message)
            if message_already_muted: return -1
            result = await self.muted.insert_one({"fingerprint": str(self.extract_first_sentence(message))})
            return result.inserted_id
        except Exception as e:
            log.error(f"Failed to save new muted message: {str(e)}")
            return None 
        
    async def message_is_muted(self, message: str):
        result = await self.muted.find_one({"fingerprint": str(self.extract_first_sentence(message))})
        return result is not None
    
    async def clear_muted_collection(self):
        result = await self.muted.delete_many({})
        return result.deleted_count