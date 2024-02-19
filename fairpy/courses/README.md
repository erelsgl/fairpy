# Fair course allocation algorithms

*DEPRECATED*: the contents of this folder has been moved to the [fairpyx](https://github.com/ariel-research/fairpyx) library.

This folder contains algorithms for an important special case of item allocation: [course allocation](https://en.wikipedia.org/wiki/Course_allocation) --- allocating course-seats among students. This setting has the following characteristics:

* Usually there is a small number of different item-types (courses), but each item-type has many copies. Therefore, the input must record the number of copies of each item.
* Each student must receive at most a single copy of each item.  Usually there are additional constraints, such as: each student must receive exactly 6 courses overall. The input must record these constraints too.

