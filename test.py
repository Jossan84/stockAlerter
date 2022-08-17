#test.py
#17/08/2022

from importData import importData

class Test(object):
    fileName = 'stocksData.json'
    def __init__(self):
        self.data = None
    def run(self):
        self.TestImportData()
        self.TestDataIsEmpty()
        self.TestDataStructure()
    
    def TestImportData(self):
        try:
            self.data = importData(self.fileName)
        except NameError:
            raise NameError
        
    def TestDataIsEmpty(self):
        assert isinstance(self.data, dict), f"Not valid input data type for file: {self.fileName}"
    
    def TestDataStructure(self):
        for data in self.data['members']:
            assert "name" in data, f"Key name is not in data from file: {self.fileName}"
            assert "tikr" in data, f"Key tikr is not in data from file: {self.fileName}"
            assert "currency" in data, f"Key currency is not in data from file: {self.fileName}"            
            assert "minPE10Years" in data, f"Key minPE10Years is not in data from file: {self.fileName}"
            assert "years" in data, f"Key years is not in data from file: {self.fileName}"
            assert "eps" in data, f"Key eps is not in data from file: {self.fileName}"  