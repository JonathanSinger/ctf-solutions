#!/bin/bash

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