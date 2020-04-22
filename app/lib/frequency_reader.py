def read_frequency(line, input_string):

    freq_splitted = line.split("\t")
    freq = freq_splitted[1].replace(input_string, '')
    freq = freq.replace(';', '')
    freq = str(float(freq))

    return freq
