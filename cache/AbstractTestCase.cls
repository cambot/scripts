Class Tests.AbstractTestCase Extends %UnitTest.TestCase
{

/// Wrapper plus some.
Method AssertEquals(expected, actual, description = "")
{
	if (expected = actual) {
		do $$$AssertSuccess("AssertEquals "_description)
	}
	else {
		do $$$AssertFailure("AssertEquals "_description_"  Expected: "_expected_" Actual: "_actual)
	}
}

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

/// sample usage: <br>
/// do ..AssertEqualsWithinDelta($p(dataObj.LastPWChange,",",2), $p(currentDateTime,",",2), 1, "Property should be set to current time.")
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

/// Verify lists contain the same items, but where order does not matter
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

}
