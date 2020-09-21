from copy import deepcopy
from math import inf
# в вводном файле хранится платежная матрица и вероятности
# вероятность - первая строка во входном файле
input_file_name = 'C:\\Users\\Влад\\Desktop\\7 semester\\Fundamentals-of-Software-Engineering-Economics-and-project-management-1\\lab1\\input.txt'

output_file_name = 'C:\\Users\\Влад\\Desktop\\7 semester\\Fundamentals-of-Software-Engineering-Economics-and-project-management-1\\lab1\\output.txt'
# коэффициент оптимизма для критерия Гурвица (0 - наиболее оптимистичный сценарий, 1 - наиболее пессимистичный)
optimism_factor = 0.5
zero = 0
one = 1


def reading():
    """ Чтение данных из входного файла """
    with open(input_file_name, 'r') as r:
        probability = r.readline().split()
        probability = [float(i) for i in probability]
        matrix = []
        for line in r:
            _line = line.split()
            matrix.append([int(element) for element in _line])
    return probability, matrix


def print_input_data(probability, matrix):
    """ Печать входных данных в файл """
    with open(output_file_name, 'w') as w:
        None
    print_message('Вероятности: ' + str(probability))
    print_message('Платежная матрица')
    print_matrix(matrix)


def print_matrix(matrix):
    """ Печать матрицы в файл """
    with open(output_file_name, 'a') as w:
        for i in matrix:
            w.write(str(i) + '\n')
        w.write('\n')


def print_list_in_column(_list):
    """ Печать списка в столбик """
    with open(output_file_name, 'a') as w:
        for i in _list:
            w.write(str(i) + '\n') 


def print_message(message):
    """ Печать текста """
    with open(output_file_name, 'a') as w:
        w.write(message + '\n')


def find_solution(matrix, probability):
    """ Определение решения в зависимости от указанных критериев """
    risk = count_risk(matrix)
    print_message('Матрица рисков')
    print_matrix(risk)

    priority = [zero for _ in range(len(matrix))]

    strategy = with_probability(risk, probability)
    print_message('\nКритерий, основанный на известных вероятностях условиях (меньше - лучше)')
    print_list_in_column(strategy)
    recount_priority(priority, define_min(strategy))

    strategy = Wald(matrix)
    print_message('\nКритерий Вальда (больше - лучше)')
    print_list_in_column(strategy)
    recount_priority(priority, define_max(strategy))

    strategy = Savage(risk)
    print_message('\nКритерий Сэвиджа (меньше - лучше)')
    print_list_in_column(strategy)
    recount_priority(priority, define_min(strategy))

    strategy = Hurwitz_matrix(matrix)
    print_message('\nКритерий Гурвица, основанный на выигрыше (больше - лучше)')
    print_list_in_column(strategy)
    recount_priority(priority, define_max(strategy))

    strategy = Hurwitz_risk(risk)
    print_message('\nКритерий Гурвица, основанный на риске (меньше - лучше)')
    print_list_in_column(strategy)
    recount_priority(priority, define_min(strategy))

    return priority


def recount_priority(priority, _pr):
    """ Пересчитать приоритет в зависимости от нового критерия """
    for i in _pr:
        priority[i] += one


def count_risk(matrix):
    """ Посчитать матрицу рисков """
    # beta[j] = max(i) matrix[i][j]
    beta = [zero for _ in range(len(matrix[0]))]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > beta[j]:
                beta[j] = matrix[i][j]
    
    # r - матрица рисков
    r = []
    for i in range(len(matrix)):
        line = []
        for j in range(len(matrix[i])):
            line.append(beta[j] - matrix[i][j])
        r.append(line)
    return r


def with_probability(risk, probability):
    """ Критерий, основанный на известных вероятностях условиях """
    r_medium = []
    for i in range(len(risk)):
        sum = zero
        for j in range(len(risk[i])):
            sum += probability[j] * risk[i][j]
        r_medium.append(sum)
    return r_medium


def Wald(matrix):
    """ Критерий Вальда """
    # найдем min(j) matrix[i][j]
    m = []
    for i in matrix:
        m.append(min(i))

    return m


def Savage(risk):
    """ Критерий Сэвиджа """
    # найдем max(j) risk[i][j]
    m = []
    for i in risk:
        m.append(max(i))

    return m


def Hurwitz_matrix(matrix):
    """ Критерий Гурвица, основанный на выигрыше """
    g = []
    for i in matrix:
        g.append(optimism_factor * min(i) + (one - optimism_factor) * max(i))
    return g


def Hurwitz_risk(risk):
    """ Критерий Гурвица, основанный на риске """
    g = []
    for i in risk:
        g.append(optimism_factor * max(i) + (one - optimism_factor) * min(i))
    return g


def define_max(_list):
    """ Поиск всех максиминов в указанном массиве
        Возвращает все индексы максиминов """
    priority = []
    _max = -inf
    for i in range(len(_list)):
        if _list[i] > _max:
            priority = [i]
            _max = _list[i]
        elif _list[i] == _max:
            priority.append(i) 
    return priority


def define_min(_list):
    """ Поиск всех минимаксов в указанном массиве
        Возвращает все индексы минимаксов """
    priority = []
    _min = inf
    for i in range(len(_list)):
        if _list[i] < _min:
            priority = [i]
            _min = _list[i]
        elif _list[i] == _min:
            priority.append(i) 
    return priority

def inc(_list):
    """ Увеличить каждый элемент списка на 1 """
    return [i + one for i in _list]


if __name__ == '__main__':
    probability, matrix = reading()
    print_input_data(probability, matrix)
    result = inc(define_max(find_solution(matrix, probability)))

    print_message('\nВ результате анализа всех критериев, делаем вывод, что наиболее оптимальные стратегии это ' + str(result))


