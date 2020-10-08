import sys
sys.path.append('C:\\Users\\Влад\\Desktop\\7 semester\\Fundamentals-of-Software-Engineering-Economics-and-project-management-1\\lab3')
import lab3

class Gantt(lab3.NewApp):
    
    def __init__(self):
        lab3.NewApp.__init__(self)
        self.lenght_crit_way = 0
        self.input_file_name = 'C:\\Users\\Влад\\Desktop\\7 semester\\Fundamentals-of-Software-Engineering-Economics-and-project-management-1\\lab4\\input.txt'

        self.output_file_name = 'C:\\Users\\Влад\\Desktop\\7 semester\\Fundamentals-of-Software-Engineering-Economics-and-project-management-1\\lab4\\output.txt'
    
    def print_gantt_chart(self):
        """ Печатает диаграмму Ганта """
        self.print_line_gantt_chart()
        keys = self.early_time.keys()
       
        for key in keys:
            for job in self.jobs:
                if key == job.start and job.time != 0:
                    self.print_job_gantt_chart(key, job)
        self.print_message_in_out_file('\n')
            
    
    def print_line_gantt_chart(self):
        """ Печатает линейку """
        self.lenght_crit_way = self.early_time[self.finish]
        with open(self.output_file_name, 'a') as w:
            w.write('\n%20s' % ('Работы 0'))
            for i in range(1, self.lenght_crit_way + 1):
                if i % 5 == 0:
                    w.write('%3s' % (str(i)))
                else:
                    w.write(' \' ')

    def print_job_gantt_chart(self, key, job):
        """ Печатает строку графика Гантта """
        with open(self.output_file_name, 'a') as w:
            w.write('\n%20s' % ('[' + str(job.start) + ' - ' + str(job.finish) + ']'))
            for i in range(self.lenght_crit_way):
                if i >= self.early_time[key] and i < self.early_time[key] + job.time:
                    w.write(' * ')
                else:
                    w.write(' \' ')

    def sort_by_early(self):
        """ Проводит сортировку по ранним срокам свершения событий """
        items = list(self.early_time.items())
        items.sort(key=lambda x: x[1])
        self.early_time = dict(items)
        keys = self.early_time.keys()
        old = self.jobs
        new = []
        for key in keys:
            for job in old:
                if key == job.start:
                    new.append(job)
        self.jobs = new
                
    def dialog(self):
        """ Режим диалога """
        number = -1
        while True:
            print('0 - выйти')
            print('1 - добавить работу')
            print('2 - удалить работу')
            print('3 - изменить вес')
            number = int(input())

            if number == 0:
                return    
            elif number == 1:
                self.add()
            elif number == 2:
                self.delete()
            else:
                self.change()

            self.get_rid_of_cycles()
            self.detect_start()
            self.define_start()
            self.detect_finish()
            self.define_finish()

            self.early()
            self.sort_by_early()
            self.print_gantt_chart()
        

    def add(self):
        """ Добавим работу """
        print('Введите A, B, T')
        inp = input()
        inp = inp.split()
        inp = [int(i) for i in inp]
        self.jobs.append(lab3.NewJob(inp))

    def change(self):
        """ Изменим время """
        while True:
            print('Введите A, B, T')
            inp = input()
            inp = inp.split()
            inp = [int(i) for i in inp]
            if inp[2] < 1:
                continue
            for job in self.jobs:
                if job.start == inp[0] and job.finish == inp[1]:
                    job.time = inp[2]
                    return

    def delete(self):
        """ Удалим работу """
        while True:
            print('Введите A, B')
            inp = input()
            inp = inp.split()
            inp = [int(i) for i in inp]
            for job in self.jobs:
                if job.start == inp[0] and job.finish == inp[1]:
                    self.jobs.remove(job)
                    return
        


if __name__ == "__main__":
    lab = Gantt()
    lab.reading()
    
    lab.get_rid_of_cycles()
    lab.detect_start()
    lab.define_start()
    lab.detect_finish()
    lab.define_finish()

    lab.print_message_in_out_file('Исходный список работ сетевого графика\n', True)
    lab.print_message_in_out_file('%10s%10s%10s\n' % ('A', 'B', 't'))
    lab.print_jobs()

    lab.early()
    lab.sort_by_early()
    lab.print_message_in_out_file('\nУпорядоченный список работ сетевого графика\n')
    lab.print_message_in_out_file('%10s%10s%10s\n' % ('A', 'B', 't'))
    lab.print_jobs()


    lab.print_gantt_chart()
    lab.dialog()
