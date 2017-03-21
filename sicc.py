import os
import random
import datetime

import git

FORMAT_STRING = " 01:01:{0}"

def generate_repo(startday, mask):
    repo_dir = os.path.join(os.getcwd(), 'GitSicco')
    new_file = os.path.join(repo_dir, 'sicc')

    r = git.Repo.init(repo_dir)

    f = open(new_file, 'wb')
    date = startday
    for i in range(len(mask)):
        for j in range(mask[i]):
            date_string = get_date_string(date, j)
            print(date_string)
            r.index.add([new_file])
            r.index.commit("commit{0}.{1}".format(str(i), str(j)))
            hexsha = r.head.commit.hexsha
            bash_string = """
            if [ $GIT_COMMIT = {0} ]
             then
                 export GIT_AUTHOR_DATE="{1}"
                 export GIT_COMMITTER_DATE="{1}"
             fi""".format(hexsha, date_string)
            r.git.filter_branch('-f', '--env-filter', bash_string)
        date += 1

def get_date_string(date, int_sec):
    sec = str(int_sec)
    str_sec = sec
    if len(sec) != 2:
        str_sec = '0' + sec
    temp = datetime.date.fromordinal(date)
    iso_array = temp.isoformat().split('-')
    iso_array[0] = iso_array[0][-2:]
    to_return = iso_array[1] + '-' +  iso_array[2] + '-' + iso_array[0]
    return to_return + FORMAT_STRING.format(str_sec)

generate_repo(300000, [1,2,1])
