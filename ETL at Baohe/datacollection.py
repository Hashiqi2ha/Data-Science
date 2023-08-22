# -*- coding: utf-8 -*-
import pymysql
import lxml.etree as le
import datetime



def insert_many_sql(_db_name='', key_list=[]):
    fields_sql = '`,`'.join(key_list)
    values_sql = ','.join((u'%s'.format(t) for t in key_list))
    insert_sql = u'insert ignore into `{}` (`{}`) VALUES ({})'.format(_db_name, fields_sql, values_sql)
    return insert_sql

db_config = {
    'host': '127.0.0.1',  # Server IP Address
    'port': 3306,
    'user': 'root',
    'password': '1234',
    'db': 'work',
    'charset': 'utf8',

}
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

def insertdata(path):
    with open('%s' % path, 'r', encoding='utf-8') as f:
        html = le.HTML(f.read())
        titles = html.xpath('//table[@class="table_s1"]/thead/tr/th/text()')
        titles.append('Year')
        # print(titles)
        trs = html.xpath('//table[@class="table_s1"]/tbody/tr')
        data_list = []
        for tr in trs:
            data = eval(str(tr.xpath('th/text()')).replace(r'\n', '').replace(r'\t', ''))
            data.append(path[:4])
            data_list.append(data)
        # print(data_list)
        return titles, data_list


# sql = insert_many_sql('EI', titles)
# cursor.executemany(sql, data_list)
# conn.commit()
if __name__ == '__main__':
    start = datetime.datetime.now()
    print('Start time：' + str(start))

    key_list, data_list = insertdata('2021.html')
    key_list2, data_list2 = insertdata('2022.html')
    data_list.extend(data_list2)

    # sql = insert_many_sql('qikancaiji', key_list)
    # cursor.executemany(sql, data_list)
    # conn.commit()
    end = datetime.datetime.now()
    print('\n' + 'End time：' + str(end) + '\n')
    print('Execution time：' + str(end - start))
