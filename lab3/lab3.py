from copy import deepcopy
from math import inf
import sys
sys.path.append('C:\\Users\\Влад\\Desktop\\7 semester\\Fundamentals-of-Software-Engineering-Economics-and-project-management-1\\lab2')
import lab2

class NewApp(lab2.App):
    
    def __init__(self):
        """ В новом конструкторе к старым полям добавим словари для ранних и поздних сроков совершения событий """
        lab2.App.__init__(self)
        self.vertexes_by_groups = {}
        self.early_time = {}
        self.late_time = {}
        self.inverse_jobs = []
        self.input_file_name = 'C:\\Users\\Влад\\Desktop\\7 semester\\Fundamentals-of-Software-Engineering-Economics-and-project-management-1\\lab3\\input.txt'

        self.output_file_name = 'C:\\Users\\Влад\\Desktop\\7 semester\\Fundamentals-of-Software-Engineering-Economics-and-project-management-1\\lab3\\output.txt'
    
    def reading(self):
        """ Чтение данных из входного файла """
        with open(self.input_file_name, 'r') as r:
            for line in r:
                _line = line.split()
                _line = [int(element) for element in _line]
                if _line[0] == _line[1]:
                    print('Ошибка. Дуга ' + str(_line) + ' удалена')
                else:
                    self.check_job(NewJob(_line))
    
    def by_groups(self):
        """ Определяет какая вершина в каком слое находится """
        self.vertexes_by_groups[self.start] = 0
        queue = [self.start]
        while len(queue):
            now = queue.pop(0)
            for job in self.jobs:
                if now == job.start:
                    queue.append(job.finish)
                    self.vertexes_by_groups[job.finish] = self.vertexes_by_groups[now] + 1


    def early(self):
        """ Определение ранних сроков совершения событий """
        self.by_groups()
        self.early_time[self.start] = 0
        for i in range(1, max(self.vertexes_by_groups.values()) + 1):
            for vertex in self.vertexes_by_groups:
                if self.vertexes_by_groups[vertex] == i:
                    self.define_early(vertex)


    def define_early(self, vertex):
        self.early_time[vertex] = -inf
        for job in self.jobs:
            if job.finish == vertex and self.early_time[vertex] < self.early_time[job.start] + job.time:
                self.early_time[vertex] = self.early_time[job.start] + job.time

        
    def late(self):
        """ Определение поздних сроков совершения событий """
        self.late_time[self.finish] = self.early_time[self.finish]
        for i in range(max(self.vertexes_by_groups.values()) - 1, -1, -1):
            for vertex in self.vertexes_by_groups:
                 if self.vertexes_by_groups[vertex] == i:
                    self.define_late(vertex)


    def define_late(self, vertex):
        self.late_time[vertex] = inf
        for job in self.jobs:
            if job.start == vertex and self.late_time[vertex] > self.late_time[job.finish] - job.time:
                self.late_time[vertex] = self.late_time[job.finish] - job.time


    def print_times_param(self):
        """ Печатает таблицу "Параметры событий СГ" """
        self.print_message_in_out_file('\nПараметры событий СГ\n')
        self.print_message_in_out_file('%10s%10s%10s%10s\n' % ('Событие', 'Ранний', 'Поздний', 'Резерв'))
        items = list(self.early_time.items())
        items.sort(key=lambda x: x[1])
        self.early_time = dict(items)
        list_keys = self.early_time.keys()
        for key in list_keys:
            self.print_message_in_out_file('%10d%10d%10d%10d\n' % (key, self.early_time[key], self.late_time[key],
            self.late_time[key] - self.early_time[key]))


    def print_lenght_crit_way(self):
        """ Определение и печать длины критического пути """
        self.print_message_in_out_file('\nДлина критического пути = %d\n' % (self.early_time[self.finish]))

    
    def params(self):
        """ Определение параметров работ СГ """
        for job in self.jobs:
            job.full = self.late_time[job.finish] - self.early_time[job.start] - job.time
            job.independent = self.early_time[job.finish] - self.late_time[job.start] - job.time


    def print_jobs_param(self):
        """ Печатает таблицу "Параметры работ СГ" """
        self.print_message_in_out_file('\nПараметры работ СГ\n')
        self.print_message_in_out_file('%20s%20s%10s%15s\n' % ('Работа', 'Продолжительность', 'Полный', 'Независимый'))
        for job in self.jobs:
            self.print_message_in_out_file('%20s%20d%10d%15d\n' % ('[' + str(job.start) + ' - ' + str(job.finish) + ']', 
            job.time, job.full, job.independent))

    def print_jobs_crit_ways(self):
        """ Печатает список работ всех критических путей СГ, которые определяются с учетом необходимого и достаточного условия отнесения пути к критическому """
        self.print_message_in_out_file('\nCписок работ всех критических путей СГ\n')
        self.print_message_in_out_file('%20s%20s%10s%15s\n' % ('Работа', 'Продолжительность', 'Полный', 'Независимый'))
        for job in self.jobs:
            if job.full == 0:
                self.print_message_in_out_file('%20s%20d%10d%15d\n' % ('[' + str(job.start) + ' - ' + str(job.finish) + ']', 
                job.time, job.full, job.independent))


class NewJob(lab2.Job):
    def __init__(self, ABT):
        lab2.Job.__init__(self, ABT)
        self.full = 0
        self.independent = 0

if __name__ == "__main__":
    lab = NewApp()
    lab.reading()
    
    lab.get_rid_of_cycles()
    lab.detect_start()
    lab.define_start()
    lab.detect_finish()
    lab.define_finish()
    lab.partly_sort()
    lab.print_message_in_out_file('Исходный список работ сетевого графика\n', True)
    lab.print_message_in_out_file('%10s%10s%10s\n' % ('A', 'B', 't'))
    lab.print_jobs()

    # определим сроки совершения событий
    lab.early()
    lab.late()
    lab.print_times_param()
    lab.print_lenght_crit_way()
    lab.params()
    lab.print_jobs_param()
    lab.print_jobs_crit_ways()
    