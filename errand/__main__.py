import os
import time
from enum import Enum
import scipy.stats

from random import randint
from typing import Tuple

import ctypes

# from statistics import mean

from click import group, argument, option

import numpy as np

from .PythonExperiment import PythonExperiment
from .RandeerExperiment import RandeerExperiment
from .Evaluator import Evaluator
from .ParameterGrid import ParameterGrid

from .SamplingMethod import SamplingMethod
from .SamplingApproach import SamplingApproach
from .IterationMethod import IterationMethod

from .Unit import Unit
from .utils import compare_distributions, compare_execution_time

RANDEER_LIBRARY_PATH = os.environ.get('RANDEER_LIBRARY_PATH', '/usr/lib/librandeer.so')
# RANDEER_LIBRARY_PATH = os.environ.get('RANDEER_LIBRARY_PATH', '/usr/lib/libmeager.so')


@group()
def main():
    pass


@main.command()
@argument('seed', type = str, default = "17")
@option('--cpp', '-c', type = bool, is_flag = True)
def randomize(seed: int, cpp: bool):

    grid = ParameterGrid.from_range((0, ), (6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 1000, 10000), ((0, 1, 2, 4, 5, 6), ))

    # for parameter in grid.parameters:
    #     print(parameter)

    # evaluator = Evaluator(
    #     experiments = (
    #         PythonExperiment(
    #             'default looping (python)',
    #             SamplingMethod.LOOPING, SamplingApproach.DEFAULT
    #         ),
    #         PythonExperiment(
    #             'lcg looping (python)',
    #             SamplingMethod.LOOPING, SamplingApproach.LCG
    #         ),
    #         RandeerExperiment(
    #             'default looping with reusable object (c++)',
    #             RANDEER_LIBRARY_PATH, SamplingMethod.LOOPING, SamplingApproach.DEFAULT, IterationMethod.CPP, single_init = True, using_objects = True
    #         )
    #     ),
    #     n_repetitions = 10,
    #     seeds = (17, 19, 21)
    # )

    # evaluator = Evaluator(
    #     experiments = (
    #         PythonExperiment(
    #             'default looping (python)',
    #             SamplingMethod.LOOPING, SamplingApproach.DEFAULT
    #         ),
    #         PythonExperiment(
    #             'default shifting (python)',
    #             SamplingMethod.SHIFTING, SamplingApproach.DEFAULT
    #         ),
    #         RandeerExperiment(
    #             'default looping (c++), iteration in python',
    #             RANDEER_LIBRARY_PATH, SamplingMethod.LOOPING, SamplingApproach.DEFAULT, IterationMethod.PYTHON, single_init = True, using_objects = False
    #         ),
    #         RandeerExperiment(
    #             'default looping (c++), iteration in c++',
    #             RANDEER_LIBRARY_PATH, SamplingMethod.LOOPING, SamplingApproach.DEFAULT, IterationMethod.CPP, single_init = False, using_objects = False
    #         ),
    #         RandeerExperiment(
    #             'default looping (c++), iteration in c++, single init',
    #             RANDEER_LIBRARY_PATH, SamplingMethod.LOOPING, SamplingApproach.DEFAULT, IterationMethod.CPP, single_init = True, using_objects = True
    #         ),
    #         RandeerExperiment(
    #             'default looping (c++), iteration in c++, single init, no intermediate objects',
    #             RANDEER_LIBRARY_PATH, SamplingMethod.LOOPING, SamplingApproach.DEFAULT, IterationMethod.CPP, single_init = True, using_objects = False
    #         )
    #     ),
    #     n_repetitions = 10,
    #     seeds = (17, 19, 21)
    # )

    if cpp:
        evaluator = Evaluator(
            experiments = (
                # RandeerExperiment(
                #     'default looping (c++), iteration in c++, single init',
                #     RANDEER_LIBRARY_PATH, SamplingMethod.LOOPING, SamplingApproach.DEFAULT, IterationMethod.CPP, single_init = True, using_objects = True
                # ),
                # # RandeerExperiment(
                # #     'default looping (c++), iteration in c++, multiple inits',
                # #     RANDEER_LIBRARY_PATH, SamplingMethod.LOOPING, SamplingApproach.DEFAULT, IterationMethod.CPP, single_init = False, using_objects = True
                # # ),
                RandeerExperiment(
                    default_looping := 'default looping (c++), iteration in c++, single init, no intermediate objects',
                    RANDEER_LIBRARY_PATH, SamplingMethod.LOOPING, SamplingApproach.DEFAULT, IterationMethod.CPP, single_init = True, using_objects = False
                ),
                # RandeerExperiment(
                #     'default shifting (c++), iteration in c++, single init',
                #     RANDEER_LIBRARY_PATH, SamplingMethod.SHIFTING, SamplingApproach.DEFAULT, IterationMethod.CPP, single_init = True, using_objects = True
                # ),
                RandeerExperiment(
                    default_shifting := 'default constrained shifting (c++), iteration in c++, single init',
                    RANDEER_LIBRARY_PATH, SamplingMethod.CONSTRAINED_SHIFTING, SamplingApproach.DEFAULT, IterationMethod.CPP, single_init = True, using_objects = True
                ),
                # RandeerExperiment(
                #     'default shifting (c++), iteration in c++, multiple inits',
                #     RANDEER_LIBRARY_PATH, SamplingMethod.SHIFTING, SamplingApproach.DEFAULT, IterationMethod.CPP, single_init = False, using_objects = True
                # )
            ),
            n_repetitions = 10,
            seeds = (17, 19, 21)
        )
    else:
        evaluator = Evaluator(
            experiments = (
                PythonExperiment(
                    default_looping := 'default looping (python)',
                    SamplingMethod.LOOPING, SamplingApproach.DEFAULT
                ),
                # PythonExperiment(
                #     'default shifting (python)',
                #     SamplingMethod.SHIFTING, SamplingApproach.DEFAULT
                # ),
                PythonExperiment(
                    default_shifting := 'default shifting with single init (python)',
                    SamplingMethod.SHIFTING, SamplingApproach.DEFAULT, single_init = True
                ),
                RandeerExperiment(
                    default_shifting_cpp := 'default constrained shifting (c++), iteration in c++, single init',
                    RANDEER_LIBRARY_PATH, SamplingMethod.CONSTRAINED_SHIFTING, SamplingApproach.DEFAULT, IterationMethod.CPP, single_init = True, using_objects = True
                ),
                # RandeerExperiment(
                #     'default looping (c++), iteration in python',
                #     RANDEER_LIBRARY_PATH, SamplingMethod.LOOPING, SamplingApproach.DEFAULT, IterationMethod.PYTHON, single_init = True, using_objects = False
                # ),
                # RandeerExperiment(
                #     'default looping (c++), iteration in c++',
                #     RANDEER_LIBRARY_PATH, SamplingMethod.LOOPING, SamplingApproach.DEFAULT, IterationMethod.CPP, single_init = False, using_objects = False
                # ),
                # RandeerExperiment(
                #     'default looping (c++), iteration in c++, single init',
                #     RANDEER_LIBRARY_PATH, SamplingMethod.LOOPING, SamplingApproach.DEFAULT, IterationMethod.CPP, single_init = True, using_objects = True
                # ),
                # RandeerExperiment(
                #     'default looping (c++), iteration in c++, single init, no intermediate objects',
                #     RANDEER_LIBRARY_PATH, SamplingMethod.LOOPING, SamplingApproach.DEFAULT, IterationMethod.CPP, single_init = True, using_objects = False
                # )
            ),
            n_repetitions = 10,
            seeds = (17, 19, 21)
        )

    # experiment = PythonExperiment('default looping', SamplingMethod.LOOPING, SamplingApproach.DEFAULT)
    # print(experiment.run(10000, 10, 20, (11, 12), 10, (17, 19, 21, 14)))
    # experiment = RandeerExperiment('default looping with reusable object', RANDEER_LIBRARY_PATH, SamplingMethod.LOOPING, SamplingApproach.DEFAULT, IterationMethod.CPP, single_init = True, using_objects = True)
    # print(experiment.run(10000, 10, 20, (11, 12), 10, (17, 19, 21, 14)))

    # evaluator.evaluate(n = 100000, min_ = 10, max_ = 20, excluded = (11, 12))
    df, plot = evaluator.evaluate(n = 1000, grid = grid, unit = Unit.MILLISECOND)

    df = compare_distributions(df, default_looping, default_shifting)
    mean, std = compare_execution_time(df, default_shifting, default_shifting_cpp)

    print(f'\n\nexecution time difference between "{default_shifting}" and "{default_shifting_cpp}": {mean=} {std=}\n\n')

    # numerator = df[(default_looping, 'mean')].sub(df[(default_shifting, 'mean')])
    # denominator = df[(default_looping, 'std')].pow(2).divide(df[(default_looping, 'sample size')]).add(
    #     df[(default_shifting, 'std')].pow(2).divide(df[(default_shifting, 'sample size')])
    # ).pow(0.5)

    # df['t-score'] = numerator.divide(denominator)

    # # df.apply(lambda x: print(x.loc[[default_looping]]), axis = 1)
    # df['p-value'] = p_value = df.apply(lambda x: scipy.stats.t.sf(abs(x.at['t-score'].iloc[0]), df = int(x.loc[[[default_looping, 'sample size']]].iloc[0]) - 1) * 2, axis = 1)
    # # print(p_values)

    # df['is significant'] = p_value.le(0.05)

    # shifting_mul = df[(default_shifting, 'mean')].divide(df[(default_shifting_cpp, 'mean')])

    # print(shifting_mul.mean(), shifting_mul.std())

    print(df)

    df.to_csv('assets/evaluation-results.tsv', sep='\t', index = False, float_format = '{:.10f}'.format)
    plot.savefig('assets/evaluation-results.png')

    # randeer = RandeerAdapter(RANDEER_LIBRARY_PATH)
    # evaluator = Evaluator()

    # min_ = 10
    # max_ = 20
    # excluded = (11, 12, 13, 14, 15, 16, 17, 18, 19)
    # n = 100000

    # randomizer_id = 17
    # seed = 17

    # for seed_ in tuple(int(str_seed.strip()) for str_seed in seed.split(',')):

    #     randeer.seed(seed_)

    #     # for _ in range(10):
    #     #     print(randeer.sample_by_looping(100, 150, (110, 130)))
    #     #     print(randeer.sample_by_looping_lcg(100, 150, (110, 130)))

    #     # randeer.init(randomizer_id, seed, RandomizerType.DEFAULT_LOOPING)
    #     # randeer.init_in_interval_excluding_task(randomizer_id, min_, max_, excluded)

    #     print('Default')

    #     evaluator.evaluate(lambda: randeer.sample_default_by_looping_python(min_, max_, excluded), n, 'looping in python, generation in python')
    #     evaluator.evaluate(lambda: randeer.sample_default_by_looping(min_, max_, excluded), n, 'looping in python, generation in c++')
    #     evaluator.evaluate(lambda: randeer.sample_default_n_by_looping_with_init(n, min_, max_, excluded), 1, 'looping in c++, generation in c++ with init')
    #     evaluator.evaluate(lambda: randeer.sample_default_n_by_looping_without_init(n, min_, max_, excluded), 1, 'looping in c++, generation in c++ without init')

    #     print('Default using objects')

    #     evaluator.evaluate(lambda: randeer.sample_default_by_looping_using_objects(min_, max_, excluded), n, 'looping in python, generation in c++')
    #     evaluator.evaluate(lambda: randeer.sample_default_n_by_looping_with_init_using_objects(n, min_, max_, excluded), 1, 'looping in c++, generation in c++ with init')
    #     evaluator.evaluate(lambda: randeer.sample_default_n_by_looping_without_init_using_objects(n, min_, max_, excluded), 1, 'looping in c++, generation in c++ without init')

    #     print('LCG')

    #     evaluator.evaluate(lambda: randeer.sample_lcg_by_looping_python(min_, max_, excluded), n, 'looping in python, generation in python')
    #     evaluator.evaluate(lambda: randeer.sample_lcg_by_looping(min_, max_, excluded), n, 'looping in python, generation in c++')
    #     evaluator.evaluate(lambda: randeer.sample_lcg_n_by_looping_with_init(n, min_, max_, excluded), 1, 'looping in c++, generation in c++ with init')
    #     evaluator.evaluate(lambda: randeer.sample_lcg_n_by_looping_without_init(n, min_, max_, excluded), 1, 'looping in c++, generation in c++ without init')

    #     # evaluator.evaluate(lambda: randeer.sample_by_looping_randomizer(min_, max_, excluded), n, 'looping randomizer in python, generation in c++')
    #     # evaluator.evaluate(lambda: randeer.next(randomizer_id), n, 'looping contextualized randomizer in python, generation in c++')
    #     # evaluator.evaluate(lambda: randeer.sample_by_looping_lcg(min_, max_, excluded), n, 'looping in python, generation in c++ using custom function')

    #     # for _ in range(100):
    #     #     print(randeer.sample_by_looping(10, 20, (12, 13)))


if __name__ == '__main__':
    main()
