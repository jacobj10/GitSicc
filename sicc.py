import os
import random
import datetime

import git

FORMAT_STRING = " 01:01:{0}"
INIT_ACTIONS = {
                'open': open,
                'mkdir': os.mkdir,
            }

COMMANDS = [
                "for {0} in range({1}, {2}):",
                "while {0} {1} {2}:,
                "if {0}"
            ]

class GitAssistant(object):
    def __init__(self):
        pass

    def generate_repo(self, startday, mask):
        repo_dir = os.path.join(os.getcwd(), 'GitSicco')
        new_file = os.path.join(repo_dir, 'sicc')

        r = git.Repo.init(repo_dir)
        hashes = []
        dates = []
        f = open(new_file, 'w')
        date = startday
        for i in range(len(mask)):
            for j in range(mask[i]):
                date_string = self.get_date_string(date, j)
                f.write(date_string)
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
        username = r.git.config('user.name')
        r.create_remote('origin', "https://github.com/{0}/GitSicco.git".format(username))

    def get_date_string(self, date, int_sec):
        sec = str(int_sec)
        str_sec = sec
        if len(sec) != 2:
            str_sec = '0' + sec
        temp = datetime.date.fromordinal(date + 1)
        iso_array = temp.isoformat().split('-')
        iso_array[0] = iso_array[0][-2:]
        to_return = iso_array[1] + '-' +  iso_array[2] + '-' + iso_array[0]
        return to_return + FORMAT_STRING.format(str_sec)

    def calculate_start_date(self, year):
        beginning = datetime.datetime(year, 1, 1)
        if beginning.weekday() == 6:
            beginning -= datetime.timedelta(weeks=1)
        while beginning.weekday() != 6:
            beginning -= datetime.timedelta(days=1)
        print(beginning)
        return self.calculate_grid_dimensions(beginning, year)

    def calculate_grid_dimensions(self, beginning, year):
        delta = datetime.datetime(year, 12, 31) - beginning
        cols = int(delta.days / 7)
        last = delta.days % 7 + 1
        return (cols, last, beginning)
