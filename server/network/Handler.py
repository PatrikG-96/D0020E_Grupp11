import asyncio

class Handler:

    def __init__(self, max_size):
        self.max_size = max_size
        self.client_list = []

    async def handle_clients(self, reader, writer):
        request = None

        while True:
            request = (await reader.read(self.max_size)).decode()
