def checkFile(file, filename, isPutOrRead):
    acceptedFileTypes = ["png", "jpeg", "jpg", "avif", "webp", "raw", "nef", "cr2", "tiff", "tif", "svg"]

    if not file and not isPutOrRead:
        return {"error": "no file was selected"}, 400

    if "." not in filename:
        return {"error": "file has no extension"}, 400

    split = str(filename).rsplit(".", maxsplit=1)

    if split[0].strip() == "":
        return {"error": "file needs a name"}, 400
    if not split[1].lower() in acceptedFileTypes:
        return {"error": f"file type not accepted. please submit one of the following {acceptedFileTypes}"}, 400
    return None
