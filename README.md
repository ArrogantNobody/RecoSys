# Content-Collaborative-based Movie Recommendation System

This is the repository to the paper "Content-Collaborative-based Movie Recommendation System" by Zihao Wang, Hang Zhu, Zijian Kuang, Xinran Tie.
We proposed to use a hybrid Content-Collaborative-based algorithm to build our Movie Recommendation System.

<a href="https://arxiv.org/abs/1709.02371" rel="Paper"><img src="https://github.com/ArrogantNobody/RecoSys/blob/master/readme_imgs/pipeline.png" alt="Paper" width="100%"></a>

## Getting Started

You will need [Python 3.6](https://www.python.org/downloads) and the packages specified in _requirements.txt_.
We recommend setting up a [virtual environment with pip](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
and installing the packages there.

Install packages with:

```
$ pip install -r requirements.txt
```

## Dataset

The data sets were collected over various periods of time with different sizes of the set. For our application, the model is trained and evaluated with the latest small <a href="https://grouplens.org/datasets/movielens/latest/" rel="dataset"/> MovieLens dataset </a>
 
## Configure and Run the Code
1. Make sure you have the db.sqlite3 database file under the root folder
2. Please follow the code below to start the server for our web application:

```python
python manage.py runserver
```

3. Then you can view our web application use any browers at http://127.0.0.1:8000/

Out put results:

Login page:
<img src="https://github.com/ArrogantNobody/RecoSys/blob/master/readme_imgs/1.png" alt="Paper" width="100%">

Movie recommendation page:
<img src="https://github.com/ArrogantNobody/RecoSys/blob/master/readme_imgs/2.png" alt="Paper" width="100%">

Movie rating page:
<img src="https://github.com/ArrogantNobody/RecoSys/blob/master/readme_imgs/3.png" alt="Paper" width="100%">


## Evaluation of the model:

The accuray of a trained model is evaluated based on the metrics of precision@k and ROC AUC. 

For precision at k, we have set k = 10. We'll be look at whether the top 10 movie recommendation are relevant to the user.

For AUC, we'll be calculating the probability that a randomly chosen positive sample will be ranked higher than a randomly chosen negative sample.

To run evaluation:

``` 
python recommender.py
``` 

## Credits
We want to thank the work of the [lightfm] that implemented by maciejkula, we have used the lightfm as part of our recommendation model in our project.

## Citation
```
[1]  @inproceedings{lightfm,
  author    = {Maciej Kula},
  editor    = {Toine Bogers and
               Marijn Koolen},
  title     = {Metadata Embeddings for User and Item Cold-start Recommendations},
  booktitle = {Proceedings of the 2nd Workshop on New Trends on Content-Based Recommender
               Systems co-located with 9th {ACM} Conference on Recommender Systems
               (RecSys 2015), Vienna, Austria, September 16-20, 2015.},
  series    = {{CEUR} Workshop Proceedings},
  volume    = {1448},
  pages     = {14--21},
  publisher = {CEUR-WS.org},
  year      = {2015},
  url       = {http://ceur-ws.org/Vol-1448/paper4.pdf},
}
```

## License

This project is licensed under the MIT License.
