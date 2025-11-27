import requests
import pandas as pd
from event_classifier import is_promoted
from dateutil.parser import parse

# 设置好时间参数即可自动爬取并分析这段时间的issue数据
# 时间参数格式：YYYY/MM/DD
start_date = '2021/05/01'
end_date = '2021/05/31'

token = ''  # Add Your Token Here

# Data collection and analysis
date_range = pd.date_range(start=start_date, end=end_date, freq="D")

issue_list = []
for date in date_range:
    print(f'Getting issues created at {str(date.strftime("%Y-%m-%d"))}:')
    date_str = str(date.strftime("%Y%m%d"))
    issue_list_payload = {'access_token': token,
                          'state': 'all',
                          'sort': 'created',
                          'direction': 'asc',  # desc/asc
                          'per_page': 100,
                          'created_at': date_str
                          }
    r = requests.get("https://gitee.com/api/v5/repos/mindspore/mindspore/issues", params=issue_list_payload)
    daily_issues = r.json()

    for issue in daily_issues:
        created_at = issue['created_at']

        if parse(created_at).replace(tzinfo=None).date() != date:
            break

        issue_id = issue['id']
        number = issue['number']  # Gitee issue URL
        comments_url = issue['comments_url']
        owner = issue['user']
        owner_id = owner['id']
        owner_login = owner['login']
        owner_name = owner['name']

        issue_operate_logs = requests.get(
            f"https://gitee.com/api/v5/repos/mindspore/issues/{number}/operate_logs",
            params={'access_token': token, 'repo': 'mindspore', 'sort': 'desc'}).json()
        issue_comments = requests.get(
            comments_url, params={'access_token': token, 'per_page': 100}).json()

        issue_status = is_promoted(owner_id, issue_operate_logs, issue_comments)

        print(number, owner_id, owner_login, owner_name, created_at,
              issue_status[1], issue_status[2])  # 1 label_flag, 2 assign_flag

        issue_list.append((number, owner_id, owner_login, owner_name, created_at,
                           issue_status[1], issue_status[2]))

# 输出已处理的issue列表
name = ['issue_number', 'owner_id', 'owner_login', 'owner_name', 'created_at',
        'is_labeled', 'is_assigned']
issue_list_df = pd.DataFrame(columns=name, data=issue_list)
issue_list_df.drop_duplicates(['issue_number'])
issue_list_df.to_csv('data/MindSpore_issue_list(20210601).csv')
