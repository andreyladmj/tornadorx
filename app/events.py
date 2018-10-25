import application

@application.sio.on('connect', namespace='/test')
async def test_connect(sid, environ):
    print('test_connect')
    await application.sio.emit('my response', {'data': 'Connected', 'count': 0}, room=sid,
                   namespace='/test')


@application.sio.on('disconnect', namespace='/test')
def test_disconnect(sid):
    print('Client disconnected')


@application.sio.on('disconnect request', namespace='/test')
async def disconnect_request(sid):
    print('disconnect_request')
    await application.sio.disconnect(sid, namespace='/test')
