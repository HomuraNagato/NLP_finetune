
author=realdonaldtrump

python run_language_modeling.py \
    --output_dir=ckpt_$author \
    --overwrite_output_dir \
    --cache_dir=models \
    --model_type=gpt2 \
    --model_name_or_path=gpt2 \
    --logging_steps=100 \
    --save_steps=100 \
    --do_train \
    --per_gpu_train_batch_size=1 \
    --train_data_file=../twitter_data/data/$author_2020-01-26_2020-02-24.txt
