TextClassifier
---------------

A simple, efficient short-text classification tool based on Numpy,scikit-learn,Pandas,Matplotlib.

Sample Usage
````````````
.. code:: python

    >>> import TextClassifier
    >>> tc = TextClassifier.classifier_container() 
    >>> tc.load_Data('../data/Train.txt') 
    >>> tc.train() 
    >>> print tc.predict('Faker is the first League of Legends player to earn over $1 million in prize money') 
    >>> [u'game'] 

Installation 
```````````` 
.. code:: bash 

    $ pip install TextClassifier 

Links 
````` 

* `Code on Github <https://github.com/ArnoldGaius/Text_Classifier>`_