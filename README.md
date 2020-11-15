# ScreenshotLectures

### Under Construction

I just started this repo. I will clean up the read me very soon!

-   Contact me if youre having trouble running this program

Takes a screenshot of every "slide" in the video and saves it in a folder.

Example: My Professor uploads videos of him writing on this tablet but he does not upload his notes. I can run this program that will screenshot the previous page every time a page was changed.

## Bugs

-   Cant have spaces in file name or file directory

## Demo

I ran this script on this Organic Chemistry Tutor Video. The screenshots of this video are in `Test/DetereminantVideo_frames`

## How it works

It's pretty simple. Using OpenCV, I looped through the frames in the video and comapred the current frame to previous frame and if its 'significantly' different I save the frame as an image.

# How to Setup
```bash
$ python3 -m pip install -r requirements.txt
```

For a test run on the Determinants Video

```bash
$ python3 index.py Testing/DeterminantVideo.mp4
```

To generate a pdf of the images

```bash
$ python3 Screenshots2PDF.py Testing/DeterminantVideo_Frames
```

Look at the Testing folder for results.


# How to Run

# Statistics

I haven't run this program on many videos yet but as I do I will try best to estimate how long it takes to convert an X minute video to frames.

### References

-   https://vuamitom.github.io/2019/12/13/fast-iterate-through-video-frames.html
-
