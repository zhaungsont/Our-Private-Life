<!接收處理 - >

<?php  

   $number = $_POST["number"];

   echo "數字與國字對照 <BR><BR>";

   echo "數字 $number <==>";

   switch ($number) {

             case 0:

                 echo "零 <BR>";

                 break;

             case 1:

                 echo "壹 <BR>";

                 break;

             case 2:

                 echo "貳 <BR>";

                 break;

             case 3:

                 echo "叁 <BR>";

                 break;

             case 4:

                 echo "肆 <BR>";

                 break;

             case 5:

                 echo "伍 <BR>";

                 break;

             case 6:

                 echo "陸 <BR>";

                 break;

             case 7:

                 echo "柒 <BR>";

                 break;

             case 8:

                 echo "捌 <BR>";

                 break;

             case 9:

                 echo "玖 <BR>";

                 break;

    }

    echo "謝謝 !! 歡迎再來 <BR>";

?>