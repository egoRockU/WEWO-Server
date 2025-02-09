def parse_res(data, handle):
    if isinstance(data, str) and handle in data:
        index = data.find(handle) + len(handle)
        return data[index:]
    else:
        print("Cannot parse " + data)