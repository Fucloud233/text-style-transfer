CUDA_VISIBLE_DEVICES=0 nohup torchrun --nproc_per_node=1 utils/server/main.py $path >output/log/server.out 2> output/log/server.err &disown

# FLASK_ENV=development FLASK_APP=utils/server/main.py  flask run