#Sowtyy
#1.0.0
#08.10.2023


import os
import os.path
import sys
import piexif
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


DATETIME_STR_FORMAT = "%Y:%m:%d %H:%M:%S"


def setExifDateTime(exifDict : dict, newDateTimeStr : datetime):
  exifDict["0th"][piexif.ImageIFD.DateTime] = newDateTimeStr
  exifDict["Exif"][piexif.ExifIFD.DateTimeOriginal] = newDateTimeStr
  exifDict["Exif"][piexif.ExifIFD.DateTimeDigitized] = newDateTimeStr

  return

def getFileNameDateTime(fileName : str):
  cleanFileName = fileName.rsplit(".", 1)[0]
  cleanFileName = cleanFileName.replace("IMG_", "").replace("PXL_", "")

  if len(cleanFileName) > 15: # if there are milliseconds
    cleanFileName = cleanFileName[:15]

  try:
    return datetime.strptime(cleanFileName, "%Y%m%d_%H%M%S")
  except Exception as e:
    print(f"Error trying to strptime: {cleanFileName}, {repr(e)}.", end = " ")

  return

def main():
  if len(sys.argv) < 2:
    print("Enter directory path.")
    return

  filesDirPath = sys.argv[1]

  print(f"Directory: {filesDirPath}.")

  dirFileNames = os.listdir(filesDirPath)
  dirFileNamesLen = len(dirFileNames)

  for i, fileName in enumerate(dirFileNames):
    filePath = os.path.join(filesDirPath, fileName)

    print(f"File #{i + 1}/{dirFileNamesLen}: {fileName}...", end = " ")

    try:
      fileExifDict = piexif.load(filePath)
    except Exception as e:
      print(f"Error trying to load file EXIF data: {repr(e)}.")
      continue
    
    fileNameDateTime = getFileNameDateTime(fileName)

    if not fileNameDateTime:
      print("Couldn't find datetime in filename.")
      continue

    fileNameDateTimeStr = fileNameDateTime.strftime(DATETIME_STR_FORMAT)

    print(f"datetime found: {fileNameDateTimeStr}.", end = " ")

    setExifDateTime(fileExifDict, fileNameDateTimeStr) # the exif dict should be sent to the function as a reference, no need to redefine it here.

    try:
      piexif.remove(filePath)
    except Exception as e:
      print(f"Error trying to remove existing EXIF data: {repr(e)}.")
      continue

    piexif.insert(piexif.dump(fileExifDict), filePath)

    print("OK.")

  print("Done.")
  return

if __name__ == "__main__":
  main()
