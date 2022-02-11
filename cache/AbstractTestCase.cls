/// This class expands upon Cache/Iris' built in unit tests assertion library to provide 
///   more options similar to other xUnit frameworks as well as assertions for built-in
///   data structures.
Class Tests.AbstractTestCase Extends %UnitTest.TestCase
{

/// Like $$$AssertEquals, but only appends the expected and actual values when the values do not match.
Method AssertEquals(expected, actual, description = "")
{
	if (expected = actual) {
		do $$$AssertSuccess("AssertEquals "_description)
	}
	else {
		do $$$AssertFailure("AssertEquals "_description_"  Expected: "_expected_" Actual: "_actual)
	}
}

/// Like <code>$$$AssertEquals("", actualValue)</code>, but with a more readable failure message.
Method AssertIsEmptyString(actual, description = "")
{
	set message = description
	if (actual = "") {
		do $$$AssertSuccess("AssertIsEmptyString "_description)
	}
	else {
		do $$$AssertFailure("AssertIsEmptyString "_description _ " Expected: (empty string) Actual: "_actual)
	}
}

/// Asserts if the value passed is a dynamic object without any properties.
Method AssertIsEmptyObject(actual, description = "")
{
	if (actual.%IsA("%Library.DynamicObject") = 0) {
		do $$$AssertFailure("AssertIsEmptyObject "_description_" Expected object type: Dynamic Object")
	}
	set iter = actual.%GetIterator()
	set key = ""
	set x = iter.%GetNext(.key, .value)
	if (key = "") {
		do $$$AssertSuccess("AssertIsEmptyObject "_description)
	}
	else {
		do $$$AssertFailure("AssertIsEmptyObject "_description _ " Expected: (empty object)")
	}
}

/// Assert that the actual value is within a certain delta amount of an expected value.  This is useful for
///  comparing timestamp values that may differ by a few seconds due to the runtime of the code
///  under tesing.
/// <example>
/// set dataObj = ##class(My.Class).%New()
/// do ..AssertEqualsWithinDelta($piece(dataObj.DateTimeCreated, ",", 2),
///             $piece($h, ",", 2), 1, "Property should be set to current time.")
/// </example>
Method AssertEqualsWithinDelta(expected, actual, delta, description = "")
{
	set difference = $zabs(expected - actual)
	if (difference <= delta) {
		do $$$AssertSuccess("AssertEqualsWithinDelta "_description)
	}
	else {
		do $$$AssertFailure("AssertEqualsWithinDelta "_description_" Value falls outside acceptible delta (+-"_delta_")")
	}
}

/// Verify lists contain the same items, but where order does not matter.
/// <example>
/// do ..AssertListContainsSameItems($lb(3,5), $lb(5,3), "This assert should pass.")
/// </example>
Method AssertListsContainSameItems(expected, actual, description)
{
	set missingList = ""
	set extraList = ""
	set fail = 0

	for i=1:1:$listlength(expected) {
		set property = $listget(expected, i)
		if ($listfind(actual, property)=0) {
			set missingList = missingList_$lb(property), fail=1
		}
	}
	for i=1:1:$listlength(actual) {
		set property = $listget(actual, i)
		if ($listfind(expected, property)=0) {
			set extraList = extraList_$lb(property), fail=1
		}
	}
	if (fail) {
		set message = ""
		set:$listlength(missingList) message = " Missing properties: " _ $LISTTOSTRING(missingList, ", ")
		set:$listlength(extraList) message = message_" Extra properties: " _ $LISTTOSTRING(extraList, ", ")
		do $$$AssertFailure("AssertListsContainSameItems "_description _ message)
	}
	else {
		do $$$AssertSuccess("AssertListsContainSameItems " _ description)
	}
}

/// Assert that two lists are equal
/// <example>
/// do ..AssertListsAreEqual($lb(3,5), $lb(3,5), "This assert should pass.")
/// </example>
Method AssertListsAreEqual(expected, actual, description = "")
{
	if '$listvalid(expected) {
		do $$$AssertFailure("AssertListsAreEqual "_description _ " expected value is not a list")
	}
	if '$listvalid(actual) {
		do $$$AssertFailure("AssertListsAreEqual "_description _ " actual value is not a list")
	}
	if $listsame(expected, actual) {
		do $$$AssertSuccess("AssertListsAreEqual " _ description)
	}
	else {
		set message = " Expected list: " _ $LISTTOSTRING(expected, ", ")
		set message = message_" Actual list: " _ $LISTTOSTRING(actual, ", ")
		do $$$AssertFailure("AssertListsAreEqual "_description _ message)
	}
}

/// Assert that an array has a specific index
/// <example>
/// set myArray(3)="something"
/// do ..AssertArrayHasIndex(.myArray, 3, "This assert should pass.")
/// do ..AssertArrayHasIndex(.myArray, 4, "This assert should fail.")
/// </example>
Method AssertArrayHasIndex(array, index)
{
	do $$$AssertTrue($data(array(index)) > 0, "Assert array contains the index '" _ index _ "'")
}

/// Performs a shallow compare of two arrays.  Does not check for child nodes.
/// <example>
/// set firstArray(3)="something"
/// set secondArray(3)="something"
/// set thirdArray(3)="something"
/// set thirdArray(5)="else"
/// do ..AssertArraysAreEqual(.firstArray, .secondArray, "This assert should pass.")
/// do ..AssertArraysAreEqual(.firstArray, .thirdArray, "This assert should fail because thirdArray has an extra subscript.")
/// </example>
Method AssertArraysAreEqual(expected, actual, description = "")
{
	set (i, j) = ""
	for {
		set i = $o(expected(i), 1, expectedVal)
		set j = $o(actual(j), 1, actualVal)
		if (i '= j) {
			do $$$AssertFailure("Index mismatch.  Expected: "_i_" Actual: "_j)
			quit
		}
		quit:( (i="") || (j="") )
		if (expectedVal '= actualVal) {
			do $$$AssertFailure("Index ("_i_") value mismatch.  Expected: "_expectedVal_" Actual: "_actualVal)
		}
	}
	do $$$AssertSuccess("AssertArraysAreEqual " _ description)
}

}
