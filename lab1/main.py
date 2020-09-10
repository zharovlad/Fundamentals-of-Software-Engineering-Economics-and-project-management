from copy import deepcopy
from math import inf
# в вводном файле хранится платежная матрица
input_file_name = 'input.txt'
output_file_name = 'output.txt'
# коэффициент оптимизма для критерия Гурвица (0 - наиболее оптимистичный сценарий, 1 - наиболее пессимистичный)
optimism_factor = 0.5


def reading():
    """ Чтение данных из входного файла """
    with open(input_file_name, 'r') as r:
        matrix = []
        for line in r:
            _line = line.split()
            matrix.append([int(element) for element in _line])
    return matrix


def clear_file(file_name=output_file_name):
    """ Очистка выходного файла от результата прошлой работы программы """
    with open(file_name, 'w') as w:
        None
    return


def print_result():
    """ !!! Нужно сделать !!! """
    with open(output_file_name, 'a') as w:
        None


def find_solution(matrix):
    """ Определение решения в зависимости от указанных критериев """
    risk = count_risk(matrix)
    priority = [0 for _ in range(len(matrix))]

    recount_priority(priority, Wald(matrix))
    recount_priority(priority, Savage(risk))
    recount_priority(priority, Hurwitz_matrix(matrix))
    recount_priority(priority, Hurwitz_risk(risk))
    print(priority)


def recount_priority(priority, _pr):
    """ Пересчитать приоритет в зависимости от нового критерия """
    for i in _pr:
        priority[i] += 1


def count_risk(matrix):
    """ Посчитать матрицу рисков """
    # beta[j] = max(i) matrix[i][j]
    beta = [0 for _ in range(len(matrix[0]))]
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


def Wald(matrix):
    """ Критерий Вальда """
    # найдем min(j) matrix[i][j]
    m = []
    for i in matrix:
        m.append(min(i))

    # найдем, собственно, максимин
    return define_max(m)


def Savage(risk):
    """ Критерий Сэвиджа """
    # найдем max(j) risk[i][j]
    m = []
    for i in risk:
        m.append(max(i))

    # найдем, собственно, минимакс
    return define_min(m)


def Hurwitz_matrix(matrix):
    """ Критерий Гурвица, основанный на выигрыше """
    g = []
    for i in matrix:
        g.append(optimism_factor * min(i) + (1 - optimism_factor) * max(i))
    return define_max(g)


def Hurwitz_risk(risk):
    """ Критерий Гурвица, основанный на риске """
    g = []
    for i in risk:
        g.append(optimism_factor * max(i) + (1 - optimism_factor) * min(i))
    return define_min(g)


def define_max(array):
    """ Поиск всех максиминов в указанном массиве
        Возвращает все индексы максиминов """
    priority = []
    _max = -inf
    for i in range(len(array)):
        if array[i] > _max:
            priority = [i]
            _max = array[i]
        elif array[i] == _max:
            priority.append(i) 
    return priority


def define_min(array):
    """ Поиск всех минимаксов в указанном массиве
        Возвращает все индексы минимаксов """
    priority = []
    _min = inf
    for i in range(len(array)):
        if array[i] < _min:
            priority = [i]
            _min = array[i]
        elif array[i] == _min:
            priority.append(i) 
    return priority


if __name__ == '__main__':
    matrix = reading()
    find_solution(matrix)
