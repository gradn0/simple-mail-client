def heading(str):
    heading = " " + str + " "
    buffer = int((70 - len(heading))/2)
    print("="*buffer + heading + "="*(buffer + len(heading) % 2))

def seperator(str1, str2):
    buffer = int((70 - len(str1)))
    print(str1 + " " + "."*buffer + " " + str2)