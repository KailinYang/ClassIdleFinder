import pandas as pd
import os
import re


def read_file_meta(file_name: str = '课表.xls'):
    # 读取Excel文件
    file_path = file_name
    df = pd.read_excel(file_path, header=None)

    # 获取第二行数据
    second_row = df.iloc[1]

    # 将 NaN 值替换为空字符串
    second_row = second_row.fillna('')


    # 将第二行数据连接成一个字符串
    second_row_str = ' '.join(map(str, second_row.values))

    # 使用正则表达式解析所需信息
    grade = re.search(r'年级：(\d+)', second_row_str).group(1)
    num_students = re.search(r'人数：(\d+)', second_row_str).group(1)
    semester = re.search(r'(\d{4}-\d{4}学年第\d学期)', second_row_str).group(1)
    class_name = re.search(r'班级名称：(.+)', second_row_str).group(1)

    # 打印提取的信息
    print("年级:", grade)
    print("人数:", num_students)
    print("学期:", semester)
    print("班级名称:", class_name.strip())
    return {
        'grade': grade,
        'num_students': num_students,
        'semester': semester,
        'class_name': class_name.strip()
    }

def read_file_table(file_name: str = '课表.xls'):
    # 读取Excel文件
    sheet_name = 'Sheet1'  # 根据实际情况修改表名

    # 跳过前两行，从第3行开始读取，并设置header=None，因为表头不规范
    # df = pd.read_excel(file_name, sheet_name=sheet_name, header=None, skiprows=2, engine='openpyxl')
    df = pd.read_excel(file_name, sheet_name=sheet_name, header=None, skiprows=2, engine='xlrd')

    # 重置列名
    df.columns = ['时间', '节次', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']

    # 丢弃不需要的“时间”列
    df.drop(columns=['时间'], inplace=True)

    # 遍历第一列
    for i in range(df.shape[0]):
        # 更新值
        if isinstance(df.iloc[i, 0], str):
            df.iloc[i, 0] = df.iloc[i, 0].replace('\n', '').strip()

    # 重置行索引
    df.set_index('节次', inplace=True)
    return df

    # print(df)
    # print(df.loc['第一二节', '星期一'])


def read_file_list(directory: str = '2023级新生课表'):

    # 使用 os.listdir() 列出目录中的所有文件和文件夹
    all_items = os.listdir(directory)

    # 过滤出目录中的文件（排除文件夹）
    files = [item for item in all_items if os.path.isfile(os.path.join(directory, item))]
    
    # 只保留 Excel 文件
    files = [item for item in files if item.endswith('.xls')]
    
    return files

def get_db():
    directory = '2023级新生课表'
    files = read_file_list(directory)
    db = []
    for file in files:
        print(file)
        tb = read_file_table(os.path.join(directory, file))
        meta = read_file_meta(os.path.join(directory, file))
        db.append({
            'meta': meta,
            'table': tb
        })
    return db

# 查询空闲教室，x为节次，y为星期, db为数据库, z为周数
def query(db, x, y, z=0):
    ans = []
    for item in db:
        if not isinstance(item['table'].loc[x, y], str):
            ans.append(item['meta']['class_name'])
        else:
            text = item['table'].loc[x, y]
            free_time = True

            # 定义正则表达式
            pattern = r'([^☆]+)◇([^◇]+)(?:◇([^◇]*))?(?:◇([^◇]*))?(?:◇(\d+-\d+))?'
            pattern = r'([^☆]+)◇([^◇]+)◇([^◇]+)◇([^◇]+)◇(\d+-\d+)'
            pattern = r'([^◇☆]+)◇([^◇☆]+)(?:◇([^◇☆]+))?(?:◇([^◇☆]+))?(?:◇([^◇☆]+))?(?:☆|$)'

            # for ct in text.split('☆'):
            # 使用正则表达式查找所有匹配项
            matches = re.findall(pattern, text)

            # 打印结果\
            print("debug::" , matches, text)
            for match in matches:
                
                course_name, classes, teacher, location, weeks = match
                
                if not weeks:
                    weeks = location
                    location = teacher
                    teacher = classes

                print(f"课程名称: {course_name}")
                print(f"班级: {classes}")
                print(f"教师: {teacher}")
                print(f"上课地点: {location}")
                print(f"上课周数: {weeks}")
                print()
                for week in weeks.split(','):
                    if "双" in week:
                        week = week.replace("双", "")
                        if z in [int(i) for i in range(int(week.split('-')[0]), int(week.split('-')[1]), 2)]:
                            free_time = False
                        continue
                    if "单" in week:
                        week = week.replace("单", "")
                        if z in [int(i) for i in range(int(week.split('-')[0]), int(week.split('-')[1]), 2)]:
                            free_time = False
                        continue
                    if "节" in week:
                        _pattern = r"\d+-\d+"
                        _match = re.search(_pattern, week)
                        if _match:
                            week = _match.group()
                    rg = list(map(int, week.split('-'))) + [0x3f]
                    if z >= rg[0] and z <= rg[1]:
                        free_time = False
            if free_time: ans.append(item['meta']['class_name'])
    return sorted(ans)

def main():
    db = get_db()
    while True:
        y = input('请输入要查询的星期：')
        x = input('请输入要查询的节次：')
        ans = []
        for item in db:
            if not isinstance(item['table'].loc[x, y], str):
                ans.append(item['meta']['class_name'])
        print(ans)


if __name__ == '__main__':
    main()