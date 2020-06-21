from collections import OrderedDict
class modernTable:
    def __repr__(self):
        return str(self.data)
    def __str___(self):
        return 'modernTable'
    def __init__(self,data=None, colMaxLen:list=[]):
        """
        Initialize a table creation. (modern table with utf-8 charactors)
        Optional arg1: data.  type is dict.
        Optional arg2: colMaxLen.  type is list.  Must be passed if you have the dict (arg1) passed.
        """
        self.data = data or OrderedDict()
        self.row = 0
        self.colMaxLen = colMaxLen


    def new_column(self,name):
        class column:
            def __init__(self,obj,name):
                """
                create a new column (initialize)
                arg1: name.  Name of the new column.
                return: column location
                """
                obj.data[name]=list()
                obj.colMaxLen.append(len(name))
                self.name = name
                self.location = len(obj.colMaxLen) -1
                self.obj = obj
            def rename(self,newname):
                """
                rename the column (and move to end)
                arg1: newname.
                return: old name
                """
                oldname = self.name
                rowdata = self.obj.data[self.name]
                del self.obj.data[self.name]
                self.obj.data[newname] = rowdata
                self.name = newname
                self.location = len(self.obj.colMaxLen) -1
                return oldname
            def delete(self):
                """
                delete the column
                no arguments
                """
                del self.obj.data[self.name]
            def moveToEnd(self):
                """
                move a column
                no arguments
                """
                self.obj.data[self.name] = self.obj.data.pop(self.name)
                self.location = len(self.obj.colMaxLen) -1
        return column(self,name)




    def insert(self,*values):
        """
        insert a row.
        arg1: values. The value for the row.
        return: the longest length of columns (list)
        """
        self.row += 1
        loopCount = 0                                                                               # for the index loop of the list
        for column in self.data:                                                                    # column is the key
            self.data[column].append(str(values[loopCount]))
            self.colMaxLen[loopCount] = max(self.colMaxLen[loopCount],len(str(values[loopCount])),len(column))
            loopCount += 1
        return self.colMaxLen




    def get(self):
        """Return back the table in string.  No arguments."""
        result = '╔'                                                # top line
        colNum = 0
        for column in self.data:
            for i in range(self.colMaxLen[colNum]+2):
                result += '═'
            result += '╦'
            colNum += 1
        result = result[:-1]
        result += '╗\n'

        # 2nd line loop
        colNum = 0
        for column in self.data:
            result += f'║ {column} '
            neededSpaces = self.colMaxLen[colNum] - len(column)     # the column string subtract from needed full length
            for i in range(neededSpaces):
                result += ' '
            colNum += 1
        result += '║\n'

        # every row and every top bar
        for rowNum in range(0,self.row):
            result += '╠'
            colNum = 0
            # the top bar
            for column in self.data:
                for i in range(self.colMaxLen[colNum]+2):
                    result += '═'
                result += '╬'
                colNum += 1
            result = result[:-1]
            result += '╣\n'

            # the value
            colNum = 0
            for column in self.data:
                value = self.data[column][rowNum]
                result += f'║ {value}'
                neededSpaces = self.colMaxLen[colNum] - len(value)
                for i in range(neededSpaces+1):
                    result += ' '
                colNum += 1
            result += '║\n'
        
        # finish the bottom of the table
        result += '╚'
        colNum = 0
        for column in self.data:
            for i in range(self.colMaxLen[colNum]+2):
                result += '═'
            result += '╩'
            colNum += 1
        result = result[:-1]
        result += '╝\n'
        return result




    def remove(self,rowNum):
        """
        remove a row
        arg1: rowNum.  (index of a list)
        return: list with all removed values
        """
        result = list()
        for column in self.data:
            result.append(self.data[column].pop(rowNum))
        return result












class classicTable(modernTable):
    def __str__(self):
        return 'classicTable'
    def get(self):
        """Return back the table in string.  No arguments."""
        result = '+'                                                # top line
        colNum = 0
        for column in self.data:
            for i in range(self.colMaxLen[colNum]+2):
                result += '-'
            result += '+'
            colNum += 1
        result = result[:-1]
        result += '+\n'

        # 2nd line loop
        colNum = 0
        for column in self.data:
            result += f'| {column} '
            neededSpaces = self.colMaxLen[colNum] - len(column)     # the column string subtract from needed full length
            for i in range(neededSpaces):
                result += ' '
            colNum += 1
        result += '|\n'

        # every row and every top bar
        for rowNum in range(self.row):
            result += '+'
            colNum = 0
            # the top bar
            for column in self.data:
                for i in range(self.colMaxLen[colNum]+2):
                    result += '-'
                result += '+'
                colNum += 1
            result = result[:-1]
            result += '+\n'

            # the value
            colNum = 0
            for column in self.data:
                value = self.data[column][rowNum]
                result += f'| {value}'
                neededSpaces = self.colMaxLen[colNum] - len(value)
                for i in range(neededSpaces+1):
                    result += ' '
                colNum += 1
            result += '|\n'
        
        # finish the bottom of the table
        result += '+'
        colNum = 0
        for column in self.data:
            for i in range(self.colMaxLen[colNum]+2):
                result += '-'
            result += '+'
            colNum += 1
        result = result[:-1]
        result += '+\n'
        return result


class onelineTable(modernTable):
    def __str__(self):
        return 'onelineTable'
    def get(self):
        """Return back the table in string.  No arguments."""
        result = '┌'                                                # top line
        colNum = 0
        for column in self.data:
            for i in range(self.colMaxLen[colNum]+2):
                result += '─'
            result += '┬'
            colNum += 1
        result = result[:-1]
        result += '┐\n'

        # 2nd line loop
        colNum = 0
        for column in self.data:
            result += f'│ {column} '
            neededSpaces = self.colMaxLen[colNum] - len(column)     # the column string subtract from needed full length
            for i in range(neededSpaces):
                result += ' '
            colNum += 1
        result += '│\n'

        # every row and every top bar
        for rowNum in range(self.row):
            result += '├'
            colNum = 0
            # the top bar
            for column in self.data:
                for i in range(self.colMaxLen[colNum]+2):
                    result += '─'
                result += '┼'
                colNum += 1
            result = result[:-1]
            result += '┤\n'

            # the value
            colNum = 0
            for column in self.data:
                value = self.data[column][rowNum]
                result += f'│ {value}'
                neededSpaces = self.colMaxLen[colNum] - len(value)
                for i in range(neededSpaces+1):
                    result += ' '
                colNum += 1
            result += '│\n'
        
        # finish the bottom of the table
        result += '└'
        colNum = 0
        for column in self.data:
            for i in range(self.colMaxLen[colNum]+2):
                result += '─'
            result += '┴'
            colNum += 1
        result = result[:-1]
        result += '┘\n'
        return result