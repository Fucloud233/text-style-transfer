# python3 src/evaluate.py data/eval_config/7b_chat_yelp.test.0.json

while getopts p: flag

do
    case "${flag}" in
        p) path=${OPTARG};;
    esac
done

folder="output/log"
output_file="$folder/eval.out"

# echo $output_file

if [ ! -d $folder ]; then
    mkdir $folder
fi

# nohup ./myprogram > foo.out 2> foo.err < /dev/null &
nohup python3 src/evaluate.py $path >$output_file 2> $output_file &disown