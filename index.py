# Open CV for looping through frames
import cv2
# os for working with directories
import os
# sys for looking at command line arguments
import sys
# datetime for converting images to time in video
import datetime
# numpy for calculating MSE between two images
import numpy as np
# tqdm for printing a progress bar
from tqdm import tqdm


def mse(imageA, imageB):
    # Comparing the images gives us an error, use the mse as a trigger to save the image.
    # https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/

    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    y, x, z = imageA.shape
    x = int(x*0.835)
    # y = y*0.8
    # I had an issue where the speaker on the zoom video flicked a lot, causing the repetition of frames. To tackle this, I only take the MSE of the cropped image, which should ignore the zoom video.
    # image[0:y,0:x] is the inital size
    imageA = imageA[:, 0:x]
    imageB = imageB[:, :x]
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    # return the MSE, the lower the error, the more "similar" the two images are
    return err


def testRun(vidcap, frames_folder, success, image):
    # Logsitics
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    totalNoFrames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    durationInSeconds = float(totalNoFrames) / float(fps)
    print('----Logistics----')
    print("FPS:", fps)
    print("Total Frames:", int(totalNoFrames))
    print("Length of Video", str(datetime.timedelta(seconds=durationInSeconds)))
    print('---Doing a Dry run for Treshold----')
    totalError = []
    count = 0
    prev = None
    # analyzes every frame at 2s.
    for fno in range(0, totalNoFrames, fps*5):
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, fno)
        _, image = vidcap.read()
        if not prev is None:
            s = mse(image, prev)
            # print(f"{t} Image error: {s}")
            totalError.append(s)
        prev = image
    # 1991.726805678645
    totalError = np.array(totalError)
    treshold = 2 * np.std(totalError)
    print('Using Predicted Treshold:', treshold)
    print('-----End of Testing----')
    return treshold


def analyzeFrame(image, slideNo, threshold, frames_folder, timestamp, prev=None):
    if not prev is None:
        if mse(image, prev) > threshold:
            slideNo += 1
            # save frame as JPEG file
            cv2.imwrite(
                "%s/frame%d_timestamp-%s.jpg" % (frames_folder, slideNo, timestamp), prev)

    return image, slideNo


def grabFrames(vidcap, frames_folder, success, image, threshold=400):
    # Logsitics
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    totalNoFrames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    loop = tqdm(position=0, total=totalNoFrames, leave=False)
    count = 0
    prev = None
    t = 0

    # analyzes every frame at 2s.
    factor = 2
    for fno in range(0, totalNoFrames, fps*factor):
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, fno)
        _, image = vidcap.read()
        if not prev is None:
            loop.update(fps*factor)
            prev, t = analyzeFrame(image, t, threshold, frames_folder, str(
                datetime.timedelta(seconds=fno//fps)), prev)
            s = mse(image, prev)
        prev = image

    t += 1
    cv2.imwrite(
        "%s/frame%d_timestamp-%s.jpg" % (frames_folder, t, str(datetime.timedelta(seconds=count//fps))), prev)

    # new approach
    # total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


def main():
    if (len(sys.argv) != 2):
        print('Invalid number of Arguments')
        sys.exit()

    video_file_path = sys.argv[1]

    if not os.path.isfile(video_file_path):
        print('Video Path is incorrect')
        sys.exit()
    # Not sure if OpenCV is compatible with other types of videos
    elif video_file_path[-4:] != '.mp4':
        print("Video must be an mp4 file")
        sys.exit()

    vidcap = cv2.VideoCapture(video_file_path)
    # Try Reading the video
    success, image = vidcap.read()
    if not success:
        print("Error related to OpenCV capturing video")
        sys.exit()
    # Create Frames folder
    frames_folder = video_file_path[:-4] + '_frames'
    if not os.path.exists(frames_folder):
        os.makedirs(frames_folder)
    treshold = testRun(cv2.VideoCapture(video_file_path),
                       frames_folder, success, image)
    grabFrames(cv2.VideoCapture(video_file_path),
               frames_folder, success, image, treshold)
    print('Conversion Completed')


if __name__ == "__main__":
    main()
