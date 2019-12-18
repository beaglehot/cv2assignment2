import numpy as np
import cv2 as cv
import random as rng
import os
import pandas as pd

# parameters
image_folder_path = 'Video/img1/'

def parseTracks(tracks):
    frame_n = []
    id = []
    minx = []
    miny = []
    maxx = []
    maxy = []
    for t in tracks:
        for bbox in t['bboxs']:
            #frame, id, minx, miny, maxx, maxy
            frame_n.append(bbox['frame'])
            id.append(tracks.index(t))
            minx.append(bbox['left'])
            miny.append(bbox['top'])
            maxx.append(bbox['left'] + bbox['width'])
            maxy.append(bbox['top'] + bbox['height'])
    d = {'frame': frame_n, 'id': id, 'minx': minx, 'miny': miny, 'maxx': maxx, 'maxy': maxy}
    df = pd.DataFrame(data=d)
    return df

def getRectByFrameAndParsedTracks(frame_index, parsedTracks):
    return parsedTracks.loc[parsedTracks['frame'] == frame_index]


def showTracksOnImage(parsedTracks):
    # generate color for each id
    ids = parsedTracks.id.unique()
    colors = {}
    for i in ids:
        colors[i] = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))

    image_paths = []
    frameIndex = 1
    for file in os.listdir(image_folder_path):
        image_paths.append((frameIndex, image_folder_path + file))
        frameIndex += 1

    for frame_i, frame_path in image_paths:
        frame = cv.imread(frame_path)
        if frame is None:
            print('Could not open or find the image: ' + frame_path)
            exit(0)
        rows = getRectByFrameAndParsedTracks(frame_i, parsedTracks)
        for index, row in rows.iterrows():
            src = cv.rectangle(frame, (int(row['minx']), int(row['miny'])), (int(row['maxx']), int(row['maxy'])), colors[int(row['id'])], 2)

        cv.imshow('frame', frame)
        cv.waitKey(10)

if __name__ == '__main__':
    showTracksOnImage(None, None)