<?php

function loadCSVFile($fileName) {
	if ( ($file = fopen($fileName, 'r')) !== FALSE ) {
		$emptyRow = array(null);

		$row = 1;
		$values = array();
		$fields = null;

		while (($dataRow = fgetcsv($file, 4096)) !== FALSE ) {
			if ( $fields === null ) {
				$fields = $dataRow;
				continue;
			}
			if ( $dataRow === $emptyRow ) {
				continue;  // Skip empty rows
			}
			foreach ($dataRow as $key=>$value) {
				$values[$row][$fields[$key]] = $value;
			}
			$row++;
		}
		fclose($file);
		return $values;
	}
	else {
		echo "<p>Error. File not found: $fileName</p>";
		return FALSE;
	}
}

