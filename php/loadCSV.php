<?php

function loadCSVFile($fileName) {
	if ( ($file = fopen($fileName, 'r')) !== FALSE ) {
		$row = 1;
		$values = array();
		$fields = null;
		while (($dataRow = fgetcsv($file, 4096)) !== FALSE ) {
			if ( $fields === null ) {
				$fields = $dataRow;
				continue;
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

