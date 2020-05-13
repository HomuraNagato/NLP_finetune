
import torch
import transformers
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load pre-trained model tokenizer (vocabulary)
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Load pre-trained model (weights)
model = GPT2LMHeadModel.from_pretrained('gpt2')

# add all additional special tokens as an array of strings of special tokens
# cleaned twitter
'''
special_tokens_dict = { 'eos_token': '<|endoftext|>',
                        'additional_special_tokens': ['<|begindomain|>', '<|endofdomain|>', '<|begindate|>', '<|endofdate|>', 
                                                     '<|beginauthors|>', '<|endofauthors|>', '<|begintitle|>', '<|endoftitle|>',
                                                     '<|beginarticle|>', '<|endofarticle|>', '<|url|>', '<|user|>', '<|hashtag|>']}

# uncleansed twitter
special_tokens_dict = { 'eos_token': '<|endoftext|>',
                        'additional_special_tokens': ['<|begindomain|>', '<|endofdomain|>', '<|begindate|>', '<|endofdate|>', 
                                                     '<|beginauthors|>', '<|endofauthors|>', '<|begintitle|>', '<|endoftitle|>',
                                                     '<|beginarticle|>', '<|endofarticle|>']}
'''
#'''
# congress
special_tokens_dict = { 'eos_token': '<|endoftext|>',
                        'additional_special_tokens': ['<|beginauthor|>', '<|endofauthor|>', '<|beginspeech|>', '<|endofspeech|>']}
#'''
tokenizer.add_special_tokens(special_tokens_dict)

# add all additional special tokens as an array of strings of special tokens
tokenizer.save_pretrained('models/congress_tokenizer/')
#tokenizer.save_pretrained('models/twitter_tokenizer/')

#model.save_pretrained('models/')
