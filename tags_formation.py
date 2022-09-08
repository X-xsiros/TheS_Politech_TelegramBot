def alarm(group_id):
    file = open(group_id)
    names = file.readlines()
    formed_tags_msg = ''
    for i in names:
        formed_tags_msg += '@' + i[0:-1] + '\n'
    return formed_tags_msg


