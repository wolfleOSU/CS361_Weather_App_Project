
class saveData:
    def __init__(self, filename):
        self.filename = filename
        try:
            f = open(self.filename, "x")
            f.close()
        except:
            pass
            

    def saveLocation(self, location):
        f = open(self.filename, "r+")
        if location in f.read():
            return None
        f.write(location + "\n")
        f.close()

    def readSavedLocations(self):
        f = open(self.filename, "r")
        print(f.read())
        f.close()


test = saveData("savedLocations.txt")
test.saveLocation("Corvallis")
test.readSavedLocations()
