#!/bin/bash
##Simply run in the same folder as the challenge
##The final output will be indicated so that you can fix the math
##Then run the PHP file one last time once fixed

sed -i 's/<php //' gaychal.txt
mv gaychal.txt gaychal0.php

i="0"
k="eval"

while [ $k = 'eval' ]; do
echo gaychal$i.php: $k
sed -i 's/eval/<?php echo/' gaychal$i.php
echo " ?>" >> gaychal$i.php
j=$((i+1))
php -f gaychal$i.php > gaychal$j.php
k=$(head -c4 gaychal$j.php)
i=$((i+1))
done

echo gaychal$j.php: $k
echo "Fixing File: "gaychal$j.php

sed -i 's/5+5=9/5+5=10/' gaychal$j.php
sed -i 's/echo/<?php echo/' gaychal$j.php
echo " ?>" >> gaychal$j.php

echo "-----A WINRAR IS YOU!-----"

php -f gaychal$j.php
