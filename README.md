# VeRA-plus

## Table of Contents
- [Installation](#installation)
- [Example](#example)

## Installation
To install the required packages in a new environment, follow these steps:
```python
git clone https://github.com/huggingface/transformers
cd transformers
pip install .
pip install peft
pip install evaluate
```
## Example 
### LoRA
```python
python main_lora.py \
--batch_size 16 \
--model_name_or_path "roberta-base" \
--task "mrpc" \
--num_epochs 30 \
--max_length 512 \
--r 8 \
--lora_alpha 8 \
--use_rslora true \
--lr 4e-4
```
where `model_name_or_path` can be "roberta-base" or "roberta-large".
For `task`, we can choose between "sst2", "mrpc", "cola", "qnli", "rte", or "stsb".
Set `use_rsvera` "true" if we want to apply **rank stabilization** or "false" otherwise.
### VeRA
```python
python rsvera.py \
--batch_size 64 \
--model_name_or_path "roberta-base" \
--task "mrpc" \
--num_epochs 30 \
--max_length 512 \
--r 1024 \
--vera_alpha 8 \
--use_rsvera true \
--head_lr 4e-3 \
--vera_lr 1e-2
```
### VeRA-plus
```python
python rsvera.py\
 --batch_size 64\
 --model_name_or_path roberta-base\
 --task mrpc\
 --num_epochs 30\
 --max_length 512\
 --r 1024\
 --vera_alpha 8\
 --use_rsvera true\
 --head_lr 4e-3\
 --vera_lr 1e-2\
```

