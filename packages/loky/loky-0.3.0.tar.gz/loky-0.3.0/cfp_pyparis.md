## Title: Robustifying `concurrent.futures`


### Plan

* `concurrent.futures` paradigm
* Issues with this library: overhead and deadlocks
* `Loky` and improvment

#### Abstract: 
(*<300 characters*)

This talk presents in details `concurrent.futures` and its drawbacks. It then introduce [`loky`](https://github.com/tomMoral/loky), a library that robustifies
`concurrent.futures.ProcessPoolExecutor`, and some of the major design choices.

#### Description


The `concurrent.futures` module offers an easy to use API to parallelize code execution in python, using `threading` or `multiprocessing` modules. We will begin our talk by presenting this API and the differences between `Thread` and `Process`.

For `Process` backed executions, useful for pure python parallelization, several issues can reduce the performance. Spwaning new workers for each execution can create a large overhead, but maintaining the pool of worker across the program can become quickly bothersome. We will describe several of the pitfall that can make using `concurrent.futures` instable.

Finally, we will inttroduce [`loky`](https://github.com/tomMoral/loky), a library providing a robust, reusable pool of workers, handled internaly. It uses a
customized implementation of `ProcessPoolExecutor` from `concurrent.futures`. We will describe its main features and the major technical design choice that helped making it more robust.

#### Note

We wish to present in details `concurrent.futures` and how to use it and, from there, explain why their is a need for reusable version of the `ProcessPoolExecutor`, introduced in [`loky`](https://github.com/tomMoral/loky). The talk will be as followed:  
  * Introduction to `concurrent.futures` and its API. (10min)
  * Differences between `Thread` and `Process`, to explain some situations when to use each. (5min)
  * The issues with `ProcessPoolExecutor`, more specifically, the overhead of spawning a new `executor` and some of the common deadlock or interpreter freeze. (10min)
  * Introduce [`loky`](https://github.com/tomMoral/loky) and its design choice. We will notably cover some possibilities of deadlock and how to test it (15min).

This talk is aimed at intermediate practitioner that wish to know more about `concurrent.futures` under the hood and also more advance ones that will be more interested in the end of the talk, with the technical discussion over multiprocessing systems.

#### Bio

I am a PhD student at Centre de Mathématiques et de leurs applications (CMLA), ENS Paris-Saclay, since Fall 2014. My PhD subject is *Automatic feature extraction for physiological time series*. My research interests touch several areas of Machine Learning, Signal Processing and High-Dimensional Statistics. In particular, I am working on Convolutional Dictionary Learning, studying both their computational aspects and their possible application to pattern analysis. I am also studying on theoretical properties of learned optimization algorithms and their links to deep learning.

I have been experimenting with different tools for parallel and distributed computation, from standard libraries like python multiprocessing to more advance tools such as CUDA or openMPI. I have been working on [`loky`](https://github.com/tomMoral/loky) and the robustification of `concurrent.futures` for the past 2 years in collaboration with Olivier Grisel.