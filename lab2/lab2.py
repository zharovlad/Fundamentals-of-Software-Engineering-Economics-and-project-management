# в вводном файле хранится список рёбер (работ) в виде: A B T
# A - предшествующее событие 
# B - последующее событие
# T - продолжительность работы

from math import inf
from copy import deepcopy

class App:
    def __init__(self):
        self.jobs = []      # работы (дуги)
        self.start = []     # начальные события (вершины)
        self.finish = []    # конечные события (вершины)
        self.full_ways = [] # список полных путей

        self.input_file_name = 'C:\\Users\\Влад\\Desktop\\7 semester\\Fundamentals-of-Software-Engineering-Economics-and-project-management-1\\lab2\\input.txt'

        self.output_file_name = 'C:\\Users\\Влад\\Desktop\\7 semester\\Fundamentals-of-Software-Engineering-Economics-and-project-management-1\\lab2\\output.txt'

        # индексы фиктивных вершин

        self.fict_start_index = -1000
        self.fict_finish_index = -1001


    def print_message_in_out_file(self, message, clear_file=False):
        """ Печать сообщения в выходной файл output_file_name 
        clear_file - флаг, нужно очищать выходной файл или нет, по умолчанию False """
        if clear_file:
            with open(self.output_file_name, 'w') as w:
                pass
        with open(self.output_file_name, 'a') as w:
            w.write(message)

    def print_ways(self):
        for way in self.full_ways:
            self.print_message_in_out_file(str(way[0]) + '  длина пути = ' + str(way[1]) + '\n')
    
    def print_jobs(self):
        for job in self.jobs:
            self.print_message_in_out_file('%10d%10d%10d\n' % (job.start, job.finish, job.time))
            

    def reading(self):
        """ Чтение данных из входного файла """
        with open(self.input_file_name, 'r') as r:
            for line in r:
                _line = line.split()
                _line = [int(element) for element in _line]
                if _line[0] == _line[1]:
                    print('Ошибка. Дуга ' + str(_line) + ' удалена')
                else:
                    self.check_job(Job(_line))
                

    def check_job(self, new_job):
        """ Проверка работ (вершин) на дубляж """
        for job in self.jobs:
            if new_job.start == job.start:
                if new_job.finish == job.finish:
                    if new_job.time != job.time:
                        # если начальная и конечная вершина одинаковые, а время не дублируется, то просим выбрать пользователя
                        # какое время нужно оставить
                        # если время не дублируется - то переходим к следующей дуге, не добавляя текущую
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
        """ Определить начальные события.
        Событие начальное, если до него не требуется выполнение никаких работ """
        
        self.start = []
        for job in self.jobs:
            if not (job.start in self.start):
                self.start.append(job.start)
        for job in self.jobs:
            try:
                self.start.remove(job.finish)
            except:
                pass
    

    def detect_finish(self):
        """ Определить конечные события.
        Событие конечное, если после него не требуется выпонение никаких работ """
        self.finish = []
        for job in self.jobs:
            if not (job.finish in self.finish):
                self.finish.append(job.finish)
        for job in self.jobs:
            try:
                self.finish.remove(job.start)
            except:
                pass

    
    def define_start(self):
        """ Сделать одно начальное событие """

        # информативные сообщения
        mess_several_starts = 'Несколько начальных событий. \n \
            1 - Удаление одного из событий \n \
            2 - Добавить фиктивную вершину \n'

        while len(self.start) != 1:
            print(mess_several_starts)
            # удаляем событие или делаем фиктивную вершину в соответствии с запросами пользователя
            if response_user(1, 2) == 1:
                self.delete_vertex(self.fict_start_index)
            else:
                self.add_vertex(self.fict_start_index)
        
        self.start = self.start[0]


    def define_finish(self):
        """ Сделать одно начальное событие """

        # информативные сообщения
        mess_several_finishes = 'Несколько конечных событий. \n \
            1 - Удаление одного из событий \n \
            2 - Добавить фиктивную вершину \n'

        while len(self.finish) != 1:
            print(mess_several_finishes)
            # удаляем событие или делаем фиктивную вершину в соответствии с запросами пользователя
            if response_user(1, 2) == 1:
                self.delete_vertex(self.fict_finish_index)
            else:
                self.add_vertex(self.fict_finish_index)
        
        self.finish = self.finish[0]
    

    def add_vertex(self, index):
        """ Добавляет фиктивную вершину, чтобы было одно начальное и одно конечное событие """
        if index == self.fict_start_index:
            self.start = sorted(self.start, reverse=True)
            for each in self.start:
                self.jobs.insert(0, Job([index, each, 0]))
            self.start.clear()
            self.start.append(index)
        else:
            for each in self.finish:
                self.jobs.append(Job([each, index, 0]))
            self.finish.clear()
            self.finish.append(index)

    
    def delete_vertex(self, index):
        """ Удаляет одну из начальных или конечных вершин по выбору пользователя """
        new_list = []
        if index == self.fict_start_index:
            new_list = self.start
        else:
            new_list = self.finish
        ask_message = 'Какую вершину вы хотите удалить? ' + str(new_list)
        error = 'Ошибка, данной вершины нет, повторите ввод ' + str(new_list)

        print(ask_message)
        try:
            del_vertex = int(input())
        except:
            del_vertex = index

        while not del_vertex in new_list:
            print(error)
            try:
                del_vertex = int(input())
            except:
                del_vertex = index
        self.delete_jobs_with_vertex(del_vertex)
    

    def delete_jobs_with_vertex(self, vertex):
        """ Удаляет все дуги с данной вершиной и для полученного графа пересчитывает начальные и конечные вершины """
        i = 0
        while i < len(self.jobs):
            if self.jobs[i].start == vertex or self.jobs[i].finish == vertex:
                self.jobs.pop(i)
            else:
                i += 1
        self.detect_start()
        self.detect_finish()


    def partly_sort(self):
        """ Частичное упорядочивание """
        old_list = self.jobs
        new_list = []
        stack = [self.start]
        while len(stack):
            i = 0
            while i < len(old_list):
                if stack[0] == old_list[i].start:
                    if not old_list[i].finish in stack:
                        stack.append(old_list[i].finish)
                    new_list.append(old_list[i])
                    old_list.pop(i)
                else:
                    i += 1
            stack.pop(0)
        self.jobs = new_list

    
    def find_full_ways(self, i, j, way=[], lenght=0):
        """ Нахождение полных путей в графе """
        way.append(i)
        if i == j:
            self.full_ways.append([deepcopy(way), lenght])
            return
        for job in self.jobs:
            if i == job.start:
                self.find_full_ways(i=job.finish, j=j, way=way, lenght=lenght+job.time)
                way.pop()

        
class Job:
    def __init__(self, ABT):
        self.start = ABT[0]
        self.finish = ABT[1]
        self.time = ABT[2]
       

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


if __name__ == "__main__":
    lab = App()
    
    lab.reading()
    lab.print_message_in_out_file('Входные данные\n',True)
    lab.print_message_in_out_file('%10s%10s%10s\n' % ('A', 'B', 't'))
    lab.print_jobs()

    lab.get_rid_of_cycles()
    lab.detect_start()
    lab.define_start()
    lab.detect_finish()
    lab.define_finish()

    # После того, как сделали одно стартовое и одно конечное событие - частично упорядочим список работ
    lab.partly_sort()
    lab.print_message_in_out_file('\nЧастично упорядочили\n')
    lab.print_message_in_out_file('%10s%10s%10s\n' % ('A', 'B', 't'))

    lab.print_jobs()
    lab.find_full_ways(i=lab.start, j=lab.finish)
    lab.print_message_in_out_file('\nПолные пути\n')
    lab.print_ways()
        