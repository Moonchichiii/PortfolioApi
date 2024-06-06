import pytest
from channels.testing import WebsocketCommunicator
from backend.asgi import application

@pytest.mark.asyncio
async def test_connect():
    communicator = WebsocketCommunicator(application, "/ws/chat/")
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.disconnect()

@pytest.mark.asyncio
async def test_send_receive_message():
    communicator = WebsocketCommunicator(application, "/ws/chat/")
    connected, subprotocol = await communicator.connect()
    assert connected

    message = {'type': 'chat.message', 'message': 'hello'}
    await communicator.send_json_to(message)

    response = await communicator.receive_json_from()
    assert response['message'] == 'hello'

    await communicator.disconnect()
