import pandas as pd
import matplotlib.pyplot as plt


path = r"C:\Users\NikolaySanin\Desktop\database.xlsx"

department = pd.read_excel(path, sheet_name='department')
subject = pd.read_excel(path, sheet_name='subject')
program = pd.read_excel(path, sheet_name='program')
enrollee = pd.read_excel(path, sheet_name='enrollee')
achievement = pd.read_excel(path, sheet_name='achievement')
enrollee_achievement = pd.read_excel(path, sheet_name='enrollee_achievement')
program_subject = pd.read_excel(path, sheet_name='program_subject')
program_enrollee = pd.read_excel(path, sheet_name='program_enrollee')
enrollee_subject = pd.read_excel(path, sheet_name='enrollee_subject')



#Отчет №1. Статистика результатов по предмету (max, min, mean, median)

def max_min_mean_subject(discipline):
    discipline = discipline.strip().lower().capitalize()
    if discipline not in ['Русский язык', 'Математика', 'Информатика', 'Физика']:
        return 'Такого предмета нет. Повторите попытку'
    table = subject.merge(enrollee_subject, on='subject_id', how='inner')
    table = table.query('name_subject == @discipline')
    
    

    max_result = table['result'].max()
    min_result = table['result'].min()
    mean_result = round(table['result'].mean(), 2)
    median_result = table['result'].median()
    return f'''Предмет: {discipline}
Максимальный балл: {max_result}
Минимальный балл: {min_result}
Средний балл: {mean_result}
Медианный балл: {median_result}'''

disciplines = pd.unique(subject['name_subject'])
print('Список предметов: ')
print(*list(discipline for discipline in disciplines), sep = ', ')
discipline = input('Выберите один из предметов: ')
print(max_min_mean_subject(discipline))



#Отчет №2 Список абитуриентов c баллами за все предметы (с медалью)
#между двух значений (баллов), которые выбирает пользователь

def over_and_under(start, end):
    table = enrollee_subject[['enrollee_id', 'result']]
    table = table.groupby(['enrollee_id']).sum()
    table = table.merge(enrollee_achievement, on='enrollee_id', how='inner')
    table = table.merge(achievement, on='achievement_id', how='inner')[['enrollee_id', 'result', 'bonus']]
    table['All'] = table['result'] + table['bonus']
    table = table[['enrollee_id', 'All']].sort_values(by='All', ascending=False)
    table = table.merge(enrollee, on='enrollee_id', how='inner')[['enrollee_id', 'name_enrollee', 'All']]
    table.set_index('enrollee_id', inplace=True)
    
    under_table = table.query('All >= @start')
    over_table = table.query('All <= @end')
    table = over_table.merge(under_table, on='enrollee_id', how='inner')[['name_enrollee_x', 'All_x']]
    table.columns = ['Имя', 'Общее количество баллов']
    table.drop_duplicates(inplace=True)
    if len(table) == 0:
        return 'Студентов с такими баллами не нашлось'
    return table



print('Введите нижний и верхний порог баллов студентов через пробел: ')
start, end = list(map(int, input().split()))
print(f'Абитуриенты, у которых больше {start} баллов, но меньше {end}: ')
print(over_and_under(start, end))

#Отчет №3. Список абитуриентов (+ баллы и медаль), подавших заявление на программу

def applicants_of_program(name_of_program):
    name_of_program = name_of_program.strip().lower().capitalize()
    if name_of_program not in ['Прикладная математика и информатика', 'Прикладная механика', 'Мехатроника и робототехника', 'Математика и компьютерные науки']:
        return 'Такой программы нет. Повторите попытку'
    main_table = program.merge(program_enrollee, on='program_id', how='inner')
    main_table = main_table.merge(enrollee, on='enrollee_id', how='inner')
    
    math_table = enrollee_subject.merge(subject, on='subject_id', how='inner')
    math_table = math_table.query('name_subject == "Математика"')[['name_subject', 'enrollee_id', 'result']]
    math_table.reset_index(drop=True, inplace=True)
    
    rus_table = enrollee_subject.merge(subject, on='subject_id', how='inner')
    rus_table = rus_table.query('name_subject == "Русский язык"')[['name_subject', 'enrollee_id', 'result']]
    rus_table.reset_index(drop=True, inplace=True)

    inf_table = enrollee_subject.merge(subject, on='subject_id', how='inner')
    inf_table = inf_table.query('name_subject == "Информатика"')[['name_subject', 'enrollee_id', 'result']]
    inf_table.reset_index(drop=True, inplace=True)
    
    phy_table = enrollee_subject.merge(subject, on='subject_id', how='inner')
    phy_table = phy_table.query('name_subject == "Физика"')[['name_subject', 'enrollee_id', 'result']]
    phy_table.reset_index(drop=True, inplace=True)
    
    ach_table = enrollee_achievement.merge(achievement, on='achievement_id', how='inner')[['enrollee_id', 'bonus']]
    

    main_table = main_table.query('name_program == @name_of_program')[['name_enrollee', 'enrollee_id']]
    main_table = main_table.merge(rus_table, on='enrollee_id', how='inner', suffixes=('_xx', '_yy'))[['name_enrollee', 'enrollee_id', 'result']]
    main_table = main_table.merge(math_table, on='enrollee_id', how='inner', suffixes=('_xx', '_yy'))[['name_enrollee', 'enrollee_id', 'result_xx', 'result_yy']]
    main_table = main_table.merge(phy_table, on='enrollee_id', how='inner', suffixes=('_x', '_y'))[['name_enrollee', 'enrollee_id', 'result_xx', 'result_yy', 'result']]
    main_table = main_table.merge(inf_table, on='enrollee_id', how='inner', suffixes=('_x', '_y'))[['name_enrollee', 'enrollee_id', 'result_xx', 'result_yy', 'result_x', 'result_y']]
    main_table.columns = ['Имя', 'enrollee_id', 'Rus', 'Math', 'Phy', 'Inf']
    main_table['bonus'] = ach_table['bonus']
    main_table['All'] = main_table['Rus'] + main_table['Math'] + main_table['Phy'] + main_table['Inf'] + main_table['bonus']
    main_table.set_index('enrollee_id', inplace=True)
    main_table.sort_values(by='All', ascending=False, inplace=True)
    
    return main_table

programs = pd.unique(program['name_program'])
print('Список образовательных программ: ')
print(*list(i for i in programs), sep = ', ')
name_of_program = input('Выберите одну из программ: ')
print(applicants_of_program(name_of_program))


#Графический отчет №1. Популярность образовательных программ

def func_graph_1(programs):
    dict_1 = {'Математика и компьютерные науки': 'МКН', 'Мехатроника и робототехника': 'МиР', 'Прикладная математика и информатика': 'ПМИ', 'Прикладная механика': 'ПМ', '1': 'ПМИ', '2': 'МКН', '3': 'ПМ', '4' : 'МиР'}
    dict_2 = {'1': 'Прикладная математика и информатика', '2': 'Математика и компьютерные науки', '3' :'Прикладная механика', '4' : 'Мехатроника и робототехника'}
    labels = []
    programs = [dict_2[program.strip()] if program.strip().isdigit() else str(program).strip().lower().capitalize() for program in programs]
    for name in programs:
        if name not in ['Прикладная математика и информатика', 'Прикладная механика', 'Мехатроника и робототехника', 'Математика и компьютерные науки']:
            return 'Одна из введенных программ не существует. Повторите попытку'
        labels.append(dict_1[name])
    table = program_enrollee.merge(program, on='program_id', how='inner')[['program_enrollee_id', 'name_program']]
    table.columns = ['Количество абитуриентов', 'name_program']
    table = table.query('name_program in @programs')
    table = table.groupby('name_program').count()
    table.reset_index(inplace=True)
    plt.bar(table['name_program'], table['Количество абитуриентов'], color=['red', 'blue', 'green', 'yellow'], alpha=0.75)
    plt.xticks(ticks=list(range(len(programs))), labels=labels)
    plt.xlabel('Название образовательной программы')
    plt.ylabel('Количество поданных заявлений')
    plt.grid(axis='both', linewidth=0.3, color='black')
    plt.show()
    return ''

print('Вы можете узнать количество заявлений, поданных на каждую из программ.')
print(f'''Список образовательных программ: 
      Прикладная математика и информатика (1)
      Математика и компьютерные науки (2)
      Прикладная механика (3)
      Мехатроника и робототехника (4)''')
programs = input('Введите названия или номера программ через запятую, которые вас интересуют: ').split(',')
print(func_graph_1(programs))

#Графический отчет №2. Распределение абитуриентов по количеству баллов


def func_graph_2(programs):
    dict_1 = {'Математика и компьютерные науки': 'МКН', 'Мехатроника и робототехника': 'МиР', 'Прикладная математика и информатика': 'ПМИ', 'Прикладная механика': 'ПМ', '1': 'ПМИ', '2': 'МКН', '3': 'ПМ', '4' : 'МиР'}
    dict_2 = {'1': 'Прикладная математика и информатика', '2': 'Математика и компьютерные науки', '3' :'Прикладная механика', '4' : 'Мехатроника и робототехника'}
    labels = []
    programs = [dict_2[program.strip()] if program.strip().isdigit() else str(program).strip().lower().capitalize() for program in programs]
    for name in programs:
        if name not in ['Прикладная математика и информатика', 'Прикладная механика', 'Мехатроника и робототехника', 'Математика и компьютерные науки']:
            return 'Одна из введенных программ не существует. Повторите попытку'
        labels.append(dict_1[name])
    table = enrollee_subject[['enrollee_id', 'result']]
    table = table.groupby(['enrollee_id']).sum()
    table = table.merge(enrollee_achievement, on='enrollee_id', how='inner')
    table = table.merge(achievement, on='achievement_id', how='inner')[['enrollee_id', 'result', 'bonus']]
    table['All'] = table['result'] + table['bonus']
    table = table[['enrollee_id', 'All']].sort_values(by='All', ascending=False)
    table = table.merge(enrollee, on='enrollee_id', how='inner')[['enrollee_id', 'name_enrollee', 'All']]
    table = table.merge(program_enrollee, on='enrollee_id', how='inner')[['enrollee_id', 'name_enrollee', 'program_id', 'All']]
    table = table.merge(program, on='program_id', how='inner')[['name_enrollee', 'name_program', 'All']]
    table = table.query('name_program in @programs')[['name_enrollee', 'All']]
    plt.hist(x=table['All'], bins=30, edgecolor='black')
    plt.xlabel('Баллы абитуриентов за экзамены и достижения')
    plt.ylabel('Количество абитуриентов')
    plt.show()
    return ''
    
print('Вы можете увидеть распределение баллов абитуриентов на определенных программах.')
print(f'''Список образовательных программ: 
          Прикладная математика и информатика (1)
          Математика и компьютерные науки (2)
          Прикладная механика (3)
          Мехатроника и робототехника (4)''')
programs = input('Введите названия или номера программ через запятую, которые вас интересуют: ').split(',')
print(func_graph_2(programs))

#Графический отчет №3. Популярность достижений

def func_graph_3(programs):
    dict_1 = {'Математика и компьютерные науки': 'МКН', 'Мехатроника и робототехника': 'МиР', 'Прикладная математика и информатика': 'ПМИ', 'Прикладная механика': 'ПМ', '1': 'ПМИ', '2': 'МКН', '3': 'ПМ', '4' : 'МиР'}
    dict_2 = {'1': 'Прикладная математика и информатика', '2': 'Математика и компьютерные науки', '3' :'Прикладная механика', '4' : 'Мехатроника и робототехника'}
    labels = []
    programs = [dict_2[program.strip()] if program.strip().isdigit() else str(program).strip().lower().capitalize() for program in programs]
    for name in programs:
        if name not in ['Прикладная математика и информатика', 'Прикладная механика', 'Мехатроника и робототехника', 'Математика и компьютерные науки']:
            return 'Одна из введенных программ не существует. Повторите попытку'
        labels.append(dict_1[name])
    table = enrollee_achievement.merge(achievement, on='achievement_id', how='inner')[['enrollee_id', 'name_achievement']]
    table = table.merge(program_enrollee, on='enrollee_id', how='inner')[['enrollee_id', 'name_achievement', 'program_id']]
    table = table.merge(program, on='program_id', how='inner')[['enrollee_id', 'name_achievement', 'name_program']]
    table = table.query('name_program in @programs')[['enrollee_id', 'name_achievement']]
    table = table.groupby('name_achievement').count()
    table.reset_index(inplace=True)
    table.columns = ['name_achievement', 'count']
    colors = ['#fff35d', '#ffbf32','#c0c0c0', '#e8e8e8']
    plt.pie(table['count'], 
           labels=table['name_achievement'],
          wedgeprops={'edgecolor':'black'},
          colors=colors,
          autopct='%1.1f%%')
    plt.title('Процентное соотношение в достижениях абитуриентов')
    plt.show()

print('Вы можете увидеть процентное соотношение в количестве достижений на выбранных вами программах.')
print(f'''Список образовательных программ: 
          Прикладная математика и информатика (1)
          Математика и компьютерные науки (2)
          Прикладная механика (3)
          Мехатроника и робототехника (4)''')
programs = input('Введите названия или номера программ через запятую, которые вас интересуют: ').split(',')
print(func_graph_3(programs))

#Сводная таблица №1. 
#Количество достижений разных типов в заявлениях на образовательные программы

def func_pivot_1(programs):
    dict_1 = {'Математика и компьютерные науки': 'МКН', 'Мехатроника и робототехника': 'МиР', 'Прикладная математика и информатика': 'ПМИ', 'Прикладная механика': 'ПМ', '1': 'ПМИ', '2': 'МКН', '3': 'ПМ', '4' : 'МиР'}
    dict_2 = {'1': 'Прикладная математика и информатика', '2': 'Математика и компьютерные науки', '3' :'Прикладная механика', '4' : 'Мехатроника и робототехника'}
    labels = []
    programs = [dict_2[program.strip()] if program.strip().isdigit() else str(program).strip().lower().capitalize() for program in programs]
    for name in programs:
        if name not in ['Прикладная математика и информатика', 'Прикладная механика', 'Мехатроника и робототехника', 'Математика и компьютерные науки']:
            return 'Одна из введенных программ не существует. Повторите попытку'
        labels.append(dict_1[name])
    table = program_enrollee.merge(enrollee_achievement, on='enrollee_id', how='inner')[['enrollee_id', 'program_id', 'achievement_id']]
    table = table.merge(achievement, on='achievement_id', how='inner')[['enrollee_id', 'program_id', 'name_achievement']]
    table = table.merge(program, on='program_id', how='inner')[['enrollee_id', 'name_program', 'name_achievement']]
    table.drop_duplicates(inplace=True)
    table = table.query('name_program in @programs')
    pvt = pd.pivot_table(table, index='name_achievement', columns='name_program', aggfunc='count')
    pvt.columns = labels
    return pvt

print('Вы можете увидеть количество достижений всех типов на выбранных вами программах.')
print(f'''Список образовательных программ: 
          Прикладная математика и информатика (1)
          Математика и компьютерные науки (2)
          Прикладная механика (3)
          Мехатроника и робототехника (4)''')
programs = input('Введите названия или номера программ через запятую, которые вас интересуют: ').split(',')
print(func_pivot_1(programs))
print()
print(f'''Аббревиатуры: 
ПМИ - Прикладная математика и информатика
МКН - Математика и компьютерные науки
ПМ - Прикладная механика
МиР - Мехатроника и робототехника''')

#Сводная таблица №2. Средний балл среди поступающих по каждому 
#из предметов на выбранных вами образовательных программах


def func_pivot_2(programs):
    dict_1 = {'Математика и компьютерные науки': 'МКН', 'Мехатроника и робототехника': 'МиР', 'Прикладная математика и информатика': 'ПМИ', 'Прикладная механика': 'ПМ', '1': 'ПМИ', '2': 'МКН', '3': 'ПМ', '4' : 'МиР'}
    dict_2 = {'1': 'Прикладная математика и информатика', '2': 'Математика и компьютерные науки', '3' :'Прикладная механика', '4' : 'Мехатроника и робототехника'}
    labels = []
    programs = [dict_2[program.strip()] if program.strip().isdigit() else str(program).strip().lower().capitalize() for program in programs]
    for name in programs:
        if name not in ['Прикладная математика и информатика', 'Прикладная механика', 'Мехатроника и робототехника', 'Математика и компьютерные науки']:
            return 'Одна из введенных программ не существует. Повторите попытку'
        labels.append(dict_1[name])
    table = enrollee_subject.merge(program_enrollee, on='enrollee_id', how='inner')[['enrollee_id', 'subject_id', 'result', 'program_id']]
    table = table.merge(program, on='program_id', how='inner')[['enrollee_id', 'subject_id', 'result', 'name_program']]
    table = table.query('name_program in @programs')
    table = table.merge(subject, on='subject_id', how='inner')[['enrollee_id', 'name_subject', 'result', 'name_program']]
    table.loc[table['name_program'] == 'Прикладная математика и информатика', 'name_program'] = 'ПМИ'
    table.loc[table['name_program'] == 'Прикладная механика', 'name_program'] = 'ПМ'
    table.loc[table['name_program'] == 'Мехатроника и робототехника', 'name_program'] = 'МиР'
    table.loc[table['name_program'] == 'Математика и компьютерные науки', 'name_program'] = 'МКН'
    table.drop_duplicates(inplace=True)
    pvt = pd.pivot_table(table, values='result', index='name_program', columns='name_subject', aggfunc='mean')
    pvt = pvt.round(1)
    return pvt

print('Вы можете увидеть средний балл среди поступающих по каждому из предметов на выбранных вамиобразовательных программах.')
print(f'''Список образовательных программ: 
          Прикладная математика и информатика (1)
          Математика и компьютерные науки (2)
          Прикладная механика (3)
          Мехатроника и робототехника (4)''')
programs = input('Введите названия или номера программ через запятую, которые вас интересуют: ').split(',')
print(func_pivot_2(programs))
print()
print(f'''Аббревиатуры: 
ПМИ - Прикладная математика и информатика
МКН - Математика и компьютерные науки
ПМ - Прикладная механика
МиР - Мехатроника и робототехника''')


#Сводная таблица №3. Количество абитуриентов, которые не прошли
#на выбранные программы по разным предметам (их балл ниже минимального необходимого)

def func_pivot_3(programs):
    dict_1 = {'Математика и компьютерные науки': 'МКН', 'Мехатроника и робототехника': 'МиР', 'Прикладная математика и информатика': 'ПМИ', 'Прикладная механика': 'ПМ', '1': 'ПМИ', '2': 'МКН', '3': 'ПМ', '4' : 'МиР'}
    dict_2 = {'1': 'Прикладная математика и информатика', '2': 'Математика и компьютерные науки', '3' :'Прикладная механика', '4' : 'Мехатроника и робототехника'}
    labels = []
    programs = [dict_2[program.strip()] if program.strip().isdigit() else str(program).strip().lower().capitalize() for program in programs]
    for name in programs:
        if name not in ['Прикладная математика и информатика', 'Прикладная механика', 'Мехатроника и робототехника', 'Математика и компьютерные науки']:
            return 'Одна из введенных программ не существует. Повторите попытку'
        labels.append(dict_1[name])
    table = enrollee_subject.merge(program_subject, on='subject_id', how='inner')[['enrollee_id', 'subject_id', 'result', 'min_result']]
    table = table.merge(program_enrollee, on='enrollee_id', how='inner')[['enrollee_id', 'subject_id', 'program_id', 'result', 'min_result']]
    table = table.query('result < min_result')
    table = table.drop_duplicates()[['subject_id', 'program_id', 'result']]
    table = table.merge(subject, on='subject_id', how='inner')[['name_subject', 'program_id', 'result']]
    table = table.merge(program, on='program_id', how='inner')[['name_subject', 'name_program', 'result']]
    table = table.query('name_program in @programs')
    table.loc[table['name_program'] == 'Прикладная математика и информатика', 'name_program'] = 'ПМИ'
    table.loc[table['name_program'] == 'Прикладная механика', 'name_program'] = 'ПМ'
    table.loc[table['name_program'] == 'Мехатроника и робототехника', 'name_program'] = 'МиР'
    table.loc[table['name_program'] == 'Математика и компьютерные науки', 'name_program'] = 'МКН'
    pvt = pd.pivot_table(table, index='name_program', columns='name_subject', aggfunc='count', fill_value=0)
    return pvt

print('Вы можете увидеть количество людей, не прошедших на выбранные вами образовательные программы по конкретным предметам.')
print(f'''Список образовательных программ: 
          Прикладная математика и информатика (1)
          Математика и компьютерные науки (2)
          Прикладная механика (3)
          Мехатроника и робототехника (4)''')
programs = input('Введите названия или номера программ через запятую, которые вас интересуют: ').split(',')
print(func_pivot_3(programs))
print()
print(f'''Аббревиатуры: 
ПМИ - Прикладная математика и информатика
МКН - Математика и компьютерные науки
ПМ - Прикладная механика
МиР - Мехатроника и робототехника''')