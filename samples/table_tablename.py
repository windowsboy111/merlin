def gettable():
	import table
	tablename = table.modernTable()
	colID = tablename.new_column("column1")
	colID2 = tablename.new_column("column with space")
	colID2.rename("this too")
	tablename.insert("a","b")
	tablename.insert("1","2")
	return tablename.get()
	return tablename.get()
