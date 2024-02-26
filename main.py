import asyncio
import websockets
import json
from datetime import datetime

connected_clients = set()

async def broadcast(data, sender=None):
    for client in connected_clients:
        if client != sender:
            await client.send(data)


async def forward_command_to_pi(command):
    # TODO
    pass

# List of valid commands
valid_commands = ["pause", "resume", "easteregg"]


async def handle_connection(websocket, path):
    connected_clients.add(websocket)
    print("Client connected")

    try:
        ### === REMOVE === ### ------------------------------------------------------------------------------------
        # Send a welcome message to the client upon connection
        welcome_log = {
            "type": "info",
            "message": "Welcome to the WebSocket server!",
            "details": "You are successfully connected.",
            "timestamp": datetime.now().isoformat(),
        }
        await websocket.send(json.dumps(welcome_log))

        # Periodically send log messages
        async def send_periodic_messages():
            while True:
                await asyncio.sleep(5)  # Wait for 5 seconds
                periodic_log = {
                    "type": "info",
                    "message": "Periodic log message from the server.",
                    "details": "This is a test message sent every 5 seconds.",
                    "timestamp": datetime.now().isoformat(),
                }
                await websocket.send(json.dumps(periodic_log))

        # Start the periodic message task
        periodic_task = asyncio.create_task(send_periodic_messages())

        ### === END REMOVE === ### ---------------------------------------------------------------------------------

        # Handle incoming messages
        async for message in websocket:
            print("Received:", message)
            try:
                parsed_message = json.loads(message)
                if "command" in parsed_message.keys():
                    cmd = parsed_message["command"]
                    if cmd in valid_commands:
                        if cmd == "easteregg":
                            print("Easter egg activated!")
                            await broadcast(json.dumps({
                                "type": "special_event",
                                "message": "Easter egg activated!",
                                "details": "The easter egg was activated by a client.",
                                "timestamp": datetime.now().isoformat(),
                            }), sender=websocket)
                        print(f"Command received: {cmd}")
                        await forward_command_to_pi(cmd)
                    
                    else:
                        print(f"Invalid command: {cmd}")
                        await websocket.send(json.dumps({
                            "type": "server_error",
                            "message": "Invalid command",
                            "details": f"The command '{cmd}' is not valid.",
                            "timestamp": datetime.now().isoformat(),
                        }))
                else:
                    print("Received message does not contain a command")
                    await websocket.send(json.dumps({
                        "type": "server_error",
                        "message": "Invalid message",
                        "details": "The received message does not contain a command.",
                        "timestamp": datetime.now().isoformat(),
                    }))
        
            except json.JSONDecodeError:
                print("Failed to parse message as JSON")
                await websocket.send(json.dumps({
                    "type": "server_error",
                    "message": "Invalid message",
                    "details": "The received message is not valid JSON.",
                    "timestamp": datetime.now().isoformat(),
                }))
    
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        # Cleanup
        connected_clients.remove(websocket)
        periodic_task.cancel()

# Start the WebSocket server
start_server = websockets.serve(handle_connection, "localhost", 3000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
