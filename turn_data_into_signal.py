import numpy as np
import struct

def data_into_signal(datafile, calibrationfile, nparray=False):

    def return_data(filename):
        if filename == "no_file":
            print("\n- file not given -\n")
            return []

        print(f"decoding file {filename}...")

        with open(filename, "rb") as file:
            raw_data = file.read()
            data = []

            first_index = 0
            last_index = 8
            length = len(raw_data)
            print(f"number of bytes to be decoded: {length}")
            if length % 8 != 0: print(f"!!ATTENTION!! length not multiple of 8")
            for i in range(length//8):
                if i % 1000000 == 0:
                    print(f"decoding byte no. {(i*8)//1000000} / {length//1000000}... (in millions)")
                data.append(struct.unpack("d", raw_data[first_index:last_index]))
                first_index += 8
                last_index += 8

        return data

    dataarray = return_data(datafile)
    calibration = return_data(calibrationfile)

    if nparray:
        dataarray, calibration = np.array(dataarray), np.array(calibration)

    return dataarray, calibration
