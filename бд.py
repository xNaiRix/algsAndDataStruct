#бд Студентэ
#возможность созранения в файл и извлечения из файла
#Student:
#Фио
#age
#group
#id -> grates
#id - params
#params: title - value
#grates: id->grates по каждому предмету
#функционал: добавление, поиск, удаление, изменение, сохранение и извлечене из txt
class Student:
    def __init__(self, name = None, Mname = None, SerName = None, age = None, group = None, id = None):
        self.name = name
        self.Mname = Mname
        self.SerName = SerName
        self.age = age
        self.group = group
        self.params = {}#название параметра -> значение параметра
        self.id = id
        self.grates = {}#предмет->оценки (лист)
    def setName(self, name):
        self.name = name
    def setMname(self, Mname):
        self.Mname = Mname
    def setSerName(self, SerName):
        self.SerName = SerName
    def setAge(self, age):
        self.age = age
    def setGroup(self, group):
        self.group = group
    def addParam(self, parTitle, parValue):
        self.params[parTitle] = parValue
    def delParam(self, parTitle):
        self.params.pop(parTitle)
    def __eq__(self, other):
        return self.id == other.id
    def addMark(self, subject, mark):
        if subject not in self.grates:
            self.grates[subject] = [mark]
            return  
        self.grates[subject] += [mark]
    def getImperStr(self):
        return [str(self.id), str(self.name), str(self.Mname), str(self.SerName), str(self.age), str(self.group)] 
    def getParamsStr(self):
        return[str(title) + '|' + str(value) for title,value in self.params.items()]#предполагаем, что в value лежат строки
    def getGratesStr(self):
        return [str(title) + '|' + '|'.join(str(n) for n in value) for title,value in self.grates.items()]
class BD:#всё - строки
    def __init__(self):
        self.students = {}#храним по id
        #храним по ФИО (списки людей)
        self.names = {}
        self.Mnames = {}
        self.SerNames = {}
        self.ages = {}#храним по возрасту (set(людей))
        self.groups = {}#храним списки по группам
        self.params = {}#название параметра -> {cловарь: значение параметра - список id}
        self.grates = {}#id->marks
        self.cur_cnt = 0
    def find_with_one_parametr(self, param, value):
        if param == "name":
            return self.names[value]
        if param == "Mname":
            return self.Mnames[value]
        if param == "SerName":
            return self.SerNames[value]
        if param == "age":
            return self.ages[value]
        if param == "group":
            return self.groups[value]
        if param not in self.params:
            return set()
        return self.params[param][value]
    def find(self, params):#params: название параметра (передается строкой) -> значение параметра
        if len(params) <= 0 or len(params[0]) != 2:
            raise IndexError
        results = self.find_with_one_parametr(params[0][0],params[0][1]) #храним список подходящих студентов
        for i in range(1, len(params)):
            results&=self.find_with_one_parametr(params[i][0],params[i][1])
        return results#веозвращается множество всех студентов, подходящих по параметрам (множество их id)
    def add(self, student):
        student.id = str(self.cur_cnt)
        self.students[student.id] = student
        self.cur_cnt += 1
        if student.name not in self.names:
            self.names[student.name] = {student.id}
        else:
            self.names[student.name]|= {student.id}
        if student.Mname not in self.Mnames:
            self.Mnames[student.Mname] = {student.id}
        else:
            self.Mnames[student.Mname]|= {student.id}
        if student.SerName not in self.SerNames:
            self.SerNames[student.SerName] = {student.id}
        else:
            self.SerNames[student.SerName]|= {student.id}
        if student.age not in self.ages:
            self.ages[student.age] = {student.id}
        else:
            self.ages[student.age]|= {student.id}
        if student.group not in self.groups:
            self.groups[student.group] = {student.id}
        else:
            self.groups[student.group]|= {student.id}
        for i in student.params:
            if i[0] not in self.params:
                self.params[i[0]] = {i[1] : student.id}     
            elif i[1] not in self.params[i[0]]:
                self.params[i[0]][i[1]] = {student.id}
            else:
                self.params[i[0]][i[1]] |={student.id}
        self.grates[student.id] = student.grates
    def remove(self, id):
        student = self.students[id]
        self.students.pop(id)
        self.names[student.name].discard(id)
        if len(self.names[student.name]) == 0:
            self.names.pop(student.name)
        self.Mnames[student.Mname].discard(id)
        if len(self.Mnames[student.Mname]) == 0:
            self.Mnames.pop(student.Mname)
        self.SerNames[student.SerName].discard(id)
        if len(self.SerNames[student.SerName]) == 0:
            self.SerNames.pop(student.SerName)
        self.ages[student.age].discard(id)
        if len(self.ages[student.age]) == 0:
            self.ages.pop(student.age)
        self.groups[student.group].discard(id)
        if len(self.groups[student.group]) == 0:
            self.groups.pop(student.group)
        for i in student.params:
            self.params[i].discard(id)
            if len(self.params[i]) == 0:
                self.params.pop(i)
        self.grates.pop(id)
    def saveInFile(self, file_name):    
        file = open(file_name, "w")
        file.write("Students\n")
        for id, student in self.students.items():
            file.write('|'.join(student.getImperStr()) + '\n')
        file.write("Parametrs\n")
        for id, student in self.students.items():
            file.write(str(id) + '|' + '|'.join(student.getParamsStr()) + '\n')
        file.write("Grates\n")
        for id, student in self.students.items():############################
            file.write(str(id) + '|' + '|'.join(student.getGratesStr()) + '\n')
        file.write("Counter\n" + str(self.cur_cnt) + "\nEND")
        file.close()
    def getFromFile(self, file_name):
        file = open(file_name, "r")
        cur_line = file.readline().rstrip('\n')
        title = cur_line
        while cur_line != "END":
            #print(cur_line, end='')
            cur_line = file.readline().rstrip('\n')
            if cur_line in ['Students', "Parametrs", "Grates", "Counter"]:
                title = cur_line
                continue
            if "Students" == title and cur_line != title and cur_line != '':
                student_list = list(map(str, cur_line.split('|')))
                self.add(Student(id=student_list[0], name=student_list[1], Mname=student_list[2], SerName=student_list[3], age=student_list[4], group=student_list[5]))
                continue
            if "Parametrs" == title and cur_line != title and cur_line != '':
                params_list = list(map(str, cur_line.split('|')))
                self.addParams(params_list[0], params_list[1:])
                continue
            if "Grates" == title and cur_line != title and cur_line != '':###############ПОФИКСИТЬ
                grates_list = list(map(str, cur_line.split('|')))#id|subject1 mark1 mark2|subject2 mark1 mark2 ...
                if len(grates_list) <= 1:
                    continue
                cur_subject = ''
                for i in range(1, len(grates_list)):
                    if not grates_list[i].isdigit():
                        cur_subject = grates_list[i]
                        continue
                    self.addGrate(id=grates_list[0],subject=cur_subject,mark=grates_list[i])
            if "Counter" == title and cur_line != title and cur_line != '':
                self.cur_cnt = int(cur_line)
                title = "END"
        file.close()
    def addParams(self, id, params):
        if id not in self.students:
            raise IndexError
        self.students[id].addParam(params[0], params[1])
        if params[0] not in self.params:
            self.params[params[0]] = {params[1] : {id}}
        elif params[1] not in self.params[params[0]]:
            self.params[params[0]][params[1]] = {id}
        else:
            self.params[params[0]][params[1]] |= {id}
    def addGrate(self, id, subject, mark):
        if id not in self.students:
            raise IndexError
        self.students[id].addMark(subject, mark)#??
        '''if subject not in self.grates[id]:
            self.grates[id][subject] = [mark]
        else:
            self.grates[id][subject] += [mark]'''

a = BD()
a.add(Student(name = "Ирина", Mname="Тимофеевна",SerName='Глубокая',age='16',group='ИОП-ИТ-24/2'))
a.add(Student(name = "Глеб", Mname="Не знаю",SerName='Синявский',age='16',group='ИОП-ИТ-24/1'))
a.add(Student(name = "Дарья", Mname="Владимировна",SerName='Силова',age='16',group='ИОП-ИТ-24/2'))
a.addParams(id = '2', params =["сон", "0 часов"])
a.addGrate(id = '2', subject="math", mark="5")
a.addGrate(id = '2', subject="литература", mark="5")
a.addGrate(id = '2', subject="math", mark="4")
a.addParams(id='1',params =["сон", "1 час"])
a.addParams(id = '0', params =["сон", "0 часов"])
print(a.find(params=[["age", "16"], ["group", "ИОП-ИТ-24/2"]]))
f = "C:\\Users\\Пользователь\\OneDrive\\Рабочий стол\\Sirius\\Informatics\\1sem\\testWrite.txt"
f2 = "C:\\Users\\Пользователь\\OneDrive\\Рабочий стол\\Sirius\\Informatics\\1sem\\testGet.txt"
#a.saveInFile(f2)
a.getFromFile(f2)
a.add(Student(name="Екатерина", Mname="Не знаю", age="15"))
a.saveInFile(f)