# errand

<p align="center">
    <img src="assets/images/logo.png"/>
</p>

Evaluation of random number generation functions performance

There are basically two types of randomizers which are evaluated in this package. The first one allows to sample random numbers in the interval `[min, max]`, excluding elements which are passed as components of the `excluded` array using a simple loop-based algorithm:

```mermaid
stateDiagram-v2

generate: Generate number x ∈ [min, max]
return: return x

[*] --> generate

state if_x_is_bad <<choice>>

generate --> if_x_is_bad

if_x_is_bad --> generate: "x ∈ excluded"
if_x_is_bad --> return

return --> [*]
```

An alternative algorithm implements the same thing, but does it without a need to repeat the sampling procedure. The algorithm is much more complex, but essentially it is just choosing the right offset which should be added to the generated x in order to not to obtain a forbidden value. The offset is equal to the number of excluded values before the shifted value of x:

```mermaid
stateDiagram-v2

generate: Generate number x ∈ [min, max(excluded) - excluded.length]
return: return x
return_shifted: return x + excluded.length
return_complex_shifted: return x + left + 1
shift_x: left = 0, right = excluded.length - 1, middle = 0
update_middle: middle = floor(left + right / 2)
update_left: left = middle
update_right: right = middle

[*] --> generate

state if_x_is_small <<choice>>
state if_x_is_large <<choice>>
state found_bounds <<choice>>
state check_middle <<choice>>

generate --> if_x_is_small

if_x_is_small --> return: "x < min(excluded)"
if_x_is_small --> if_x_is_large: "x >= min(excluded)"

if_x_is_large --> return_shifted: "x > max(excluded) - excluded.length"
if_x_is_large --> shift_x: "x <= max(excluded) - excluded.length"

shift_x --> found_bounds

found_bounds --> update_middle: "left + 1 < right"
update_middle --> check_middle

check_middle --> update_left: "excluded[middle] - (middle + 1) < x"
check_middle --> update_right: "excluded[middle] - (middle + 1) >= x"

update_left --> found_bounds
update_right --> found_bounds

found_bounds --> return_complex_shifted: "left + 1 >= right"

return --> [*]
return_shifted --> [*]
return_complex_shifted --> [*]
```

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
RandeerExperiment *-- RandeerSampler

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
