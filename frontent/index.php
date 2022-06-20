<!DOCTYPE html>
<!-- Nothing important in this html page. Its all HTML and does not have any secret information.
Thus, if you are trying to find backdoors or do some malicious shit, go fuck yourself. --!>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="utf-8">
<title>Desmos Picture Graph Generator</title>
<style>
#maincontent{
	margin:16px;
	justify-content:center;
}
#centerer{
	max-width:1500px;
	margin:auto;
}
img {
   max-width:100%;
   height:auto;
   max-height:100%;
}

</style>

</head>
<body>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

<div id="maincontent">
<div id="centerer">
<nav class="navbar navbar-expand-lg navbar-light"  style="background-color: #e3f2fd;">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Picture to Desmos Graph</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
  </div>
</nav>
&nbsp
<h1 id="minecraft-cultureland-plugin">Picture to Desmos Graph</h1>
<h3 id="-">Convert your picture to Desmos graph!</h3>
<img class="intro" src="./intro.png">

<?php
	function post_data(){
		$url = "http://220.149.231.241:5001/pic";
		$file = $_FILES['image'];
		$allowedExts = array("gif", "jpeg", "jpg", "png");

		$error = $file["error"];
    		$name = $file["name"];
    		$type = $file["type"];
    		$size = $file["size"];
    		$tmp_name = $file["tmp_name"];
   
    		if ( $error > 0 ) {
        			echo "Error: " . $error . "<br>";
    		}
    		else {
        		$temp = explode(".", $name);
        		// print_r($temp);
        		$extension = end($temp);
        		//echo $extension;
       
        		if (!((($size/1024/1024) < 2.) && in_array($extension, $allowedExts))) {
				echo "<div class=\"alert alert-danger\" role=\"alert\"> Image must be .png, .jpg, .jpeg less than 2MB!</div>";
        		}
    		}

if (function_exists('curl_file_create')) { 
                        $cFile = curl_file_create($_FILES['image']['tmp_name']);
                      } else {
                        $cFile = '@' . realpath($_FILES['image']['tmp_name']);
                    }
                    $post = array('image'=> $cFile);
                    $ch = curl_init();
                    curl_setopt($ch, CURLOPT_URL,"http://220.149.231.241:5001/pic");
                    curl_setopt($ch, CURLOPT_POST,1);
                    curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);
                    curl_setopt($ch, CURLOPT_POSTFIELDS, $post);
                    $response=curl_exec ($ch);
		    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
                    curl_close ($ch);
		
		if ($http_code == 200){
			$json_result = json_decode($response, true);
			echo "<div class=\"alert alert-success\" role=\"alert\">Success! Please wait...</div>\n";
			$js_result = $json_result["js_result"];
			
			echo "<h4> Graph preview (might take some time to load) </h4>\n";
			echo $js_result;
			echo "<h4> Copy and paste following functions to Desmos.com </h4>\n";
			$text_result = $json_result["text_result"];
			echo $text_result;	
		}
		else{
			echo "<div class=\"alert alert-danger\" role=\"alert\">".$response."</div>";
		}
	}
?>

<?php
	if(isset($_POST['submit'])){
		post_data();
	}
?>

<form action="" method="post" enctype="multipart/form-data">
	<div class="row g-3">
  		<label for="formFile" class="form-label" style="font-size: 30px">Upload Picture</label>
		<?php
			$host = '127.0.0.1'; // check connection to server. 
			$port = 5001; 
			$waitTimeoutInSeconds = 1; 
			if($fp = fsockopen($host,$port,$errCode,$errStr,$waitTimeoutInSeconds)){   
				// if api is working, then enable submit button
				echo "<div class=\"alert alert-success\" role=\"alert\">API Server is alive!</div>";
			} else {
				// if api is not working, then disable submit button
				echo "<div class=\"alert alert-danger\" role=\"alert\">API Server is down... Visit later</div>";
			} 
			fclose($fp);
		?>

  		<div class="col-auto">
         		<input class="form-control" type="file" name="image" />
  		</div>
  		<div class="col-auto">
		<?php
			$host = '127.0.0.1'; // check connection to server. 
			$port = 5001; 
			$waitTimeoutInSeconds = 1; 
			if($fp = fsockopen($host,$port,$errCode,$errStr,$waitTimeoutInSeconds)){   
				// if api is working, then enable submit button
				echo "<button type=\"submit\" name=submit value=submit class=\"btn btn-primary mb-3\">Convert!</button>";
			} else {
				// if api is not working, then disable submit button
				echo "<button type=\"submit\" name=submit value=submit class=\"btn btn-primary mb-3\" disabled=\"disabled\">Convert!</button>";
			} 
			fclose($fp);
		?>
  		</div>
	</div>
</form>

