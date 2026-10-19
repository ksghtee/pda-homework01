import pandas as pd
import re
from typing import Tuple

df = pd.read_csv('isu_fake_data.csv')
df_suir = df[df['факультет'].str.contains('факультет систем управления и робототехники', na = False, case = False)]
# Задача 1
def filter_fsuir_students(data: pd.DataFrame) -> Tuple[int, int, pd.DataFrame]:
    """
    Создает подвыборку студентов факультета систем управления и робототехники (ФСУиР).
    Возвращает количество таких студентов, количество уникальных групп и отфильтрованный датасет.
    """
    
    count_suir = len(df_suir)
    groups_suir = df_suir['группа'].nunique()
    return count_suir, groups_suir, df_suir


# Задача 2
def find_homonymous_students(df: pd.DataFrame) -> Tuple[bool, int, pd.Series, str]:
    """
    Проверяет наличие однофамильцев на ФСУиР, их количество, распределение по курсам
    и определяет группу с наибольшим числом однофамильцев.
    Возвращает:
     - логическое значение (наличие однофамильцев)
     - общее количество однофамильцев
     - серию с числом однофамильцев по курсам
     - группу с максимальным числом однофамильцев
    """

    df_suir['фамилия'] = df_suir['фио'].str.split().str[0]
    surname_counts = df_suir['фамилия'].value_counts()
    duplicates = surname_counts[surname_counts>1].index
    df_odnofam = df_suir[df_suir['фамилия'].isin(duplicates)]
    df_course_odnofam = df_odnofam.groupby('курс').size().sort_index()
    group_odnofam = df_odnofam.groupby('группа').size()
    group_max_odnofam_name = group_odnofam.idxmax()
    vsevo = df_odnofam.groupby('курс').size().sum()
    return True if len(duplicates)>0 else False, vsevo, df_course_odnofam, group_max_odnofam_name
    

# Задача 3
def gender_identification(patronym: str) -> str:
    """
    Определяет пол по отчеству. Возвращает пол: female/male/unknown.
    """
    pass
def analyze_patronyms(df: pd.DataFrame) -> Tuple[int, pd.Series]:
    """
    Определяет количество студентов без отчества и распределение студентов по полу на основе отчества.
    Возвращает:
     - количество студентов без отчества
     - серию с распределением студентов по полу 
    """
    df_suir['отчество'] = df_suir['фио'].str.split().str[2]
    no_otchestvo = df_suir['отчество'].isna().sum()
    df_girls = df_suir[df_suir['отчество'].str.contains('на', na=False)]
    df_boys = df_suir[df_suir['отчество'].str.contains('ич', na = False)]
    gender_counts = pd.DataFrame([[len(df_girls), len(df_boys), len(df_suir)-len(df_girls)-len(df_boys)-no_otchestvo]], columns = ['девушек','парней','не определено по отчеству'])
    return no_otchestvo, gender_counts


# Задача 4
def faculty_statistics(data: pd.DataFrame) -> Tuple[pd.DataFrame, Tuple[str, int], Tuple[str, int]]:
    """
    Подсчитывает количество студентов на каждом факультете,
    а также определяет факультеты с максимальным и минимальным числом студентов.
    """
    students_faculty = df.groupby('факультет').size()
    max = students_faculty.idxmax()
    min = students_faculty.idxmin()
    return students_faculty, max, min


# Задача 5
def course_statistics(data: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    """
    Вычисляет среднее и медианное число студентов на каждом курсе.
    Возвращает две серии с результатами: сначала средние, потом медиана.
    """
    students_courses = df.groupby('курс').size()
    return students_courses.mean(), students_courses.median()


# Задача 6
def most_popular_name(data: pd.DataFrame) -> Tuple[str, str, str, int, float]:
    """
    Определяет самое популярное имя, группу с наибольшим количеством студентов с этим именем,
    факультет, курс и долю таких студентов в общем числе.
    Возвращает результат в следующем порядке:
     1. самое частое имя
     2. группа
     3. факультет
     4. доля
    """
    df['имя'] = df['фио'].str.split().str[1]
    names = df.groupby('имя').size()
    df_most_popular_name = df[df['имя'] == names.idxmax()][['курс', 'факультет', 'группа']]
    mpn_groups = df_most_popular_name.groupby('группа').size()
    df_vsp = df[df['группа'] == mpn_groups.idxmax()].iloc[0]
    course = df_vsp['курс']
    fac = df_vsp['факультет']
    name_ratio = len(df_most_popular_name)/len(df)
    return names.idxmax(), mpn_groups.idxmax(),  fac, course, f'{name_ratio:.2f}'

# Задача 7
def find_students_with_name_starting_P(data: pd.DataFrame) -> pd.DataFrame:
    """
    Находит студентов, чье имя встречается ровно один раз и начинается на "П". Выводит их ФИО, факультет и курс.
    """
    pass


# Задача 8
def highest_avg_grade_faculty(data: pd.DataFrame) -> Tuple[str, str, int]:
    """
    Находит факультет, на котором средний балл студентов третьего курса самый высокий.
    Определяет пол, средний балл котого выше.
    Сначала возвращает факультет, затем пол, затем балл.
    """
    pass


# Задача 9
def find_consecutive_students(data: pd.DataFrame) -> pd.DataFrame:
    """
    Находит первых 5 студентов, которым номера были присвоены подряд.
    Выводит их ФИО, факультет, курс и номер группы.
    """
    pass


if __name__ == "__main__":
    data = pd.read_csv("isu_fake_data.csv")
    # data["surname"] = "put your code here"
    # data["name"] = "put your code here"
    # data["patronim"] = "put your code here"
    
    # Задача 1
    num_students, num_groups, fsuir = filter_fsuir_students(data)
    print(f"Задача 1:\nСтудентов на ФСУиР: {num_students}, Групп: {num_groups}\n\n")
    
    # Задача 2
    has_homonyms, total_homonyms, homonyms_per_course, max_homonym_group = find_homonymous_students(fsuir)
    print("Задача 2:")
    print(f"Есть однофамильцы: {has_homonyms}, Всего: {total_homonyms}, Группа с максимумом: {max_homonym_group}")
    print(f"На каждом курсе: {homonyms_per_course}\n\n")
    
    # Задача 3
    students_without_patronym, gender_counts = analyze_patronyms(fsuir)
    print('Задача 3:\n')
    print(f"Студентов без отчества: {students_without_patronym}")
    print("Распределение по полу:\n", gender_counts, '\n\n')
    
    # Задача 4
    faculty_counts, max_faculty, min_faculty = faculty_statistics(data)
    print('Задача 4:\n')
    print(f"Факультет с наибольшим числом студентов: {max_faculty}")
    print(f"Факультет с наименьшим числом студентов: {min_faculty}\n\n")
    
    # Задача 5
    mean_students, median_students = course_statistics(data)
    print('Задача 5:\n')
    print("Среднее число студентов на курсах:", mean_students)
    print("Медианное число студентов на курсах:", median_students, '\n\n')
    
    # Задача 6
    popular_name, name_group, faculty, course, name_ratio = most_popular_name(data)
    print('Задача 6:\n')
    print(f"Самое популярное имя: {popular_name},\nГруппа: {name_group},\nФакультет: {faculty},\nКурс: {course}")
    print(f"Доля студентов с этим именем: {name_ratio}\n\n")
    
    # Задача 7
    result_7 = find_students_with_name_starting_P(data)
    print("Студенты с именем, начинающимся на П и встречающимся ровно один раз:")
    print(result_7)
    
    # Задача 8
    fac, best_gender, best_grade = highest_avg_grade_faculty(data)
    print(f"Факультет с высоким средним баллом 3-го курса: {fac}")
    print(f"Пол с наивысшим средним баллом: {best_gender}, Средний балл: {best_grade}")
    
    # Задача 9
    result_9 = find_consecutive_students(data)
    print("Первые 5 студентов с подряд идущими табельными номерами:")
    print(result_9)
