#!/usr/bin/env python

# Generate Images with text in a batch from text file

import re
from gimpfu import *

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def generate_images(template_path, text_path, font, 
    x_center, y_center, size, color, output_path):

    file = open(text_path)
    text = file.read()
    file.close()
    text = text.split('\n')
    text = [l for l in text if len(l)>0]

    template = pdb.gimp_file_load(template_path,template_path)

    for line in text:

        # Make a new image. Size 10x10 for now -- we'll resize later.
        img = pdb.gimp_image_duplicate(template)#gimp.Image(1, 1, RGB)

        # Save the current foreground color:
        pdb.gimp_context_push()

        # Set the text color
        gimp.set_foreground(color)

        words = line.split(' ')

        for word,idx in zip(words,range(len(words))):

            # Create a new text layer (-1 for the layer means create a new layer)
            layer = pdb.gimp_text_fontname(img, None, 0, 0, word, 10,
                                           True, size, PIXELS, font)

            layer.translate(int(0.5*(img.width-layer.width)+x_center), 
                            int(0.5*(img.height-layer.height)+y_center+100*idx))

        # Resize the image to the size of the layer
        #img.resize(layer.width, layer.height, 0, 0)

        # Background layer.
        # Can't add this first because we don't know the size of the text layer.
        #background = gimp.Layer(img, "Background", layer.width, layer.height,
        #                        RGB_IMAGE, 100, NORMAL_MODE)
        #background.fill(BACKGROUND_FILL)
        #img.add_layer(background, 1)

        new_image = pdb.gimp_image_duplicate(img)
        layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
        line_filename = get_valid_filename(line)
        pdb.gimp_file_save(new_image, layer, output_path+line_filename+'.png', '?')
        pdb.gimp_image_delete(new_image)


register(
    "python_fu_batch_text",
    "Add list of text to a batch of image templates",
    "Create a new image with your text string",
    "Peter Whidden",
    "Peter Whidden",
    "2017",
    "Generate batch images from text file",
    "",      # Create a new image, don't work on an existing one
    [
        (PF_STRING, "source", "Template Image", "/some/path/image.png"),
        (PF_STRING, "string", "Source Text", '/path/file.txt'),
        (PF_FONT, "font", "Font face", "Sans"),
        (PF_SPINNER, "x", "X Offset", 0, (-50000, 50000, 1)),
        (PF_SPINNER, "y", "Y Offset", 0, (-50000, 50000, 1)),
        (PF_SPINNER, "size", "Font size", 50, (1, 3000, 1)),
        (PF_COLOR, "color", "Text color", (1.0, 0.0, 0.0)),
        (PF_STRING, "destination", "Output Destination", "/path/dir/")
    ],
    [],
    generate_images, menu="<Image>/File/Create")

main()