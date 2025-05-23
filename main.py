from orm import Table, execute_query

employees = Table('employees', [('id', int), ('name', str), ('age', int), ('salary', int)])

print(employees)
execute_query("ASOSIY(QO'SH(employees, ('name'='Said', 'age'=18, 'salary'=1000)))")
