python train.py -mode train -cfg gpt_path=distilgpt2 lr=1e-4 warmup_steps=2000 gradient_accumulation_steps=16 batch_size=2 epoch_num=60 exp_no=best_model
echo "done with distill no curriculum"
python train.py -mode train -cfg gpt_path=../distilgpt2/ta_noencode lr=1e-4 warmup_steps=2000 gradient_accumulation_steps=16 batch_size=2 epoch_num=60 exp_no=best_model_noencode
echo "done with distill no encode"
python train.py -mode train -cfg gpt_path=../distilgpt2/ta_encode_nolabel lr=1e-4 warmup_steps=2000 gradient_accumulation_steps=16 batch_size=2 epoch_num=60 exp_no=best_model_encode_nolabel
echo "done with distill encode no label"
python train.py -mode train -cfg gpt_path=../distilgpt2/ta_encode lr=1e-4 warmup_steps=2000 gradient_accumulation_steps=16 batch_size=2 epoch_num=60 exp_no=best_model_encode
echo "done with distill encode"

echo "finished"
