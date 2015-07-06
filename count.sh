input_list=`ls log`
for file in $input_list
do
	num=`cat log/$file | wc -l`
	word_num=`grep 'word=' log/$file | wc -l`
	echo $file: $word_num / $num
done
