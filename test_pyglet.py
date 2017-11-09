import pyglet

window = pyglet.window.Window(320, 180, resizable=True)

source1 = pyglet.media.load('tanioka.mp4')
source2 = pyglet.media.load('sun-chang.mp4')

player = pyglet.media.Player()
player.queue(source1)
player.queue(source2)

@window.event
def on_draw():
    player.get_texture().blit(0, 0)

player.play()
pyglet.app.run()