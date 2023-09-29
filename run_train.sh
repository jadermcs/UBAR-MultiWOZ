python train.py -mode train -cfg gpt_path=models/gpt2-large/ta_encode lr=1e-5 warmup_steps=2000 gradient_accumulation_steps=16 batch_size=2 epoch_num=60 exp_no=best_model_encode
echo "done with distill encode"
python train.py -mode train -cfg gpt_path=gpt2-large lr=1e-5 warmup_steps=2000 gradient_accumulation_steps=16 batch_size=2 epoch_num=60 exp_no=best_model
echo "done with distill no curriculum"
python train.py -mode train -cfg gpt_path=models/gpt2-large/ta_noencode lr=1e-5 warmup_steps=2000 gradient_accumulation_steps=16 batch_size=2 epoch_num=60 exp_no=best_model_noencode
echo "done with distill no encode"
python train.py -mode train -cfg gpt_path=models/gpt2-large/ta_encode_nolabel lr=1e-5 warmup_steps=2000 gradient_accumulation_steps=16 batch_size=2 epoch_num=60 exp_no=best_model_encode_nolabel
echo "done with distill encode no label"

echo "finished"
