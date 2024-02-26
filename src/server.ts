import WebSocket from 'ws';

const wss = new WebSocket.Server({ port: 3000 });

function broadcast(data: string) {
  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(data);
    }
  });
}

wss.on('connection', (ws: WebSocket) => {
  console.log('Client connected');

  ws.on('message', (message: string) => {
    console.log('Received:', message);

    try {
      const parsedMessage = JSON.parse(message);
      if (parsedMessage.command) {
        console.log(`Command received: ${parsedMessage.command}`);
        // Broadcast the command to all clients
        broadcast(JSON.stringify({ command: parsedMessage.command }));
      }
    } catch (error) {
      console.error('Failed to parse message as JSON:', error);
    }
  });

  // Example log message sent to the client upon connection
const welcomeLog = {
    type: 'Debug',
    message: 'Welcome to the WebSocket server!',
    details: 'You are successfully connected.',
    timestamp: new Date().toISOString(),
  };
  ws.send(JSON.stringify(welcomeLog));

  // Periodically send log messages
  const interval = setInterval(() => {
    const periodicLog = {
      type: 'info',
      message: 'Periodic log message from the server.',
      details: 'This is a test message sent every 5 seconds.',
      timestamp: new Date().toISOString(),
    };
    ws.send(JSON.stringify(periodicLog));
  }, 5000);

  ws.on('close', () => {
    console.log('Client disconnected');
  });
});