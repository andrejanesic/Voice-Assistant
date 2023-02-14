import os
import re

dirPath = "D:\\skills\\Computer Science\\Machine Learning & Big Data\\Machine Learning\\Projects\\Voice-Assistant\\notebooks\\audiorecords"

lastIndex = max([int(re.search(r"(\d+)", f).group(1)) for f in os.listdir(dirPath) if re.search(r"(\d+)", f)])
toRename = [f for f in os.listdir(dirPath) if re.match("Recording", f)]

i = 1
print(f"Renaming {len(toRename)} files: {lastIndex + i}-{lastIndex + len(toRename)}")
for f in toRename:
    oldPath = dirPath + "\\" + f
    newPath = dirPath + f"\\audio{lastIndex + i}.wav"
    os.rename(oldPath, newPath)
    i += 1