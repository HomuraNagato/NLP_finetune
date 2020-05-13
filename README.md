# NLP_finetune

## Introduction, Results

View presentation/report.pdf for a detailed report on this project. View 'presentation/Grover 
a new voice pres{1,2,3}.pptx' for lab presentations covering progress of the project;
includes generated text.

The goal of this project is to investigate the ability of a pre-trained model to fine 
tune on new data to speak in an author's voice and quantify a lower bound on this task.

This project was inspired by the publication of GROVER [[1]](#1), 
where researchers extended GPT-2 [[2]](#2) by adding trainable fields that include
not only the body of a text, but also the domain, date, author, and headline of an article; with
the hope that conditional text generation will be more realistic than unconditional. What they
found is that Grover is able to generate articles as if they were written by humans.

One aspect that is not convered in the Grover paper is how well the model trains on a conditioned variable, for example
the author of the article. The implications of this are significant. If Grover or a similar algorithm
can be trained to speak in the voice of an author and have it say something contrary to their moral
values could be quite damaging. To better understand how Grover might be trained to perform such a
feat is the aim of this project. While Grover is ideal, due to limitations in the ability to fine-tune
the model, GPT-2 was used as the algorithm for fine-tuning. This loses out on specific layers included
during training yet as shown in the results section of the report, some of the conditionality can be recovered through
proper format of the training dataset.

We see that the algorithm appears to be able to produce readable text with as few as 300-400 examples. 
The content and format of the data affects the convergence rate. Comparing nytimes to congress, 
consistent and structured fields allows an easier ability for the algorithm to generate structured text. 
The effect of cleansing the text slows this convergence yet produces potentially a more generalized form
 with generic tags. Finally, the algorithm is able to speak in different voices, represented by the 
comparison of the congress sessions 061 and 111.

With specifics coverted in the report, we see the algorithm is able to speak in an authors voice with
as few as 300-400 examples. The ability of the algorithm to pick up on fields and format generated text
occurs within 700-1300 examples for twitter data, yet remains harder for congress data. Congress data
shows the ability of the algorithm to pick up on author specifics such as their party and role in congress.

## Data Preparation

### Twitter data collection

twitter/data_collection.py will call the twitter API to collect tweets for a user. Use parameter 
--help to view available parameters to include when calling this function. The results are saved as
a csv.

twitter/data_inspection.py will format csv files into text files ready for training on GPT-2 with
 fields resembling Grover's conditional fields.

### Congress data collection

Data stored locally.

congress/initiation.py will map speaker data to speech data for a correspondence between a speaker
and their speeches. Cleanses data by removing procedural words and other expected steps. Finally
adds fields and saves as text ready format for fine-tuning. 


## Fine-tuning

gpt2_internal.py prepares the tokenizers and saves a local model for preparation.

train and train_congress are scripts that run on the Brown University compute_grid that utilizes
a GPU to fine-tune GPT-2 on the provided data. 

generation and generation_congress are scripts that run on the Brown University compute_grid that 
utilizes a GPU to generate various texts for a given prompt and checkpoint.

## References

<a id="1">[1]</a>
@Online{zellers19:_defen_again_neural_fake_news,
  author       = {Rowan Zellers AND Ari Holtzman AND Hannah Rashkin
                  AND Yonatan Bisk AND Ali Farhadi AND Franziska
                  Roesner AND Yejin Choi},
  title	       = {{Defending Against Neural Fake News}},
  year	       = 2019,
  archiveprefix= {arXiv},
  eprint       = {1905.12616v2},
  primaryclass = {cs.CL},
  url = {https://arxiv.org/abs/1905.12616}
}

<a id="2">[2]</a>
@article{radford2019language,
  title        = {Language Models are Unsupervised Multitask Learners},
  author       = {Radford, Alec and Wu, Jeff and Child, Rewon and Luan, David and Amodei, Dario and Sutskever, Ilya},
  year         = {2019}
}
