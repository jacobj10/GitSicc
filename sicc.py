import os
import random
from hashlib import sha1
from random import random
import git


repo_dir = os.path.join(os.getcwd(), 'GitSicco')

new_file = os.path.join(repo_dir, 'sicc')

r = git.Repo.init(repo_dir)

f = open(new_file, 'wb')
for i in range(5):
    r.index.add([new_file])
    r.index.commit("commit{0}".format(str(i)))
    hexsha = r.head.commit.hexsha
    bash_string = """
    if [ $GIT_COMMIT = {0} ]
     then
         export GIT_AUTHOR_DATE="Fri Jan 2 21:38:53 2009 -0800"
         export GIT_COMMITTER_DATE="Sat May 19 01:01:01 2007 -0700"
     fi""".format(hexsha)
    r.git.filter_branch('-f', '--env-filter', bash_string)
