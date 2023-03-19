from socketio import AsyncServer, ASGIApp

sio = AsyncServer(async_mode='asgi', cors_allowed_origins='*')

@sio.event
async def connect(sid, environ, auth):
    # print(f"Server is running on port {app.config.PORT}")
    print(f"Dispositivo ({sid}) conectado.")

@sio.event
async def disconnect(sid):
    # print(f"Server is running on port {app.config.PORT}")
    print(f"Dispositivo ({sid}) desconectado.")

@sio.on('newTurn')
async def newTurn(sid, turn):
    print('Evento newTurn')
    if turn == 'newTurn':
        print('New turn event received')
        await sio.emit('refresh', 'refresh', broadcast=True)
    else:
        print(turn)
