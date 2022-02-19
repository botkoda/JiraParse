# import requests
from datetime import datetime
import re
# from bs4 import BeautifulSoup
from jira import JIRA
import csv
import cx_Oracle

def get_html():
    options = {'server': 'http://10.226.90.42/jira/'}
    jira = JIRA(options, basic_auth=('dmshagaliev', 'Idohori123'))
    projects = jira.projects()[5].key #5-RNDOB 6-TIS   8-CDS
    total = jira.search_issues('project='+projects).total
    reporter_comments = []
    description_comments = []
    data = []
    created_comments = []
    block_size = 1000
    block_num = 0
    while True:
        start_idx = block_num*block_size
        issues = jira.search_issues('project='+projects, start_idx, block_size)
        if len(issues) == 0:
            break
        block_num += 1
    #issues = jira.search_issues('project='+projects, 1500, 300) 
        for i in issues:
            try:
                sus = jira.issue(i.key)
            except:
                sus = ''
            try:
                project = sus.fields.project.key
            except:
                project = ''
            try:
                key = i.key
            except:
                key = ''
            try:
                name = sus.fields.issuetype.name
            except:
                name = ''
            try:
                reporter = sus.fields.reporter.displayName
            except:
                reporter = ''
            try:
                description = sus.fields.description
            except:
                description = ''
            try:
                created = sus.fields.created.split('T')
                created = created[0]+' '+created[-1][:8]
            except:
                created = ''
            try:
                summary = sus.fields.summary
            except:
                summary = ''
            count_comments = int(len(sus.fields.comment.comments))
            if count_comments != 0:
                for j in range(0, count_comments):
                    created_comment = sus.fields.comment.comments[j].created.split(
                        'T')
                    created_comment = created_comment[0] + \
                        ' '+created_comment[-1][:8]
                    reporter_comments.append(
                        sus.fields.comment.comments[j].author.displayName)
                    description_comments.append(
                        sus.fields.comment.comments[j].body)
                    created_comments.append(created_comment)

            data.append({'project': project, 'key': key, 'name': name, 'reporter': reporter, 'description': description, 'created': created, 'summary': summary,
                         'reporter_comments': reporter_comments,
                         'description_comments': description_comments,
                         'created_comments': created_comments
                         })
            sus = ''
            project = ''
            key = ''
            name = ''
            reporter = ''
            description = ''
            created = ''
            summary = ''
            reporter_comments = []
            description_comments = []
            created_comments = []
            # row = [(1, project), (2, key), (3, name), (4, reporter), (5, description), (6, reporter_comments), (7, description_comments)]

        write_csv(data)


def write_csv(data):
    try:
        conn = cx_Oracle.connect('UN_DATA/UN_DATA@10.226.90.129/bitest')
    except:
        print('Нет подключения')
        exit(0)
    cursor = conn.cursor()
    for d in data:
        count_comments = len(d['description_comments'])
        for i in range(0, count_comments):
            sql = '''insert into JIRA_PARSE3
                        (projects,keys,names,reporters,descriptions,reporter_comments, 
                         description_comments,createds,created_comments,summarys) 
                        values 
                        (:project2,:key2,:name2,:reporter2,:description2,:reporter_comments2,
                         :description_comments2,:created2,:created_comments2,:summary2)'''
            cursor.execute(sql, {'project2': d['project'],
                                 'key2': d['key'],
                                 'name2': d['name'],
                                 'reporter2': d['reporter'],
                                 'description2': d['description'],
                                 'reporter_comments2': d['reporter_comments'][i],
                                 'description_comments2': d['description_comments'][i],
                                 'created2': datetime.strptime(d['created'], '%Y-%m-%d %H:%M:%S'),
                                 'created_comments2': datetime.strptime(d['created_comments'][i], '%Y-%m-%d %H:%M:%S'),
                                 'summary2': d['summary']
                                 })
    cursor.close()
    conn.commit()
    conn.close()

def main():

    
    total_pages = get_html()

    pass


if __name__ == '__main__':
    main()
