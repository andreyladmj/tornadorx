from application import sio


@sio.on('connect', namespace='/test')
async def test_connect(sid, environ):
    await sio.emit('my response', {'data': 'Connected', 'count': 0}, room=sid,
                   namespace='/test')


@sio.on('disconnect', namespace='/test')
def test_disconnect(sid):
    print('Client disconnected')


@sio.on('disconnect request', namespace='/test')
async def disconnect_request(sid):
    await sio.disconnect(sid, namespace='/test')
