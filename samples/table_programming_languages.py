def gettable():
	import table
	programming_languages = table.modernTable()
	c1 = programming_languages.new_column("id")
	c2 = programming_languages.new_column("name")
	c3 = programming_languages.new_column("description")
	c4 = programming_languages.new_column("example")
	c5 = programming_languages.new_column("note")
	programming_languages.insert("a",'C++','Upgrade of C','std::cout << "Hello, World!\\n";','mid-lvl')
	programming_languages.insert("b","C#","upgrade of C++","<please teach me stupid benz>","")
