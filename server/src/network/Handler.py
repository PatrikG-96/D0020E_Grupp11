import asyncio

class Handler:

    def __init__(self, max_size):
        self.max_size = max_size
        self.clients = {}

    async def handle_clients(self, reader, writer):
        request = None

        while True:
            request = (await reader.read(self.max_size)).decode()

    async def sendToClient(self, user_id, message):
        client = self.clients[user_id]
        writer = client.getWriter()
        writer.write(message.encode())
        await writer.wait_closed()