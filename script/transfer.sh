# while getopts k: flag

# do 
#     case "${flag}" in
#         k) k=${OPTARG};;
#     esac
# done

while getopts p: flag

do
    case "${flag}" in
        p) path=${OPTARG};;
    esac
done

# nohup ./myprogram > foo.out 2> foo.err < /dev/null &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --nproc_per_node=1 src/transfer.py $path >output/log/log.out 2> output/log/log.err &disown