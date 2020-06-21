def gettable():
	import table
	plan = table.modernTable()
	c1 = plan.new_column("original")
	c1.rename("before")
	c2 = plan.new_column("after")
	plan.insert('general in general','general in general')
	plan.insert('polls in polls','polls in polls')
