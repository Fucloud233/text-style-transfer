while getopts k: flag

do 
    case "${flag}" in
        k) k=${OPTARG};;
    esac
done

CUDA_VISIBLE_DEVICES=1 torchrun --nproc_per_node=1 src/transfer.py -k=$k