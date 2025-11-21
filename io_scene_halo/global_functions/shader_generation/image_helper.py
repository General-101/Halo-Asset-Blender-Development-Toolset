# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2023 Steven Garcia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ##### END MIT LICENSE BLOCK #####

import os
import math
import numpy as np
from PIL import Image
from collections import deque

def is_power_of_two(n):
    return n > 0 and (n & (n - 1) == 0)

def save_image(img, out_dir, name):
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, name))

def is_color_plate(img):
    w, h = img.size
    palette = [img.getpixel((i, 0)) for i in range(3)]
    mask = palette[0]
    border = palette[1]
    filler = palette[2]

    is_color_plate = True
    if mask == border:
        is_color_plate = False
    
    if is_color_plate:
        border_pixels = []
        for x in range(w):
            border_pixels.append(img.getpixel((x, 0)))
            border_pixels.append(img.getpixel((x, h - 1)))
        for y in range(h):
            border_pixels.append(img.getpixel((0, y)))
            border_pixels.append(img.getpixel((w - 1, y)))

        is_color_plate = all(p in palette for p in border_pixels)

    return is_color_plate, palette

def flood_fill(img, start, palette, visited):
    w, h = img.size
    pixels = img.load()
    x0, y0 = start
    q = deque([start])
    visited[x0][y0] = True
    minx, miny, maxx, maxy = x0, y0, x0, y0

    while q:
        x, y = q.popleft()
        minx, miny = min(minx, x), min(miny, y)
        maxx, maxy = max(maxx, x), max(maxy, y)

        for nx, ny in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= nx < w and 0 <= ny < h and not visited[nx][ny]:
                if pixels[nx, ny] not in palette:
                    visited[nx][ny] = True
                    q.append((nx, ny))

    return (minx, miny, maxx+1, maxy+1)

def group_islands_into_sequences(islands):
    islands.sort(key=lambda box: (box[1], box[0])) 
    sequences = []

    while islands:
        row = []
        first = islands.pop(0)
        row.append(first)

        _, y0, _, y1 = first
        row_height = y1 - y0

        i = 0
        while i < len(islands):
            x0, y0c, x1, y1c = islands[i]
            if abs(y0c - y0) < row_height // 2:
                row.append(islands.pop(i))
            else:
                i += 1
        sequences.append(row)

    return sequences

def extract_colorplate_faces(img, palette):
    w, h = img.size
    visited = [[False]*h for _ in range(w)]
    pixels = img.load()

    islands = []
    for y in range(h):
        for x in range(w):
            if not visited[x][y] and pixels[x, y] not in palette:
                box = flood_fill(img, (x, y), palette, visited)
                bw, bh = box[2]-box[0], box[3]-box[1]
                if not (is_power_of_two(bw) and is_power_of_two(bh)):
                    print("Skipping non power of 2 island at %s (%sx%s)" % (box, bw, bh))
                    continue
                islands.append(box)

    sequences = group_islands_into_sequences(islands)

    face_sequences = []
    for seq_idx, seq in enumerate(sequences):
        faces = []
        for face_idx, (x0, y0, x1, y1) in enumerate(seq):
            face = img.crop((x0, y0, x1, y1))
            faces.append(face)

        face_sequences.append(faces)

    return face_sequences

def extract_t_faces(img):
    w, h = img.size
    if w % 4 != 0 or h % 3 != 0:
        print("Not a valid 4x3 T-shape image (%sx%s)" % (w, h))
        return None

    face_w, face_h = w // 4, h // 3
    if face_w != face_h or not is_power_of_two(face_w):
        print("Face size must be square and power of two. got %sx%s" % (face_w, face_h))
        return None

    coords = [
        ((2,1), "posx"), 
        ((0,1), "negx"),
        ((0,0), "posy"),
        ((0,2), "negy"),
        ((1,1), "posz"),
        ((3,1), "negz"),
    ]

    faces = []
    for coord, face_name in coords:
        cx, cy = coord
        x0, y0 = cx * face_w, cy * face_h
        face = img.crop((x0, y0, x0 + face_w, y0 + face_h))
        faces.append(face)

    return faces

def direction_to_face_uv(rd):
    x, y, z = rd
    ax, ay, az = abs(x), abs(y), abs(z)
    if ax >= ay and ax >= az:
        if x > 0:  
            face = 0
            u, v = -z / ax, -y / ax
        else:
            face = 1
            u, v = z / ax, -y / ax
    elif ay >= ax and ay >= az:
        if y > 0:
            face = 2
            u, v = x / ay, z / ay
        else:
            face = 3
            u, v = x / ay, -z / ay
    else:
        if z > 0:
            face = 4
            u, v = x / az, -y / az
        else:
            face = 5
            u, v = -x / az, -y / az

    u = (u + 1) / 2
    v = (v + 1) / 2
    return face, u, v

def cubemap_to_panorama(images, width=1024, height=512):
    faces = []
    for image_idx, image in enumerate(images):
        if image_idx == 2 or image_idx == 3:
            image = image.transpose(Image.Transpose.ROTATE_90)
            if image_idx == 2:
                image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        np_image = np.array(image.convert("RGB"))
        faces.append(np_image)

    face_h, face_w, _ = faces[0].shape
    pano = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        v = (y + 0.5) / height
        phi = (0.5 - v) * math.pi
        for x in range(width):
            u = (x + 0.5) / width
            theta = (u - 0.5) * 2 * math.pi 

            rd = (
                math.cos(phi) * math.cos(theta),
                math.sin(phi),
                math.cos(phi) * math.sin(theta)
            )

            face, fu, fv = direction_to_face_uv(rd)

            ix = min(int(fu * face_w), face_w - 1)
            iy = min(int(fv * face_h), face_h - 1)
            pano[y, x] = faces[face][iy, ix]

    return Image.fromarray(pano)

def get_texture_from_plate(texture, permutation_index=0, is_cubemap=True):
    img = texture
    is_plate, palette = is_color_plate(img)
    if is_plate:
        sequences = extract_colorplate_faces(img, palette)
        sequence_count = len(sequences)
        if is_cubemap:
            image_sets = []
            for sequence_idx, sequence in enumerate(sequences):
                face_0 = sequence[1]
                face_0 = face_0.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                face_0 = face_0.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                face_1 = sequence[3]
                face_2 = sequence[4]
                face_3 = sequence[5]
                face_3 = face_3.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                face_3 = face_3.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                face_4 = sequence[0]
                face_4 = face_4.transpose(Image.Transpose.ROTATE_90)
                face_4 = face_4.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                face_4 = face_4.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                face_5 = sequence[2]
                face_5 = face_5.transpose(Image.Transpose.ROTATE_90)
                faces = [face_0, face_1, face_2, face_3, face_4, face_5]

                if sequence:
                    w, h = face_0.size
                    pano_w = 4 * w
                    pano_h = 2 * h

                    img = cubemap_to_panorama(faces, pano_w, pano_h)
                    image_sets.append([img])

            if sequence_count > 0:
                if sequence_count < permutation_index:
                    img = image_sets[0][0]
                else:
                    img = image_sets[permutation_index][0]

        else:
            if sequence_count > 0:
                if sequence_count < permutation_index:
                    img = sequences[0][0]
                else:
                    img = sequences[permutation_index][0]

    elif is_cubemap:
        faces = extract_t_faces(img)
        if faces:
            w, h = img.size
            pano_w = 4 * w
            pano_h = 2 * h

            img = cubemap_to_panorama(faces, pano_w, pano_h)

    return img.convert('RGBA')
