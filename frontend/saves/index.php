<?php
	foreach(glob($log_directory.'./*.html') as $file) {
    		echo "<li><a href=".$file.">".$file."</a></li>";
	}


?>
