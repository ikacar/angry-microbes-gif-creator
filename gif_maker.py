from distutils.command.build_scripts import first_line_re
from PIL import Image
import glob

WIDTH = 560
HEIGHT = 560

bubbles_velocity = -35
subject_velocity = 4

orientation = 1
start_position = True
subject_width_position = 0
subject_height_position = 0
bubbles_position = 0


background_images = glob.glob('backgrounds/*.png')

bubbles_images = glob.glob('bubbles/*.png')

subject_images = glob.glob('subjects/*.png')


def ud_animation(frame, background_img, bubbles_img, subject_img):

    global orientation
    global subject_width_position
    global subject_height_position
    global bubbles_position
    global start_position

    if start_position:
        subject_width_position = int(WIDTH/2 - subject_img.width/2)
        subject_height_position = int(HEIGHT/2 - subject_img.height/2)
        start_position = False
        bubbles_position = 0

    # CREATE NEW IMAGE WITH PROPPER WIDTH AND HEIGHT
    img = Image.new('RGB', (WIDTH,HEIGHT))
    # APPEND BACKGROUND
    img.paste(background_img, (0,0), background_img)
    # APPEND BUBBLES WITH MOVING VELOCITY
    img.paste(bubbles_img, (50,bubbles_position), bubbles_img)
    bubbles_position = bubbles_position + bubbles_velocity
    if frame % 4 == 0:
        orientation = -orientation
    else:
        subject_height_position = subject_height_position + subject_velocity*orientation

    img.paste(subject_img, (subject_width_position, subject_height_position), subject_img)
    return img
    # img.save('test/'+str(frame)+'.png',"PNG")

def save_frames_to_gif(frames, name):
    frames[0].save(name + '.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=170, loop=0)

counter = 1
for background in background_images:
    
    for bubbles in bubbles_images:

        for subject in subject_images:
            # reset to start positions
            start_position = True 

            # load images
            background_img = Image.open(background)
            bubbles_img = Image.open(bubbles)
            subject_img = Image.open(subject)

            frames = []
            frame = 16
            while frame > 0:

                frames.append(ud_animation(frame,background_img, bubbles_img, subject_img))

                frame = frame - 1

            counter = counter + 1
            save_frames_to_gif(frames, 'result/'+ str(counter))

