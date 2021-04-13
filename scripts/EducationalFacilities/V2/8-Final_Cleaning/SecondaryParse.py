import csv

#note this was written in Python 2

inputFile = '../6-CSD_And_Clean/output/ODEFv2_ValidationFile_31-03-2021.csv'
outputFile = 'parseTestOut.csv'

suffixes = ['street','st','avenue','ave','road','rd','drive','dr','boulevard','av','boul','on','route','blvd','bc','place','lane','highway','mall', 'hwy','way','square','park','rte','trail','crescent','cres','port','rang','line','parkway']
invalidChars = ['e', 'w', 'n', 's', '&']

def is_number(s):
    try:
        float(s)
        return True 
    except ValueError:          return False

def charCount(s):
    count = 0
    for i, x in enumerate(s):
        if not is_number(x):    count += 1
    return count

def numCount(s):
    count = 0
    for i, x in enumerate(s):
        if is_number(x):        count += 1
    return count

def getFirstChar(s):
    for i, x in enumerate(s):
        if not is_number (x):   return x

def getUnit(s):
    group = s.split(" ")
    found = False
    for g in group:
        if found:      return g
        if g =="unit": found = True

unitCount = 0

def quickAddressParse(row):
    global unitCount
    addr =  row['address_str']
    index = row["idx"]
    if addr != "" and not isinstance(addr, float):
        pos = 0 #Check if text before civic number and remove to get rid of business titles
        for i, x in enumerate(addr):
            if is_number(x):
                pos = i
                break
        if pos>0:   addr = addr[pos:]
        addr = addr.replace(" a ", " ")
        row['trimmed'] = addr

        group = addr.split(" ")

        if len(group[0].split("-")) == 2: #If the first word is a set of two joined by a hyphen
            g = group[0].split("-")
            row["unit_2"], row["street_no_2"] = g[0], g[1]
            unitCount +=1
        elif len(group) >= 3 and is_number(group[0]) and is_number(group[1]) and group[2] not in suffixes: #If the first two words are numbers and the third isn't a street suffix
            row["unit_2"], row["street_no_2"] = group[0], group[1]
            unitCount +=1
        elif charCount(group[0]) ==1 and numCount(group[0]) >= 1: #if the first word is mostly numbers with only one character
            unit = getFirstChar(group[0])
            row["unit_2"], row["street_no_2"] = unit, group[0].replace(unit, "")
            unitCount +=1
        elif len(group) >= 2 and is_number(group[0]) and len(group[1]) == 1 and charCount(group[1]) == 1 and group[1] not in invalidChars: #If it's a number followed by a singe non-directional character
            row["unit_2"], row["street_no_2"] = group[1], group[0]
            unitCount +=1
        elif "unit " in addr: #If they've just straight up put the unit number in there somewhere
            row["unit_2"] = getUnit(addr)
            unitCount +=1


def main():
    global unitCount
    arr = []
    input_file = csv.DictReader(open(inputFile))

    first, keys = True, ""
    for row in input_file:
        quickAddressParse(row)
        arr.append(row)
        if first:
            first, keys = False, row.keys()
    print(unitCount)

    with open(outputFile, 'wb') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(arr)
        f.close()

if __name__ == '__main__':
    main()