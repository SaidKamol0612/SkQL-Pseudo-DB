from orm import Table, execute_query

employees = Table('employees', [('id', int), ('name', str), ('age', int), ('salary', int)])
print(employees)

res = execute_query("ASOSIY(QO'SH(employees, ('name'='Said', 'age'=18, 'salary'=15000)))")
print(res)
res = execute_query("ASOSIY(QO'SH(employees, ('name'='Kamol', 'age'=81, 'salary'=25000)))")
print(res)

res = execute_query("ASOSIY(KO'RSAT(HAMMASI employees)) SHART(QAYERDA(salary KICHIKROQ 30000))")
print(dict(res).get("rows"))

res = execute_query("ASOSIY(YANGILA(employees, ('age'=19))) SHART(QAYERDA(name TENG 'Kamol'))")
print(res)
res = execute_query("ASOSIY(YANGILA(employees, ('salary'=15500))) SHART(QAYERDA(age KICHIKROQ 19))")
print(res)

res = execute_query("ASOSIY(O'CHIR(employees))")
print(res)

res = execute_query("ASOSIY(KO'RSAT(HAMMASI employees))")
print(dict(res).get("rows"))
