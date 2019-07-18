#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os
import json
import subprocess
import time
from os.path import isfile, join
import filecmp
import random
import string


def write_grade(grade, suffix):
    if os.isatty(1):
        print('Removing all files with suffix', suffix)
        os.system('rm -f *{}'.format(suffix))

    data = {}
    data['grade'] = grade
    if os.isatty(1):
        print('Grade: {}/80'.format(grade))
    else:
        print(json.dumps(data))

    sys.exit(0)


if __name__ == '__main__':

    if sys.version_info[0] != 3:
        print("Plz use python3")
        sys.exit()

    suffix = '.' + ''.join([random.choice(string.ascii_lowercase) for i in range(4)])
    if os.isatty(1):
        print('SUFFIX is', suffix)
    os.environ['SUFFIX'] = suffix

    dependency = {}
    dependency[('thesis', 'analytical_mechanics')] = 1
    dependency[('thesis', 'quantum_mechanics')] = 1
    dependency[('thesis', 'statistical_mechanics')] = 1
    dependency[('thesis', 'electrodynamics')] = 1
    dependency[('analytical_mechanics', 'multivariate_calculus')] = 1
    dependency[('analytical_mechanics', 'general_physics')] = 1
    dependency[('analytical_mechanics', 'mathematical_physics')] = 1
    dependency[('thermodynamics', 'multivariate_calculus')] = 1
    dependency[('thermodynamics', 'general_physics')] = 1
    dependency[('statistical_mechanics', 'thermodynamics')] = 1
    dependency[('statistical_mechanics', 'probability_theory')] = 1
    dependency[('quantum_mechanics', 'linear_algebra')] = 1
    dependency[('quantum_mechanics', 'general_physics')] = 1
    dependency[('quantum_mechanics', 'analytical_mechanics')] = 1
    dependency[('multivariate_calculus', 'univariate_calculus')] = 1
    dependency[('mathematical_physics', 'multivariate_calculus')] = 1
    dependency[('mathematical_physics', 'linear_algebra')] = 1
    dependency[('electrodynamics', 'multivariate_calculus')] = 1
    dependency[('electrodynamics', 'general_physics')] = 1
    dependency[('electrodynamics', 'mathematical_physics')] = 1
    dependency[('probability_theory', 'multivariate_calculus')] = 1

    if os.isatty(1):
        print('Removing all files with suffix', suffix)
    os.system('rm -f *{}'.format(suffix))

    grade = 0

    # Part 1
    if os.isatty(1):
        print('Running \'make -n\'')
    p = subprocess.Popen(['make', '-n'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    start_time = time.time()

    while p.poll() is None:
        if time.time() - start_time > 1:
            p.kill()

    stdout, stderr = p.communicate(timeout=1)

    if len(stderr) == 0:
        try:
            lines = stdout.decode('utf-8').split('\n')
            steps = []
            for line in lines:
                if line.startswith('touch '):
                    steps.append(line.split(' ')[1].split('.')[0])

            # check dependency
            flag = 1
            for (a, b) in dependency: # a after b
                try:
                    idx_a = steps.index(a)
                    idx_b = steps.index(b)
                    if idx_a < idx_b:
                        raise Exception()
                except:
                    if os.isatty(1):
                        print('error: {} should appear after {}'.format(a, b))
                    flag = 0
                
            if flag:
                grade += 30

        except Exception:
            if os.isatty(1):
                print('Unexpected stdout:')
                sys.stdout.buffer.write(stdout)
    elif os.isatty(1):
        print('Your program exited with:')
        sys.stdout.buffer.write(stderr)

    if grade != 30:
        write_grade(grade, suffix)


    # Part 2
    if os.isatty(1):
        print('Running \'make\'')
    p = subprocess.Popen(['make'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    start_time = time.time()

    while p.poll() is None:
        if time.time() - start_time > 1:
            p.kill()

    stdout, stderr = p.communicate(timeout=1)
    if len(stderr) == 0:
        try:
            flag = 1
            for course1, course2 in dependency:
                flag_course2 = 0
                path = '{}{}'.format(course1, suffix)
                if not os.path.exists(path):
                    flag = 0
                    if os.isatty(1):
                        print('File missing: {}'.format(path))
                    continue

                with open('{}{}'.format(course1, suffix), 'r') as f:
                    line = f.readline()
                    for depend in line.split(' '):
                        depend = depend.strip()
                        if len(depend) > 0:
                            if not (course1, depend) in dependency:
                                flag = 0
                                if os.isatty(1):
                                    print('Unexpected dependency: {} -> {}'.format(course1, depend))
                            if depend == course2:
                                flag_course2 = 1

                if not flag_course2:
                    if os.isatty(1):
                        print('Dependency missing: {} -> {}'.format(course1, course2))
                    flag = 0
                
            if flag:
                grade += 40
        except Exception:
            if os.isatty(1):
                print('Unexpected stdout:')
                sys.stdout.buffer.write(stdout)
    elif os.isatty(1):
        print('Your program exited with:')
        sys.stdout.buffer.write(stderr)

    if grade != 70:
        write_grade(grade, suffix)


    # Part 3
    if os.isatty(1):
        print('Running \'make clean\'')
    p = subprocess.Popen(['make', 'clean'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    start_time = time.time()

    while p.poll() is None:
        if time.time() - start_time > 1:
            p.kill()

    stdout, stderr = p.communicate(timeout=1)
    if len(stderr) == 0:
        try:
            flag = 1
            for course1, course2 in dependency:
                path = '{}{}'.format(course1, suffix)
                if os.path.exists(path):
                    flag = 0
                    if os.isatty(1):
                        print('File still exists: {}'.format(path))
                    continue
                
            if flag:
                grade += 10
        except Exception:
            if os.isatty(1):
                print('Unexpected stdout:')
                sys.stdout.buffer.write(stdout)
    elif os.isatty(1):
        print('Your program exited with:')
        sys.stdout.buffer.write(stderr)

    write_grade(grade, suffix)

