Class Tests.Report Extends %RegisteredObject
{

/// Parameters:
/// <ul>
///  <li>header: header text to include in the report</li>
///  <li>runId (optional): ID of the unit test run to generate the report for.  Default is to use the most recent id.</li>
/// </ul>
ClassMethod Run(header As %String = "", runId As %Integer = "")
{
	do ..GatherTestMetrics(.data, runId)
	do ..DisplaySummary(.data, header)
}

/// Compile all the test data metrics.  If an ID is not provided, then the most recent
///  run id will be used (and returned).
ClassMethod GatherTestMetrics(data, id As %Integer = "")
{
	kill data
	set:(id > $get(^UnitTest.Result)) id = $get(^UnitTest.Result)
	set:(id = "") id = ^UnitTest.Result
	set data("runId") = id
	set data("totalTime") = $listget(^UnitTest.Result(id), 2)
	set (count,failCount,errorCount) = 0
	set progressBar = ""
	set package = ""
	for {
		set package = $order(^UnitTest.Result(id, package))
		quit:(package = "")
		set testClass = ""
		for {
			set testClass = $order(^UnitTest.Result(id, package, testClass))
			quit:(testClass = "")
			set exception = $listget(^UnitTest.Result(id, package, testClass), 4)
			if (exception [ "ERROR") {
				set progressBar = progressBar_"E"
				set errorCount = errorCount + 1
				set data("FailedTests", $increment(data("FailedTests"))) = $lb("E", package, testClass, "All", exception)
			}
			set testCase = ""
			for {
				set testCase = $order(^UnitTest.Result(id, package, testClass, testCase))
				quit:(testCase = "")
				set count = count + 1
				if ($listget(^UnitTest.Result(id, package, testClass, testCase),1) = 1) {
					set progressBar = progressBar _ "."
				}
				else {
					set exception = $listget(^UnitTest.Result(id, package, testClass, testCase), 4)
					if (exception [ "ERROR") {
						set progressBar = progressBar _ "E"
						set errorCount = errorCount + 1
						set data("FailedTests", $increment(data("FailedTests"))) = $lb("E", package, testClass, testCase, exception)
					}
					else {
						set progressBar = progressBar _ "F"
						set failCount = failCount + 1
						set index = $increment(data("FailedTests"))
						set data("FailedTests", index) = $lb("F", package, testClass, testCase)
						set assertIndex = $order(^UnitTest.Result(id, package, testClass, testCase, ""))
						set x = 0
						while (assertIndex '= "") {
							set assertRecord = ^UnitTest.Result(id, package, testClass, testCase, assertIndex)
							if ($lg(assertRecord,1) = 0) {
								set failMessage = $listget(assertRecord, 2)_" failed: "_$listget(assertRecord, 3)
								set x = x + 1
								set data("FailedTests", index, x) = failMessage
							}
							set assertIndex = $order(^UnitTest.Result(id, package, testClass, testCase, assertIndex))
						}
						kill x
					}
				}
			}
		}
	}
	set data("count") = count
	set data("errorCount") = errorCount
	set data("failCount") = failCount
	set data("progressBar") = progressBar
	set data("allTestsPass") = $data(data("FailedTests"))=0
}

/// Given data collected by GatherTestMetrics(), display a formatted report of
///  the test run.  Optionally provide an output stream if you do not want to
///  write directly to the terminal.
ClassMethod DisplaySummary(data, header As %String = "", ByRef outStream As %Stream.FileBinary = "")
{
	set report = ""
	do ..FormatSummary(.data, header, .report)
	for i=1:1:report {
		do ..Write(report(i), outStream)
	}
}

/// Formats the report data into a textual report in memory.
ClassMethod FormatSummary(data, header As %String = "", report = "")
{
	kill report
	set report($i(report)) = ""
	set report($i(report)) = ""
	set report($i(report)) = " -- "_header_" Summary -- "
	set report($i(report)) = ""
	set report($i(report)) = "Run ID: "_$get(data("runId"))
	set progressBar = $get(data("progressBar"))
	while ($length(progressBar)>0) {
		set report($i(report)) = $extract(progressBar,1, 80)
		set progressBar = $extract(progressBar, 81, *)
	}
	set report($i(report)) = "Number of tests: "_$get(data("count"))
	set:($get(data("errorCount"))) report($i(report)) = "Number of Errored Tests: "_$get(data("errorCount"))
	set:($get(data("failedCount"))) report($i(report)) = "Number of Failed Tests: "_$get(data("failCount"))
	set report($i(report)) = ""
	set report($i(report)) = $select($get(data("allTestsPass"))=1:"Success!", 1:"Fail :(")
	if ($get(data("FailedTests"))) {
		set report($i(report)) = "Failed tests: "_$get(data("FailedTests"))
		set report($i(report)) = ""
		for i=1:1:data("FailedTests") {
			set record = data("FailedTests", i)
			set status = $lg(record, 1)
			if (status = "E") {
				set report($i(report)) = "  "_$lg(record, 3)_"  "_$lg(record, 4)
				set report($i(report)) = "     "_$lg(record, 5)
			}
			if (status = "F") {
				set report($i(report)) = "  "_$lg(record, 3)_"  "_$lg(record, 4)
				set assertIndex = $order(data("FailedTests", i, ""))
				while (assertIndex '= "") {
					set report($i(report)) = "     "_data("FailedTests", i, assertIndex)
					set assertIndex = $order(data("FailedTests", i, assertIndex))
				}
				set report($i(report)) = ""
			}
		}
	}
	set report($i(report)) = "Total Time: "_$get(data("totalTime"))_" seconds"
}

/// Write out line to device.
ClassMethod Write(line As %String, ByRef outStream As %Stream.FileBinary = "")
{
	if (outStream '= "") {
		do outStream.WriteLine(line)
	}
	else {
		write !, line
	}
}

}
