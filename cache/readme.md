# Tests.AbstractTestCase.cls
Base Class that provides additional assertions to complement cache's built-ins.

# Tests.Report.cls
Provides a way to generate a compact report of a test run similar to other xUnit frameworks.  This is how you call it on its own:

```
do ##class(Tests.Report).Run("My custom header", 100)
```

It has three optional parameters:
* Header: defaults to "Summary".
* Run ID: defaults to the most recent run.
* outStream: Pass in a `%Stream.FileBinary` instance to redirect output.  Default: write to terminal.


Sample Output:
```
 -- My Custom Header Summary --
 
Run ID: 100
..................E..F.
Number of tests: 23
Number of Errored Tests: 1
 
Fail :(
Failed tests: 2
 
  Demo.Test.TestCase6  TestIteration2
      ERROR #5002: ObjectScript error: <COMMAND>zTestIteration2+1^Demo.Test.TestCase6.1 *Function must return a value at zLifeIteration2+13^Demo.Case6.1

  Demo.Test.TestCase9  TestIsLowPointTrue
     AssertTrue failed: Position 3,3 is a local minimum
     
Total Time: .153487 seconds
```


```
 -- My Custom Header Summary --
 
Run ID: 146
..................................
Number of tests: 34
 
Success!
Total Time: .591934 seconds
```

