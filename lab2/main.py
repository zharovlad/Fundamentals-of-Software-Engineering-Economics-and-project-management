# в вводном файле хранится список рёбер (работ) в виде: A B T
# A - предшествующее событие 
# B - последующее событие
# T - продолжительность работы

from math import inf

input_file_name = 'C:\\Users\\Влад\\Desktop\\7 semester\\Fundamentals-of-Software-Engineering-Economics-and-project-management-1\\lab2\\input.txt'

output_file_name = 'C:\\Users\\Влад\\Desktop\\7 semester\\Fundamentals-of-Software-Engineering-Economics-and-project-management-1\\lab2\\output.txt'


class App:
    def __init__(self):
        self.jobs = []      # работы (дуги)
        self.start = []     # начальные события
        self.finish = []    # конечные события
        self.reading()
        self.get_rid_of_cycles()
        self.detect_start()
        self.detect_finish()      

    
    def reading(self):
        """ Чтение данных из входного файла """
        with open(input_file_name, 'r') as r:
            for line in r:
                _line = line.split()
                _line = [int(element) for element in _line]
                self.check_job(Job(_line))
                

    def check_job(self, new_job):
        """ Проверка работ (вершин) на дубляж """
        for job in self.jobs:
            if new_job.start == job.start:
                if new_job.finish == job.finish:
                    if new_job.time != job.time:
                        time = inf
                        while time != new_job.time and time != job.time:
                            print('Ошибка. Работа: ' + str(job.start) + ' - ' + str(job.finish) + ' дублируется, но имеет два веса: ' + str(new_job.time) + ' и ' + str(job.time) + '. Выбрать нужное')
                            try:
                                time = int(input())
                            except:
                                time = inf
                        job.time = time
                        return
        
        self.jobs.append(new_job)


    def get_rid_of_cycles(self): 
        """ Сразу же избавимся от циклов """
        vertexes = {}
        for job in self.jobs:
            vertexes[job.start] = 'white'
            vertexes[job.finish] = 'white'
        
        for job in self.jobs:
            if vertexes[job.start] == 'white':
                self.find_cycles(job.start, vertexes)

    
    def find_cycles(self, start_vertex, vertexes):
        """ Ищем циклы """
        vertexes[start_vertex] = 'grey'
        for job in self.jobs:
            if start_vertex == job.start:
                if vertexes[job.finish] == 'white':
                    self.find_cycles(job.finish, vertexes)
                if vertexes[job.finish] == 'grey':
                    self.detect_cycle(vertexes)
        vertexes[start_vertex] = 'black'

    
    def detect_cycle(self, vertexes):
        """ Печать информационного сообщения в консоль """
        print('Обнаружен цикл. Измените входные данные и запустите программу снова. \n')
        for vertex in vertexes:
            if vertex == 'grey':
                print(str(vertex.key), end=' ')
        exit(1)

    
    def detect_start(self):
        """ Определить начальные события """
        for job in self.jobs:
            if not (job.start in self.start):
                self.start.append(job.start)
        for job in self.jobs:
            try:
                self.start.remove(job.finish)
            except:
                pass
    

    def detect_finish(self):
        """ Определить конечные события """
        for job in self.jobs:
            if not (job.finish in self.finish):
                self.finish.append(job.finish)
        for job in self.jobs:
            try:
                self.finish.remove(job.start)
            except:
                pass
    

class Job:
    def __init__(self, ABT):
        self.start = ABT[0]
        self.finish = ABT[1]
        self.time = ABT[2]


def define_start(start):
    """ Сделать одно начальное событие """

    # информативные сообщения

    mess_several_starts = 'Несколько начальных событий. \n \
        1 - Удаление одного из событий \n \
        2 - Добавить фиктивную вершину \n'

    while len(start) != 1:
        print(mess_several_starts)
        if response_user(1, 2) == 1:
            pass # удаление одного из событий
        else:
            pass # добавление вершины
    
    return start[0]
        

def response_user(start, finish):
    """ Повторять, пока не получим нужный ответ от пользователя """    
    incorrect_answer = 'Введите корректный ответ\n'
    response = 0
    while response < start or response > finish:
        try:
            response = int(input())
        except ValueError:
            print(incorrect_answer)
    return response

App()
    