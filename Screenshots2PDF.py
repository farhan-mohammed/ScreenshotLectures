import img2pdf
import sys
import os

if (len(sys.argv) != 2):
    print('Invalid number of Arguments')
    sys.exit()

directoryPath = sys.argv[1]
if (not os.path.exists(directoryPath)):
    print('Invalid Directory')
    sys.exit()

if directoryPath[-1] != '/':
    directoryPath += '/'
imagesList = [directoryPath +
              o for o in os.listdir(directoryPath) if o[-4:] == '.jpg']
if len(imagesList) == 0:
    print('No JPG images found in directory')
    sys.exit()

# Save as pdf
with open(directoryPath[:-1]+".pdf", "wb") as f:
    f.write(img2pdf.convert(imagesList))
