import zipfile
zFile = zipfile.ZipFile("./test.zip");
zFile.extractall("./",pwd="123");