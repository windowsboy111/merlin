class table:
    def __init__(self,data:dict={}, colMaxLen:list=[]):
        """
        Initialize a table creation.
        Optional arg1: data.  type is dict.
        Optional arg2: colMaxLen.  type is list.  Must be passed if you have the dict (arg1) passed.
        """
        self.data = data
        self.row = 0
        self.colMaxLen = colMaxLen
    def add_column(self,name):
        """
        add a column.
        arg1: name.  Name of the new column.
        """
        self.data[name]=list()
        self.colMaxLen.append(len(name))
    def insert(self,*values):
        """
        insert a row.
        arg1: values. The value for the row.
        """
        self.row += 1
        loopCount = 0                                                                               # for the index loop of the list
        for column in self.data:                                                                    # column is the key
            self.data[column].append(str(values[loopCount]))
            self.colMaxLen[loopCount] = max(self.colMaxLen[loopCount],len(str(values[loopCount])),len(column))
            loopCount += 1
    def get(self):
        """Return back the table in string.  No arguments."""
        result = '╔'
        colNum = 0
        for column in self.data:
            for i in range(0,self.colMaxLen[colNum]+2):
                result += '═'
            result += '╦'
            colNum += 1
        result = result[:-1]
        result += '╗\n'


        colNum = 0
        for column in self.data:
            result += f'║ {column} '
            neededSpaces = self.colMaxLen[colNum] - len(column)     # the column string subtract from needed full length
            for i in range(0,neededSpaces):                         # +1 for the rhs space
                result += ' '
            colNum += 1
        result += '║\n'


        for rowNum in range(0,self.row):
            result += '╠'
            colNum = 0
            for column in self.data:
                for i in range(0,self.colMaxLen[colNum]+2):
                    result += '═'
                result += '╬'
                colNum += 1
            result = result[:-1]
            result += '╣\n'
            colNum = 0
            for column in self.data:
                value = self.data[column][rowNum]
                result += f'║ {value}'
                neededSpaces = self.colMaxLen[colNum] - len(value)
                for i in range(0,neededSpaces+1):
                    result += ' '
                colNum += 1
            result += '║\n'
        result += '╚'
        colNum = 0
        for column in self.data:
            for i in range(0,self.colMaxLen[colNum]+2):
                result += '═'
            result += '╩'
            colNum += 1
        result = result[:-1]
        result += '╝\n'
        return result