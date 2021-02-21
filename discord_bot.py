import io
from multiprocessing.queues import Queue
import discord


def discord_bot(
        symbols,
        queue_request_from_store: Queue,
        queue_pipe_store_to_request: Queue,
):
    client = discord.Client()

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if not message.content.startswith('.plot'):
            return
        args = message.content.split(" ")
        if len(args) != 2:
            return "No symbol? lmao"
        symbol = args[1]
        symbol = symbol.lower()
        symbol = symbol if symbol.endswith("btc") else f"{symbol}btc"
        if symbol not in symbols:
            return f"You gave us {symbol} which is not a valid symbol!"
        queue_request_from_store.put(symbol)
        data: io.BytesIO = queue_pipe_store_to_request.get()
        file = discord.File(data, "plot.png")
        await message.channel.send(file=file)

    with open("config", "r", encoding="utf-8") as fp:
        token = fp.read()
    client.run(token)