#!/bin/bash
##Simply run in the same folder as the challenge
##The final output will be indicated so that you can fix the math
##Then run the PHP file one last time once fixed

sed -i 's/<php //' gaychal.txt
mv gaychal.txt gaychal0.php

i="0"
k="eval"

while [ $k = 'eval' ]; do
sed -i 's/eval/<?php\necho/' gaychal$i.php
echo " ?>" >> gaychal$i.php
j=$((i+1))
php -f gaychal$i.php > gaychal$j.php
k=$(head -c4 gaychal$j.php)
echo $k
i=$((i+1))
done

echo "Fix File: "$j
