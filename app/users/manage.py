import application

print('init my event')
@application.sio.on('my event', namespace='/test')
async def test_message(sid, message):
    print('test_message', sid, message)
    await application.sio.emit('my response', {'data': "sio.sleep 0"}, room=sid,
                   namespace='/test')