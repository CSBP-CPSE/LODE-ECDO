import urllib


def download():
    for i in range(1, 285):
        addy = 'https://www.museums.ca/site/aboutthecma/services/canadianmuseumdirectory?page=' + str(i)
        fname = 'p' + str(i) + '.txt'
        urllib.urlretrieve (addy, fname)

def parse():
    inEntry = False
    entryCount = 0
    order = "Title, Address, Phone No., Category"
    OP = open("directory.csv","w")
    OP.write(str(order))
    OP.write("\n")

    for x in range(1, 285):
        f = "p" + str(x) + ".txt"
        with open (f, "r") as myfile:

            for line in myfile:
                if "<h4>" in line:
                    inEntry = True
                    newLine = line.replace(",", " ")
                    entryCount = 0
                if inEntry and "<p>" in line and not "<strong> Notes/Details </strong>" in line:
                    entryCount += 1
                    if "<br>" not in line:  newLine += "," + line.replace(",", "-")
                    else:   newLine += "," + line.replace(",", " ").replace("<br>", " ")
                    if "<p>Category :" in line:
                        inEntry = False
                        newLine = newLine.replace("\n", "").replace("<p>", "").replace("</p>", "").replace("<h4>", "").replace("</h4>", "").replace("Category : ", "").replace("  ", " ").replace("- ", "-")
                        newLine += "\n"
                        OP.write(newLine)
    OP.close()

def main():
    #download()
    #parse()

if __name__ == '__main__':
    main()
