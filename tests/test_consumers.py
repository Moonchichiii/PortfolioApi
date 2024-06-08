import pytest
from channels.testing import WebsocketCommunicator
from backend.asgi import application  # Ensure the import is correct

@pytest.mark.asyncio
async def test_connect():
    communicator = WebsocketCommunicator(application, "/ws/chat/testroom/")
    connected, _ = await communicator.connect()
    assert connected
    await communicator.disconnect()

@pytest.mark.asyncio
async def test_send_receive_message():
    communicator = WebsocketCommunicator(application, "/ws/chat/testroom/")
    connected, _ = await communicator.connect()
    assert connected

    # Send a message
    await communicator.send_json_to({"message": "hello"})
    
    # Receive a message
    response = await communicator.receive_json_from()
    assert response["message"] == "hello"
    
    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.fixture(scope='function', autouse=True)
def clean_up_database(transactional_db):
    pass