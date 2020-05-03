from PIL import Image

frames = []
for i in range(101):
        im = Image.open('frames/frame'+str(i)+'.png')
        frames.append(im)

frames[0].save('moving_PSO.gif', format='GIF', append_images=frames[1:], save_all=True, duration=10, loop = 0)