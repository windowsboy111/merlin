from collections import OrderedDict
class invalidSettings(Exception):
    """The settings passed via kwargs from the constructor of the class is invalid"""
    def __init__(self,message,possible=None,reason=""):
        super.__init__(super(str,message))
        self.message = message
        self.possible = possible
        self.reason = reason
    def get_message(self):
        return self.message
    def get_reason(self):
        return self.reason
    def get_possible(self):
        return self.possible
    def __str__(self):
        return self.message
    def __repr__(self):
        return {'error':invalidSettings,'message':self.message,'possible':self.possible,'reason':self.reason}
def dummy_func(var=None):
    return var
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
class customTable:
    def __repr__(self):
        return str(self.data)
    def __str___(self):
        return 'customTable'
    def __init__(self,style:list,data=None, colMaxLen:list=[],**kwargs):
        """\
        Initialize a table creation.\n
        Required arg1: style. type is list. charaters to form table.\n
        Optional arg1: data.  type is dict.\n
        Optional arg2: colMaxLen.  type is list.  Must be passed if you have the dict (arg1) passed.\
        """
        self._init(style,kwargs,data,colMaxLen)
    def _init(self,style:list,kwargs,data=None,colMaxLen:list=[]):
        self.style = style
        self.data = data or OrderedDict()
        self.row = 0
        self.colMaxLen = colMaxLen
        self.settings = {"align": "left","linespacing": 0,"exp":False}
        if kwargs is not None:
            for key,value in kwargs.items():
                self.settings[key] = value or self.settings[key]
    def new_column(self,name):
        class column:
            def __init__(self,table,name):
                """\
                create a new column (initialize)\n
                arg1: name.  Name of the new column.\n
                return: column location\
                """
                table.data[name]=list()
                table.colMaxLen.append(len(name))
                self.name = name
                self.location = len(table.colMaxLen) -1
                self.table = table
            def rename(self,newname):
                """
                rename the column (and move to end)
                arg1: newname.
                return: old name
                """
                oldname = self.name
                rowdata = self.table.data[self.name]
                del self.table.data[self.name]
                self.table.data[newname] = rowdata
                self.name = newname
                self.location = len(self.table.colMaxLen) -1
                if self.table.settings['exp']:
                    return self
                return oldname
            def delete(self):
                """
                delete the column
                no arguments
                """
                del self.table.data[self.name]
                if self.table.settings['exp']:
                    return self
            def moveToEnd(self):
                """
                move a column
                no arguments
                """
                self.table.data[self.name] = self.table.data.pop(self.name)
                self.location = len(self.table.colMaxLen) -1
                if self.table.settings['exp']:
                    return self
            def getTable(self):
                return self.table
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
        if self.settings['exp']:
            return self
    def get(self):
        """Return back the table in string.  No arguments."""
        return self._get()
    def _get_l(self,style12,result,rowNum=-1):
        if self.settings['linespacing'] != 0:
            for i in range(self.settings['linespacing']):
                colNum = 0
                for column in self.data:
                    if rowNum != -1:
                        column = self.data[column][rowNum]
                    result += f'{style12} ' + ' '*self.colMaxLen[colNum] + ' '
                    colNum += 1
                result += style12 + '\n'
                dummy_func(i)
        colNum = 0
        if self.settings['align'] == 'left':
            for column in self.data:
                if rowNum != -1:
                    column = self.data[column][rowNum]
                result += f'{style12} {column} '
                neededSpaces = self.colMaxLen[colNum] - len(column)     # the column string subtract from needed full length
                result += ' '*neededSpaces
                colNum += 1
        elif self.settings['align'] == 'center':
            for column in self.data:
                if rowNum != -1:
                    column = self.data[column][rowNum]
                neededSpaces = self.colMaxLen[colNum] - len(column)
                result += f'{style12} ' + ' '*int(neededSpaces/2) + column + ' '*int(neededSpaces/2) + ' '
                if neededSpaces/2 % 1:
                    result += ' '
                colNum += 1
        elif self.settings['align'] == 'right':
            for column in self.data:
                if rowNum != -1:
                    column = self.data[column][rowNum]
                neededSpaces = self.colMaxLen[colNum] - len(column)
                result += f'{style12} ' + ' '*neededSpaces + f'{column} '
                colNum += 1
        else:
            raise invalidSettings("Invalid align settings passed",['left','right','center'],f"'{self.settings['align']}' is not a valid align setting.")
        result += style12 + '\n'
        if self.settings['linespacing'] != 0:
            for i in range(self.settings['linespacing']):
                colNum = 0
                for column in self.data:
                    if rowNum != -1:
                        column = self.data[column][rowNum]
                    result += f'{style12} ' + ' '*self.colMaxLen[colNum] + ' '
                    colNum += 1
                result += style12 + '\n'
        return result
    def _get(self):
        result = self.style[0]                                                # top line
        colNum = 0
        for column in self.data:
            result += self.style[1]*(self.colMaxLen[colNum]+2)
            result += self.style[3]
            colNum += 1
            dummy_func(column)
        result = result[:-1]
        result += self.style[2] + '\n'
        # 2nd line loop
        result = self._get_l(self.style[12],result)
        # every row and every top bar
        for rowNum in range(0,self.row):
            result += self.style[4]
            colNum = 0
            # the top bar
            for column in self.data:
                result += self.style[5]*(self.colMaxLen[colNum]+2)
                result += self.style[7]
                colNum += 1
            result = result[:-1]
            result += self.style[6] + '\n'
            # the value
            result = self._get_l(self.style[12],result,rowNum)
        # finish the bottom of the table
        result += self.style[8]
        colNum = 0
        for column in self.data:
            result += self.style[9]*(self.colMaxLen[colNum]+2)
            result += self.style[11]
            colNum += 1
        result = result[:-1]
        result += self.style[10] + '\n'
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
        if self.settings['exp']:
            return self
        return result
    def show(self):
        print(self.get())
        if self.settings['exp']:
            return self


class modernTable(customTable):
    def __str___(self):
        return 'modernTable'
    def __init__(self,data=None, colMaxLen:list=[],**kwargs):
        """\
        Initialize a Modern Table creation.\
        """
        self._init(['╔','═','╗','╦','╠','═','╣','╬','╚','═','╝','╩','║'],kwargs,data,colMaxLen)
    def get(self):
        return self._get()


class classicTable(customTable):
    def __str__(self):
        return 'classicTable'
    def __init__(self,data=None,colMaxLen:list=[],**kwargs):
        """\
        Initialize a classic table creation, which is formed with + | and -.\
        """
        self._init(['+','-','+','+','+','-','+','+','+','-','+','+','|'],kwargs,data,colMaxLen)
    def get(self):
        """Return back the table in string.  No arguments."""
        return self._get()


class onelineTable(customTable):
    def __str__(self):
        return 'onelineTable'
    def __init__(self,data=None,colMaxLen:list=[],**kwargs):
        """\
        Initialize a modern table creation, but have one border instead of double borders.\
        """
        self._init(['┌','─','┐','┬','├','─','┤','┼','└','─','┘','┴','│'],kwargs,data,colMaxLen)
    def get(self):
        return self._get()


#####################################################################################################################################################################

lib_info = """\
pyTableMaker by windowsboy111
Check out the repo:    https://github.copm/windowsboy111/pyTableMaker/
Here's the website:    https://windowsboy111.github.io/pyTableMaker/
By using this library, you agree the terms in both the website and README.md
Thanks for choosing this library! Remember to share it too!\
"""

if __name__ == "__main__":
    print(lib_info)