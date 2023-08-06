README
======

Plinq is a library for python, implementing the Language Integrated Query (LINQ) from the C# language.
Of course it is not a full port of the feature, it is only working with in memory iterable objects, including:

-  lists
-  sets
-  dictionaries
-  files
-  xml elements
-  generators
-  and every class which implements the iterable/iterator protocol (
   \_\_iter\_\_ and \_\_next\_\_)

Plinq tries to mimic the Enumerable<T> interface from C# as much as possible.

-  It has the same method names, wherever possible, and the same
   parameters too

Plinq operators are lazy, meaning calling one, will not start the actual work.
It will only happen, when the iteration over the returned object is started.

Plinq operators returning a new Linq object, so operator calls can be chained into a fluent API like call.

How do I get set up?
~~~~~~~~~~~~~~~~~~~~

-  Summary of set up

   -  There are several ways to set up plinq:

      -  The simplest way is to invoke pip install plinq

      -  You can also check out the repository, and add the path to it to your python path

      - Combining the two above steps, you can check out the repository, create a distribution package
        by executing the setup.py file, and then install that package with pip

   -  After these steps you can simply import plinq and start using the library

-  Configuration

   -  No additional configuration is needed

-  Dependencies

   -  plinq has no external dependencies. The only requirement is to have at least Python 3.5.2

-  How to run tests

   -  After you have checked out the repository,
      you can run the python unit tests by invoking the following command from the root directory of the repository:

      -  python -m unittest discover test/

Who do I talk to?
~~~~~~~~~~~~~~~~~

-  Repo owner and admin

   -  Heszele Rudolf heszele@gmail.com

Example usage
~~~~~~~~~~~~~

::

    import plinq
    linq = plinq.from_iterable([1, 2, 3, 4, 5]).where(lambda item, index: item % 2 == 0).select(lambda item, index: item ** 2)
    for item in linq:
        print(item)

This will result in the following output:

::

    4
    16

Version History
~~~~~~~~~~~~~~~
-  0.1: Never released externally
-  0.2: Initial release on pypi. Includes almost all the linq operators, except then_by and then_by_descending
-  0.3: Added then_by and then_by_descending linq operarors, and max_item and min_item operators.
