import pygame
from os import walk

def import_folder(path):
    surfaces = []

    for _, __, files in walk(path):
        for filename in sorted(files):
            full_path = f"{path}/{filename}"
            image = pygame.image.load(full_path).convert_alpha()
            image = pygame.transform.scale(image, (96, 96))
            surfaces.append(image)

    return surfaces

    # load all images inside a folder and return them as a list of Surfaces.
    # the images are sorted alphabetically to ensure consistent indexing.
