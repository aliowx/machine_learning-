from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.chat_bot import ChatbotCreate, ChatbotResponse
from app import crud
from app import exceptions as exc
from app.utils import MessageCodes
from typing import Optional, List
import aiohttp
import logging

logger = logging.getLogger(__name__)

class ChatbotService:
    def __init__(self, http_session: Optional[aiohttp.ClientSession] = None):
        """
        Initialize ChatbotService with an optional HTTP client session.
        
        Args:
            http_session (Optional[aiohttp.ClientSession]): HTTP session for API calls.
        """
        self.http_session = http_session or aiohttp.ClientSession()
        logger.info("ChatbotService initialized.")

    async def process_message(
        self,
        db: AsyncSession,
        chat_message: ChatbotCreate,
        user_id: Optional[int] = None
    ):

        try:

            if not chat_message.message.strip():
                logger.warning("Empty message received for user_id: %s", user_id)
                raise exc.AlreadyExistException(
                    detail="Message cannot be empty",
                    msg_code=MessageCodes.bad_request
                )


            chat = await crud.chat.create_chat_message(
                db=db,
                chat=chat_message,
                user_id=user_id
            )
            if not chat:
                logger.error("Failed to save message for user_id: %s", user_id)
                raise exc.NotFoundException(
                    detail="Unable to save chat message",
                    msg_code=MessageCodes.not_found
                )


            response_text = await self._generate_response(
                message=chat_message.message,
                conversation_id=chat_message.conversation_id
            )


            bot_message = ChatbotCreate(
                message=response_text,
                conversation_id=chat.conversation_id,
                is_bot=True
            )
            bot_chat = await crud.chat.create_chat_message(
                db=db,
                chat=bot_message,
                user_id=None
            )

            return ChatbotResponse(
                id=bot_chat.id,
                message=bot_chat.message,
                conversation_id=bot_chat.conversation_id,
                is_bot=bot_chat.is_bot,
                created_at=bot_chat.created_at
            )

        except exc.BaseCustomException as e:
            logger.error("Custom exception: %s, Code: %s", e.detail, e.msg_code)
            raise
        except Exception as e:
            logger.error("Unexpected error: %s", str(e), exc_info=True)
            raise exc.ServiceException(
                detail="Internal error processing message",
                msg_code=MessageCodes.internal_error
            )

