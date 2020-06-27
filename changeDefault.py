class main():
    def main(self, change):
        oldText = open("recon.py", 'r').read().split("\n")
        reconFile = open("recon.py", 'w')
        newText = []
        for line in oldText:
            if line.split(".")[0] != 'parser':
                newText.append(line)
                continue
            arg = line.split("'")[1].strip("-")
            if arg != change:
                newText.append(line)
                continue
            lineSplit = line.split("default=")
            newLine = lineSplit[0]
            value = lineSplit[1].split(",")[0]
            if value == 'True':
                newLine += 'default=False, ' + lineSplit[1].split(",")[1] + ", action='store_true')"
            elif value == 'False':
                newLine += 'default=True, ' + lineSplit[1].split(",")[1] + ", action='store_false')"
            newText.append(newLine)
        for line in newText:
            reconFile.write(line + "\n")