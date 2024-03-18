import os


def split_file(fromfile, todir, chunksize):
    if not os.path.exists(todir):  # if the directory doesn't exist, create it
        os.mkdir(todir)
    else:
        for fname in os.listdir(todir):  # delete any existing files
            os.remove(os.path.join(todir, fname))
    partnum = 0
    with open(fromfile, 'rb') as input_file:  # open the file in binary mode
        while True:
            chunk = input_file.read(chunksize)  # read a chunk of the file
            if not chunk:  # if the chunk is empty, stop reading
                break
            partnum += 1
            filename = os.path.join(todir, ('optimizer_part%01d' % partnum))
            with open(filename, 'wb') as fileobj:  # write the chunk to a new file
                fileobj.write(chunk)
    return partnum

def merge_files(fromdir, tofile):
    files = sorted(os.listdir(fromdir))  # get a list of the chunk files
    with open(tofile, 'wb') as output_file:  # open the output file in binary mode
        for fname in files:
            with open(os.path.join(fromdir, fname), 'rb') as input_file:  # open each chunk file in binary mode
                chunk = input_file.read()  # read the entire chunk
                output_file.write(chunk)  # write the chunk to the output file
