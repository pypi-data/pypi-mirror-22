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
    >>> print tc.predict('生了个可爱的宝贝') 
    >>> [u'baby'] 

Installation 
```````````` 
.. code:: bash 

    $ pip install TextClassifier 

Links 
````` 

* `Code on Github <https://github.com/ArnoldGaius/Text_Classifier>`_