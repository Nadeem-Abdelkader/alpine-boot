def read_txt_to_lst(filename):
    mylines = []
    # of = open(filename, 'rt')
    # s = of.readlines()
    # print(s)
    with open(filename, 'rt') as myfile:
        for myline in myfile:
            # print(myline)
            if myline.startswith("KEYMAPOPTS") or myline.startswith("HOSTNAMEOPTS") or myline.startswith(
                    "INTERFACESOPTS") or \
                    myline.startswith("DNSOPTS") or myline.startswith("TIMEZONEOPTS") or myline.startswith("PROXYOPTS") \
                    or myline.startswith("APKREPOSOPTS") or myline.startswith("SSHDOPTS") or \
                    myline.startswith("NTPOPTS") or myline.startswith("DISKOPTS") or \
                    myline.startswith("LBUOPTS") or \
                    myline.startswith("APKCACHEOPTS"):
                start = myline.find("\"")
                end = myline.rfind("\"")
                # print(myline[start+1:end])
                if myline[start + 1:end].startswith("-"):
                    mylines.append(myline[start + 4:end])
                else:
                    mylines.append(myline[start + 1:end])
    return mylines


# print(read_txt_to_lst("answers.txt"))
