from random import randint
from multiprocessing.pool import ThreadPool
from multiprocessing import  Queue, cpu_count   #(Manager, Queue#Process, Pool)
#'''
import csv
def  load_table(files):
    table = []
    try:
        with open(str(files)+'.csv', "r") as f:
            read = csv.reader(f)
            for i in read:
                table.append(i[0].split(';'))
            z = len(table)
            x = len(table[0])
            for i in range(z):
                for k in range(x):
                    table[i][k]=float(table[i][k])
    except OverflowError:
        print("Переполнение")
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
    return(table)#'''

'''Генерация'''
def matrix_gener(razmer, max_elem, min_elem, que):
    #global finish
    if finish:
        matric =[]
        for k in range(2):
            matric.append([])
            for i in range (razmer):
                matric[k].append([])
                for p in range (razmer):
                    matric[k][i].append(randint(min_elem, max_elem))
        que.put(matric)

def element(index, A, B):
    i, j = index
    res = 0
    N = len(A[0])
    for k in range(N):
        res += A[i][k] * B[k][j]
    return(res)

def print_tab(tabl):
    s = len(tabl)
    st = len(tabl[0]) 
    m = 0
    for i in tabl:
        for k in i:
            if m < len(str(k)):
                m = len(str(k))
    otch = '+'
    for i in range (st):
        otch += '-'*(m+2)+'+'
    otch = '\n' + otch + '\n'
    rez = otch
    for i in range (s):
        rez+='|'
        for k in range (st):
            rez+=' ' + str(tabl[i][k]) + ' '*(m - len(str(tabl[i][k]))) + ' |'
        rez+= otch
    return(rez)

def oper(que, m_cpu, numb, que_b= False):
    if finish:
        if que_b:
            que = que.get()
        matrix1=que[0]    
        matrix2=que[1]
        d1 = len(matrix1)
        d2 = len(matrix2[0])
        matric_otv=[]
        pool = ThreadPool(processes=min(max(2, d1*d2-1) , m_cpu))
        for i in range (d1):
            matric_otv.append([])
            for k in range (d2):
                p1 = pool.apply_async(element, ((i, k), matrix1, matrix2))
                matric_otv[i].append(p1.get())

        print('\n'+str(numb)+'\nУмножение:'+ print_tab(matrix1)+ ' на '+ print_tab(matrix2)+ ' Ответ: '+str(numb)+ print_tab(matric_otv)+ '\n')
    
def pusk(pool, m_cpu, kom, que):
    nom =0
    while (nom !=int(kom[1])):
        if finish:
                nom +=1
                pros.append(pool.apply_async(oper, args=(que, m_cpu, nom, True)))
                pros.append(pool.apply_async(matrix_gener, args=(int(kom[2]), int(kom[3]), int(kom[4]), que)))
finish = False
pros =[]
m_cpu = cpu_count()
while True:
    try:
        que = Queue()
        
        kom = input('Введите genr {number of mult. -1 for  inf} {sixe} {max} {min} для запуска в режиме автоматической генерации, file {first_file_name} {second_file_name} для запуска в режиме считывания из csv файлов (имена файлов вводить без формата), exit для выхода, stop (для остановки вывода): ').split(" ")
        if kom[0] == 'exit':
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
        elif kom[0] == 'stop':
            finish = False
            for p in pros: 
                p.terminate()
        elif kom[0] == 'file':
            lt=[load_table(kom[1])]
            lt.append(load_table(kom[2]))
            if lt[0] == [] or lt[1] == []:
                print('ERROR: таблицы не получены')
            elif len(lt[1]) != len(lt[0][0]):
                print('Умножение невозможно')
            else:
                finish = True
                oper(lt,m_cpu, 'Из таблиц', False)
        elif kom[0] == 'genr':
            if __name__ == "__main__":
                if int(kom[3])<int(kom[4]):
                    print('Такого не может быть')
                elif int(kom[2]) <0 or kom[1].find('.')!=-1 or kom[2].find('.')!=-1 or kom[3].find('.')!=-1 or kom[4].find('.')!=-1:
                    print('Некорректный формат ввода')
                else:
                    finish = True
                    pool = ThreadPool(processes=min(max(2, int(kom[2])**2) , m_cpu))
                    pool = ThreadPool(processes=(int(kom[2])**2))
                    pool.apply_async(pusk, args=(pool, m_cpu, kom, que))
        else:
            print('Команда не распознана')
                    
    except AttributeError:
        print('Неверный ввод')#'''
    except IndexError:
        print('Не представлены все необходимые данные')
        
#genr 1000 4 100 -100
