#!/usr/bin/env python

import sys
import datetime


def remote_branch(stdin_first_line):
    """
    Reads the name of the remote git branch from runtime parameters.
    In the pre-push.py hook the name of the remote branch is passed as the $1 parameter.
    :param stdin_first_line the first line of the standard input

    >>> remote_branch("refs/heads/master a9d45baccd631601087a75a6605909c16bbfdbca refs/heads/master 67b6dc7a5e256ae590d305a766e627258b164899")
    'master'
    >>> remote_branch("refs/heads/master a9d45baccd631601087a75a6605909c16bbfdbca refs/heads/hot-fix 67b6dc7a5e256ae590d305a766e627258b164899")
    'hot-fix'
    """
    stdin_parts = stdin_first_line.split(" ")
    remote = stdin_parts[2]
    remote_parts = remote.split("/")
    return remote_parts[-1]


def day_of_week():
    """
    Returns the integer indicating the day of week.
    Uses the datetime package so, Monday is 0 and Sunday is 6.
    """
    return datetime.datetime.today().weekday()


def hour_of_day():
    """
    Returns the current hour as an integer.
    :return:
    """
    return datetime.datetime.today().hour


def should_deploy(branch_name, day_of_week, hour_of_day):
    """
    Returns true if the code can be deployed.
    :param branch_name: the name of the remote git branch
    :param day_of_week: the day of the week as an integer
    :param hour_of_day: the current hour
    :return: true if the deployment should continue

    >>> should_deploy("hot-fix", 0, 10)
    True
    >>> should_deploy("hot-fix", 4, 10) #this branch can be deployed on Friday
    True
    >>> should_deploy("hot-fix", 5, 10) #this branch can be deployed on Saturday
    True
    >>> should_deploy("hot-fix", 6, 10) #this branch can be deployed on Sunday
    True
    >>> should_deploy("hot-fix", 0, 7) #this branch can be deployed before 8am
    True
    >>> should_deploy("hot-fix", 0, 16) #this branch can be deployed after 4pm
    True

    >>> should_deploy("master", 0, 10)
    True
    >>> should_deploy("master", 4, 10) #master cannot be deployed on Friday
    False
    >>> should_deploy("master", 5, 10) #master cannot be deployed on Saturday
    False
    >>> should_deploy("master", 6, 10) #master cannot be deployed on Sunday
    False
    >>> should_deploy("master", 0, 7) #master cannot be deployed before 8am
    False
    >>> should_deploy("master", 0, 16) #master cannot be deployed after 4pm
    False

    """
    if branch_name == "master" and day_of_week >= 4:
        return False
    elif branch_name == "master" and (hour_of_day < 8 or hour_of_day >= 16):
        return False
    else:
        return True


if __name__ == "__main__":
    print "Verifying deployment hours..."
    deploy = should_deploy(remote_branch(sys.stdin.readline()), day_of_week(), hour_of_day())

    if deploy:
        sys.exit(0)
    else:
        print "[ABORTED] Push stopped by the \"deployment hours\" pre-push hook!"
        print "If you know what you are doing and still want to push your code, use the --no-verify parameter"
        sys.exit(1)
