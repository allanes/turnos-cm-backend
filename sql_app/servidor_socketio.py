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
            await self.emit('refresh', 'refresh', broadcast=True)
        else:
            print(turn)

sio = AsyncServer(async_mode='asgi', cors_allowed_origins="*")
# app = ASGIApp(sio)
sio.register_namespace(MyNamespace('/'))

if __name__ == '__main__':
    # uvicorn.run(app, port=4000)
    pass
