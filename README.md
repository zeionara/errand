# errand

<p align="center">
    <img src="assets/images/logo.png"/>
</p>

Evaluation of random number generation functions performance

## Create environment

Use requirements file to create a `conda` environment:

```sh
conda env create -f environment.yml
```

## Run evaluation

Execute preliminary tests:

```sh
python -m errand randomize
```

## Architecture

The following UML class diagram describes structure of the package:

```mermaid
classDiagram
direction LR

Evaluator "1" -- "0..n" Experiment
Evaluator -- Unit
Evaluator -- ParameterGrid
Evaluator -- Utils

ParameterGrid -- Parameter

Experiment -- Unit
Experiment <|-- PythonExperiment
Experiment <|-- RandeerExperiment

SamplingApproach -- PythonExperiment
SamplingMethod -- PythonExperiment

SamplingApproach -- RandeerExperiment
SamplingMethod -- RandeerExperiment

Sampler <|-- PythonSampler
Sampler <|-- RandeerSampler

PythonSampler *-- ShiftingContext
PythonExperiment *-- PythonSampler
RandeerExperiment *-- PythonSampler

RandeerSampler -- RandomizerType
RandeerSampler -- IterationMethod

class Evaluator {
    +Experiment[] experiments
    +int n_repetitions
    +int[] seeds
    +visualize(int[] x, float[] y, str label, Unit unit, str xlabels)
    +evaluate(int n, ParameterGrid grid, Unit unit)
}

class ParameterGrid {
    +Parameter[] parameters
    +from_range(int[] mins, int[] maxs, int[][] excluded)
    +from_boundaries((int, int, float)[] boundaries, bool continuous_excluded_interval)
}

class Parameter {
    +int min
    +int max
    +int[] excluded
    +int id
}

class Experiment {
    +Sampler sampler
    +string label
    +run(int n, int min, int max, int[] excluded, int nRepetitions, int[] seeds, Unit unit)
    -run_for_one_seed(int n_repetitions, callable run, int seed, Unit unit)
    -sample(int n, int min, int max, int[] excluded)*
}

class Unit {
    <<enum>>
    SECOND
    MILLISECOND
    MICROSECOND
    + int scaling_coefficient
}

class PythonExperiment {
    +SamplingMethod sampling_method
    +SamplingApproach sampling_approach
    +bool single_init
    -sample(int n, int min, int max, int[] excluded)
}

class SamplingApproach {
    <<enum>>
    DEFAULT
    LCG
}

class SamplingMethod {
    <<enum>>
    LOOPING
    SHIFTING
    CONSTRAINED_SHIFTING
}

class Sampler {
    +sample(int n, int min, int max, int[] excluded)
    +seed(int seed)*
    -get_sampling_function()*
}

class PythonSampler {
    +int lcg_multiplier$
    +int lcg_increment$
    +int lcg_modulus$

    -int last_lcg_state
    -ShiftingContext context

    +seed(int seed)

    -lcg_randint(int modulus)
    -sample_default_by_looping(int min, int max, int[] excluded)
    -sample_lcg_by_looping(int min, int max, int[] excluded)
    -sample_default_by_shifting(int min, int max, int[] excluded)
    -sample_default_by_shifting_using_shared_context(int min, int max, int[] excluded)

    -get_sampling_function()
}

class ShiftingContext {
    +int max_shifted
    +int smallest_excluded_value
    +int largest_excluded_value
    +int n_excluded
}

class RandeerExperiment {
    +SamplingMethod sampling_method
    +SamplingApproach sampling_approach
    +bool single_init
    +bool using_objects
    -sample(int n, int min, int max, int[] excluded)
}

class RandomizerType {
    <<enum>>
    DEFAULT_LOOPING
    JAVA_LOOPING
}

class IterationMethod {
    <<enum>>
    PYTHON
    CPP
}

class RandeerSampler {
    -StaticLibrary lib
    +init(int id, int seed, RandomizerType type)
    +init_in_interval_excluding_task(int id, int min, int max, int[] excluded)
    +next(int id)

    +sample_default_by_looping(int min, int max, int[] excluded)
    +sample_n_default_by_looping_without_init(int n, int min, int max, int[] excluded)
    +sample_n_default_by_looping_with_init(int n, int min, int max, int[] excluded)
    
    +sample_default_by_looping_using_objects(int min, int max, int[] excluded)
    +sample_n_default_by_looping_without_init_using_objects(int n, int min, int max, int[] excluded)
    +sample_n_default_by_looping_with_init_using_objects(int n, int min, int max, int[] excluded)

    +sample_default_by_shifting_using_objects(int min, int max, int[] excluded)
    +sample_n_default_by_shifting_without_init_using_objects(int n, int min, int max, int[] excluded)
    +sample_n_default_by_shifting_with_init_using_objects(int n, int min, int max, int[] excluded)

    +sample_default_by_constrained_shifting_using_objects(int min, int max, int[] excluded)
    +sample_n_default_by_constrained_shifting_without_init_using_objects(int n, int min, int max, int[] excluded)
    +sample_n_default_by_constrained_shifting_with_init_using_objects(int n, int min, int max, int[] excluded)

    +sample_lcg_by_looping(int min, int max, int[] excluded)
    +sample_n_lcg_by_looping_without_init(int n, int min, int max, int[] excluded)
    +sample_n_lcg_by_looping_with_init(int n, int min, int max, int[] excluded)

    +sample(int n, int min, int max, int[] excluded)
    +seed(int seed)*

    -get_sampling_function()*
}

class Utils {
    +encode_list(T[] items): T*
    +compare_execution_time(DataFrame df, string lhs_label, string rhs_label)
    +compare_distributions(DataFrame df, string lhs_label, string rhs_label, float alpha)
}
```

The diagram below demonstrates a shorter version of the same diagram without sampling classes:

```mermaid
classDiagram
direction LR

Evaluator "1" -- "0..n" Experiment
Evaluator -- Unit
Evaluator -- ParameterGrid
Evaluator -- Utils

ParameterGrid -- Parameter

Experiment -- Unit
Experiment <|-- PythonExperiment
Experiment <|-- RandeerExperiment

SamplingApproach -- PythonExperiment
SamplingMethod -- PythonExperiment

SamplingApproach -- RandeerExperiment
SamplingMethod -- RandeerExperiment

class Evaluator {
    +Experiment[] experiments
    +int n_repetitions
    +int[] seeds
    +visualize(int[] x, float[] y, str label, Unit unit, str xlabels)
    +evaluate(int n, ParameterGrid grid, Unit unit)
}

class ParameterGrid {
    +Parameter[] parameters
    +from_range(int[] mins, int[] maxs, int[][] excluded)
    +from_boundaries((int, int, float)[] boundaries, bool continuous_excluded_interval)
}

class Parameter {
    +int min
    +int max
    +int[] excluded
    +int id
}

class Experiment {
    +Sampler sampler
    +string label
    +run(int n, int min, int max, int[] excluded, int nRepetitions, int[] seeds, Unit unit)
    -run_for_one_seed(int n_repetitions, callable run, int seed, Unit unit)
    -sample(int n, int min, int max, int[] excluded)*
}

class Unit {
    <<enum>>
    SECOND
    MILLISECOND
    MICROSECOND
    + int scaling_coefficient
}

class PythonExperiment {
    +SamplingMethod sampling_method
    +SamplingApproach sampling_approach
    +bool single_init
    -sample(int n, int min, int max, int[] excluded)
}

class SamplingApproach {
    <<enum>>
    DEFAULT
    LCG
}

class SamplingMethod {
    <<enum>>
    LOOPING
    SHIFTING
    CONSTRAINED_SHIFTING
}

class Sampler {
    +sample(int n, int min, int max, int[] excluded)
    +seed(int seed)*
    -get_sampling_function()*
}

class RandeerExperiment {
    +SamplingMethod sampling_method
    +SamplingApproach sampling_approach
    +bool single_init
    +bool using_objects
    -sample(int n, int min, int max, int[] excluded)
}

class Utils {
    +encode_list(T[] items): T*
    +compare_execution_time(DataFrame df, string lhs_label, string rhs_label)
    +compare_distributions(DataFrame df, string lhs_label, string rhs_label, float alpha)
}
```

Conversely, the following diagram contains all classes related to sampling:

```mermaid
classDiagram
direction LR

Sampler <|-- PythonSampler
Sampler <|-- RandeerSampler

PythonSampler *-- ShiftingContext

RandeerSampler -- RandomizerType
RandeerSampler -- IterationMethod

class Sampler {
    +sample(int n, int min, int max, int[] excluded)
    +seed(int seed)*
    -get_sampling_function()*
}

class PythonSampler {
    +int lcg_multiplier$
    +int lcg_increment$
    +int lcg_modulus$

    -int last_lcg_state
    -ShiftingContext context

    +seed(int seed)

    -lcg_randint(int modulus)
    -sample_default_by_looping(int min, int max, int[] excluded)
    -sample_lcg_by_looping(int min, int max, int[] excluded)
    -sample_default_by_shifting(int min, int max, int[] excluded)
    -sample_default_by_shifting_using_shared_context(int min, int max, int[] excluded)

    -get_sampling_function()
}

class ShiftingContext {
    +int max_shifted
    +int smallest_excluded_value
    +int largest_excluded_value
    +int n_excluded
}

class RandomizerType {
    <<enum>>
    DEFAULT_LOOPING
    JAVA_LOOPING
}

class IterationMethod {
    <<enum>>
    PYTHON
    CPP
}

class RandeerSampler {
    -StaticLibrary lib
    +init(int id, int seed, RandomizerType type)
    +init_in_interval_excluding_task(int id, int min, int max, int[] excluded)
    +next(int id)

    +sample_default_by_looping(int min, int max, int[] excluded)
    +sample_n_default_by_looping_without_init(int n, int min, int max, int[] excluded)
    +sample_n_default_by_looping_with_init(int n, int min, int max, int[] excluded)
    
    +sample_default_by_looping_using_objects(int min, int max, int[] excluded)
    +sample_n_default_by_looping_without_init_using_objects(int n, int min, int max, int[] excluded)
    +sample_n_default_by_looping_with_init_using_objects(int n, int min, int max, int[] excluded)

    +sample_default_by_shifting_using_objects(int min, int max, int[] excluded)
    +sample_n_default_by_shifting_without_init_using_objects(int n, int min, int max, int[] excluded)
    +sample_n_default_by_shifting_with_init_using_objects(int n, int min, int max, int[] excluded)

    +sample_default_by_constrained_shifting_using_objects(int min, int max, int[] excluded)
    +sample_n_default_by_constrained_shifting_without_init_using_objects(int n, int min, int max, int[] excluded)
    +sample_n_default_by_constrained_shifting_with_init_using_objects(int n, int min, int max, int[] excluded)

    +sample_lcg_by_looping(int min, int max, int[] excluded)
    +sample_n_lcg_by_looping_without_init(int n, int min, int max, int[] excluded)
    +sample_n_lcg_by_looping_with_init(int n, int min, int max, int[] excluded)

    +sample(int n, int min, int max, int[] excluded)
    +seed(int seed)*

    -get_sampling_function()*
}
```
