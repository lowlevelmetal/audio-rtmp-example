import asyncio
import logging

from pyrtmp import StreamClosedException
from pyrtmp.rtmp import SimpleRTMPController, RTMPProtocol, SimpleRTMPServer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# The RTMP library I use requires a class with a set of callbacks for handling
# RTMP messages.
class RTMPController(SimpleRTMPController):

    def __init__(self):
        logging.info("RTMPController init")
        super().__init__()

    # Here you would want to setup buffers and initialize logic that will use audio and video data
    async def on_ns_publish(self, session, message) -> None:
        logging.info(f"on_ns_publish")
        await super().on_ns_publish(session, message)

    # Here you would typically want to write some sort of function that would use av metadata
    # to configure a transcoder or reconfigure an output device to support the type of incoming
    # data
    async def on_metadata(self, session, message) -> None:
        logging.info(f"on_metadata: {message}")
        await super().on_metadata(session, message)

    # Self explanatory, recieve video data
    async def on_video_message(self, session, message) -> None:
        logging.info(f"on_video_message: {message.timestamp}")
        await super().on_video_message(session, message)

    # Self explanatory, recieve audio data
    async def on_audio_message(self, session, message) -> None:
        logging.info(f"on_audio_message: {message.timestamp}")
        await super().on_audio_message(session, message)

    # Self explanatory, cleanup area
    async def on_stream_closed(self, session, exception: StreamClosedException) -> None:
        logging.info(f"on_stream_closed")
        await super().on_stream_closed(session, exception)


class SimpleServer(SimpleRTMPServer):

    def __init__(self):
        super().__init__()

    async def create(self, host: str, port: int):
        loop = asyncio.get_event_loop()
        self.server = await loop.create_server(
            lambda: RTMPProtocol(controller=RTMPController()),
            host=host,
            port=port,
        )


async def main():
    server = SimpleServer()
    await server.create(host='0.0.0.0', port=1935)
    await server.start()
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())