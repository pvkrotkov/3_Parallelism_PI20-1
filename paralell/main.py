from multiprocessing import Queue, cpu_count
from multiprocessing.pool import ThreadPool
from random import randint
import csv

with open('paralell.txt', 'r', encoding='utf-8') as file:
    print(*file)

def load_table(files):
    table = []
    try:
        with open(str(files) + '.csv', "r") as f:
            read = csv.reader(f)
            for i in read:
                table.append(i[0].split(';'))
            z = len(table)
            x = len(table[0])
            for i in range(z):
                for k in range(x):
                    table[i][k] = float(table[i][k])
    except OverflowError:
        print("Зафиксировано переполнение")
        table = []
    except OSError:
        print("Файл не обнаружен")
        table = []
    except FileNotFoundError:
        print("Не получилось распознать файл")
        table = []
    except IndexError:
        print("Файл не указан")
        table = []
    return (table)

def matrix_gener(size, max, min, que):
    if finish:
        matrix = []
        for k in range(2):
            matrix.append([])
            for i in range(size):
                matrix[k].append([])
                for p in range(size):
                    matrix[k][i].append(randint(min, max))
        que.put(matrix)

def element(index, A, B):
    i, j = index
    res = 0
    N = len(A[0])
    for k in range(N):
        res += A[i][k] * B[k][j]
    return (res)

def print_table(table):
    s = len(table)
    st = len(table[0])
    m = 0
    for i in table:
        for k in i:
            if m < len(str(k)):
                m = len(str(k))
    otch = '+'
    for i in range(st):
        otch += '-' * (m + 2) + '+'
    otch = '\n' + otch + '\n'
    res = otch
    for i in range(s):
        res += '|'
        for k in range(st):
            res += ' ' + str(table[i][k]) + ' ' * (m - len(str(table[i][k]))) + ' |'
        res += otch
    return (res)

def multipl(que, m_cpu, num, que_b=False):
    if finish:
        if que_b:
            que = que.get()
        matrix1 = que[0]
        matrix2 = que[1]
        d1 = len(matrix1)
        d2 = len(matrix2[0])
        matrix_res = []
        pool = ThreadPool(processes=min(max(2, d1 * d2 - 1), m_cpu))
        for i in range(d1):
            matrix_res.append([])
            for k in range(d2):
                p1 = pool.apply_async(element, ((i, k), matrix1, matrix2))
                matrix_res[i].append(p1.get())

        print('\n' + str(num) + '\nУмножение:' + print_table(matrix1) + 'НА' + print_table(matrix2) + 'Ответ: ' + str(
            num) + print_table(matrix_res) + '\n')

def run(pool, m_cpu, log, que):
    num = 0
    while (num != int(log[1])):
        if finish:
            num += 1
            pros.append(pool.apply_async(multipl, args=(que, m_cpu, num, True)))
            pros.append(pool.apply_async(matrix_gener, args=(int(log[2]), int(log[3]), int(log[4]), que)))

finish = False
pros = []
m_cpu = cpu_count()
while True:
    try:
        que = Queue()

        log = input('Ввод пользователя: ').split(" ")
        if log[0] == 'exit':
            try:
                if pros != []:
                    finish = False
                    for p in pros:
                        p.terminate()
                    else:
                        break
            except AttributeError:
                break
            break
        elif log[0] == 'stop':
            finish = False
            for p in pros:
                p.terminate()
        elif log[0] == 'import':
            lt = [load_table(log[1])]
            lt.append(load_table(log[2]))
            if lt[0] == [] or lt[1] == []:
                print('Таблицы не получены')
            elif len(lt[1]) != len(lt[0][0]):
                print('Умножение невозможно')
            else:
                finish = True
                multipl(lt, m_cpu, 'Из таблиц', False)
        elif log[0] == 'gen':
            if __name__ == "__main__":
                if int(log[3]) < int(log[4]):
                    print('Минимум больше максимума')
                elif int(log[2]) < 0 or log[1].find('.') != -1 or log[2].find('.') != -1 or log[3].find('.') != -1 or log[4].find('.') != -1:
                    print('Некорректный формат ввода')
                else:
                    finish = True
                    pool = ThreadPool(processes=min(max(2, int(log[2]) ** 2), m_cpu))
                    pool = ThreadPool(processes=(int(log[2]) ** 2))
                    pool.apply_async(run, args=(pool, m_cpu, log, que))
        else:
            print('Команда не распознана')

    except AttributeError:
        print('Неверный ввод')
    except IndexError:
        print('Не представлены все необходимые данные')