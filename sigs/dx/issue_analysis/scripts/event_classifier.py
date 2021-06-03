# 遍历issue列表时调用，以判断该条issue是否满足三个条件
def is_promoted(owner_id, issue_operate_logs, issue_comments):
    # 这里某些项以后可以设置成integer，用以表示单条issue里正面行为的次数（比如打了多个标签）
    total_flag = False
    label_flag = False
    assign_flag = False
    other_flag = False

    # 先看日志里是否有推进issue解决的正面行为
    for action in issue_operate_logs:
        action_owner_id = action['user']['id']
        action_icon = action['icon']
        # 有没有打标签
        if action_owner_id == owner_id and action_icon == 'tag icon':
            label_flag = True
        # 有没有指派负责人/协作人
        if action_owner_id == owner_id and action_icon == 'add user icon':
            assign_flag = True
        # 有没有其他推进issue解决的行为（如设置schedule/milestone）
        if action_owner_id == owner_id and (action_icon != 'add user icon' and action_icon != 'tag icon'):
            other_flag = True

    # 再看评论区里是否有推进issue解决的正面行为
    def is_label_comment(issue_comment):
        # 先简单判断一下前两个字符是不是均为/
        if issue_comment['body'][0] == '/' and issue_comment['body'][1] == '/':
            return True
        else:
            return False

    for comment in issue_comments:
        comment_owner_id = comment['user']['id']
        # 有没有通过评论打标签
        if comment_owner_id == owner_id and is_label_comment(comment):
            label_flag = True
        # 有没有在自己的issue下做回复（不包括与bot互动）
        if comment_owner_id == owner_id and comment['body'][0] != '/':
            other_flag = True

    total_flag = label_flag or assign_flag or other_flag

    return total_flag, label_flag, assign_flag, other_flag
