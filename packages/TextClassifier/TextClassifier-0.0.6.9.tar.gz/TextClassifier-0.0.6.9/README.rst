TextClassifier
---------------

A simple, efficient short-text classification tool based on Numpy,scikit-learn,Pandas,Matplotlib.

Train Data Format
````````````````````

==========  		=====================================================
   type                                      Text
==========  		=====================================================
   game                  The LoL champions pro players would ban forever
  society                  In Beijing you should keep the rules
   etc.                                      etc.
==========  		=====================================================

Sample Usage
````````````
.. code:: python

    >>> import TextClassifier
    >>> tc = TextClassifier.classifier_container() 
    >>> tc.load_Data('../data/Train_data.txt') 
    >>> tc.train() 

    >>> print tc.predict('Faker is the first League of Legends player to earn over $1 million in prize money') 
    >>> [u'game'] 

    >>> print tc.predict(['Faker is the first League of Legends player to earn over $1 million in prize money',
			'18-year-old youth killed 88-year-old veteran',
			'Take you into the real North Korea']) 
    >>> [u'game',u'society',u'world'] 

Installation 
```````````` 
.. code:: bash 

    $ pip install TextClassifier 

Links 
````` 

* `Code on Github <https://github.com/ArnoldGaius/Text_Classifier>`_