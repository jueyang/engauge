<?php
$ch = curl_init();
curl_setopt( $ch, CURLOPT_URL, 'localhost/Engauge/Scripts/getCategories.php');
curl_setopt( $ch, CURLOPT_RETURNTRANSFER, true );
curl_setopt( $ch, CURLOPT_POST, 1 );
curl_setopt( $ch, CURLOPT_SSL_VERIFYPEER, false );
$output = curl_exec( $ch );
$errmsg = curl_error( $ch );
$info=json_decode($output,true);

curl_close( $ch );

$myfile = fopen("table_data.txt", "r") or die("Unable to open file!");
$string = fread($myfile,filesize("table_data.txt"));
fclose($myfile);
$token = strtok($string, "--");
echo $string;
if ($token !== false)
{
	echo "$token<br>";
	$categoryName = $token;
	$token2 = strtok($categoryName, " ");
	echo $categoryName;
	while ($token2 !== false)
	{	
		$catName = $catName . " " $token2; 
		echo "$token2<br>";
		foreach($output as $category){
			if($category['name'] === $catName){
				$C_ID = $category['C_ID'];
				break 3;
			}
		}


		$token2 = strtok(" ");
	}
	$token3 = strtok("--");
	while ($token3 !== false)
	{	
		$billNumber = $token3;
		$billName = strtok("--");
		$synopsis = strtok("--");
		$link = strtok("--");
		$primarySponsor = strtok("--");
		$sponsorDistrict = strtok("--");
		echo "$token3<br>";
		$ch = curl_init();
		curl_setopt( $ch, CURLOPT_URL, 'localhost/Engauge/Scripts/createBill.php');
		curl_setopt( $ch, CURLOPT_RETURNTRANSFER, true );
		curl_setopt( $ch, CURLOPT_POST, 1 );
		curl_setopt( $ch, CURLOPT_POSTFIELDS, "billNumber=$billNumber&billName=$billName&synopsis=$synopsis&link=$link&primarySponsor=$primarySponsor&categoryID=$categoryID&sponsorDistrict=$sponsorDistrict");
		curl_setopt( $ch, CURLOPT_SSL_VERIFYPEER, false );
		$output = curl_exec( $ch );
		$errmsg = curl_error( $ch );
		$info=json_decode($output,true);

		curl_close( $ch );

		$token2 = strtok(" ");
	}

	$token = strtok("--");
}
?>