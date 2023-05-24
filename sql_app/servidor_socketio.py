import uvicorn
from socketio import AsyncServer, ASGIApp, AsyncNamespace

class MyNamespace(AsyncNamespace):
    async def on_connect(self, sid, environ, auth):
        print(f"Dispositivo ({sid}) conectado.")

    async def on_disconnect(self, sid):
        print(f"Dispositivo ({sid}) desconectado.")

    async def on_newTurn(self, sid, turn):
        print('Evento newTurn')
        if turn == 'newTurn':
            print('New turn event received')
            await self.emit('refresh', 'refresh')
        else:
            print(turn)

    async def on_play(self, sid, data):
        print(f'Evento ON_PLAY recibido. Video: {data["video"]}, Sala: {data["sala"]}')
        await self.emit('play', data)
 
    async def on_volume(self, sid, data):
        print(f'Evento ON_VOLUME recibido. Volumen: {data["volume"]}, Sala: {data["sala"]}')
        await self.emit('volume', data)

    async def on_mute(self, sid, data):
        sala = data
        print(f'Evento ON_MUTE recibido. data: {sala}')
        await self.emit('mute', data)

    async def on_next(self, sid, data):
        print(f'Evento ON_NEXT recibido. Video: {data["video"]}, Sala: {data["sala"]}')
        await self.emit('next', data)

    async def on_addVideo(self, sid, data):
        print(f'Evento ON_ADD_VIDEO recibido. URL: {data["url"]}, Sala: {data["sala"]}')
        await self.emit('addVideo', data)

    async def on_quitar_video(self, sid, data):
        print(f'Evento ON_QUITAR_VIDEO recibido. URL: {data["url"]}, Sala: {data["sala"]}')
        await self.emit('quitar_video', data)


sio = AsyncServer(async_mode='asgi', cors_allowed_origins="*")
# app = ASGIApp(sio)
sio.register_namespace(MyNamespace('/'))

if __name__ == '__main__':
    # uvicorn.run(app, port=4000)
    pass
