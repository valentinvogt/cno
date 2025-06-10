import torch
device = "cuda" if torch.cuda.is_available() else "cpu"

model_original =  '/cluster/scratch/vogtva/models/cno_delayed_2/model123/epoch=74-step=111000.ckpt'
model_ft = '/cluster/scratch/vogtva/models/cno_delayed_2/FT_brusselator_eval/model0/epoch=142-step=28314.ckpt'

cp1 = torch.load(model_original, map_location=device)
cp2 = torch.load(model_ft, map_location=device)

print("")
