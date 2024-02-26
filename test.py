import asyncio
import websockets
import json

async def test_websocket_extended():
    uri = "ws://localhost:3000"
    
    async with websockets.connect(uri) as websocket:
        # Wait for the welcome message
        welcome_message = await websocket.recv()
        print("Welcome message from server:", welcome_message)
        
        # Listen for messages for a set duration
        async def listen_for_messages(duration):
            start_time = asyncio.get_event_loop().time()
            while True:
                now = asyncio.get_event_loop().time()
                if now - start_time > duration:
                    break
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=duration - (now - start_time))
                    print("Received message from server:", message)
                except asyncio.TimeoutError:
                    break

        # Listen briefly to catch any initial messages like periodic logs
        await listen_for_messages(10)

        # Send a non-JSON message and listen for a response
        print("Sending non-JSON message...")
        await websocket.send("This is not a JSON message")
        await listen_for_messages(1)  # Adjust timing as needed

        # Check if connection is still open
        if websocket.open:
            # Send a JSON message without a command and listen for a response
            print("Sending JSON without command...")
            no_command_message = json.dumps({"not_a_command": "test"})
            await websocket.send(no_command_message)
            await listen_for_messages(1)  # Adjust timing as needed
        else:
            print("Connection was closed by the server.")

        if websocket.open:
            # Send a JSON message with wrong command and listen for a response
            print("Sending JSON with wrong command...")
            no_command_message = json.dumps({"command": "test"})
            await websocket.send(no_command_message)
            await listen_for_messages(1)  # Adjust timing as needed
        else:
            print("Connection was closed by the server.")

        # Ester egg
        if websocket.open:
            print("Sending easteregg command...")
            easteregg_message = json.dumps({"command": "easteregg"})
            await websocket.send(easteregg_message)
            await listen_for_messages(1)
        else:
            print("Connection was closed by the server.")

asyncio.get_event_loop().run_until_complete(test_websocket_extended())
