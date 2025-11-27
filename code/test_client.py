import httpx
import logging
from typing import Any
from uuid import uuid4
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import SendMessageRequest, MessageSendParams

async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)  

    base_url = "http://localhost:9999/"

    async with httpx.AsyncClient() as httpx_client:
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=base_url
        )

        final_agent_card_to_use = await resolver.get_agent_card()

        client = A2AClient(
            httpx_client=httpx_client,
            agent_card=final_agent_card_to_use
        )

        logger.info('A2AClient initialized.')

        send_message_payload: dict[str, Any] = {
            'message': {
                'role': 'user',
                'parts': [
                    {
                        'kind': 'text',
                        'text': 'Hi'
                    }
                ],                    
                'messageId': uuid4().hex
            }
        }

        request = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(**send_message_payload)
        )

        response = await client.send_message(request)

        logger.info(response.model_dump(mode='json',exclude_none=True))



if __name__ == "__main__":
    import asyncio

    asyncio.run(main())