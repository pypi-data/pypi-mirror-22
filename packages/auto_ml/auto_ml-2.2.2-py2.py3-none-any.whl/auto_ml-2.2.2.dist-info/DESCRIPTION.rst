b'# auto\_ml:raw-latex:`\n`'b'> Automated machine learning for
production and analytics:raw-latex:`\n`'b':raw-latex:`\n`'b'|Build
Status|\ :raw-latex:`\n`'b'|Documentation
Status|\ :raw-latex:`\n`'b'|PyPI version|\ :raw-latex:`\n`'b'|Coverage
Status|\ :raw-latex:`\n`'b'|license|\ :raw-latex:`\n`'b':raw-latex:`\n`'b':raw-latex:`\n`'b'##
Installation:raw-latex:`\n`'b':raw-latex:`\n`'b'-
``pip install auto_ml``\ :raw-latex:`\n`'b':raw-latex:`\n`'b'## Getting
started:raw-latex:`\n`'b':raw-latex:`\n`'b'``python\n'b'from auto_ml import Predictor\n'b'from auto_ml.utils import get_boston_dataset\n'b'\n'b'df_train, df_test = get_boston_dataset()\n'b'\n'b'column_descriptions = {\n'b"    'MEDV': 'output'\n"b"    , 'CHAS': 'categorical'\n"b'}\n'b'\n'b"ml_predictor = Predictor(type_of_estimator='regressor', column_descriptions=column_descriptions)\n"b'\n'b'ml_predictor.train(df_train)\n'b'\n'b'ml_predictor.score(df_test, df_test.MEDV)\n'b'``\ :raw-latex:`\n`'b':raw-latex:`\n`'b'##
Show off some more features!:raw-latex:`\n`'b':raw-latex:`\n`'b"auto\_ml
is designed for production. Here's an example that includes serializing
and loading the trained model, then getting predictions on single
dictionaries, roughly the process you'd likely follow to deploy the
trained
model.:raw-latex:`\n`"b':raw-latex:`\n`'b'``python\n'b'from auto_ml import Predictor\n'b'from auto_ml.utils import get_boston_dataset\n'b'from auto_ml.utils_models import load_ml_model\n'b'\n'b'# Load data\n'b'df_train, df_test = get_boston_dataset()\n'b'\n'b"# Tell auto_ml which column is 'output'\n"b"# Also note columns that aren't purely numerical\n"b"# Examples include ['nlp', 'date', 'categorical', 'ignore']\n"b'column_descriptions = {\n'b"  'MEDV': 'output'\n"b"  , 'CHAS': 'categorical'\n"b'}\n'b'\n'b"ml_predictor = Predictor(type_of_estimator='regressor', column_descriptions=column_descriptions)\n"b'\n'b'ml_predictor.train(df_train)\n'b'\n'b'# Score the model on test data\n'b'test_score = ml_predictor.score(df_test, df_test.MEDV)\n'b'\n'b'# auto_ml is specifically tuned for running in production\n'b'# It can get predictions on an individual row (passed in as a dictionary)\n'b'# A single prediction like this takes ~1 millisecond\n'b'# Here we will demonstrate saving the trained model, and loading it again\n'b'file_name = ml_predictor.save()\n'b'\n'b'trained_model = load_ml_model(file_name)\n'b'\n'b'# .predict and .predict_proba take in either:\n'b'# A pandas DataFrame\n'b'# A list of dictionaries\n'b'# A single dictionary (optimized for speed in production evironments)\n'b'predictions = trained_model.predict(df_test)\n'b'print(predictions)\n'b'``\ :raw-latex:`\n`'b':raw-latex:`\n`'b'##
XGBoost, Deep Learning with TensorFlow & Keras, and
LightGBM:raw-latex:`\n`'b':raw-latex:`\n`'b'auto\_ml has all three of
these awesome libraries integrated!:raw-latex:`\n`'b'Generally, just
pass one of them in for
model\_names.:raw-latex:`\n`'b"``ml_predictor.train(data, model_names=['DeepLearningClassifier'])``\ :raw-latex:`\n`"b':raw-latex:`\n`'b'Available
options are:raw-latex:`\n`'b'- ``DeepLearningClassifier`` and
``DeepLearningRegressor``\ :raw-latex:`\n`'b'- ``XGBClassifier`` and
``XGBRegressor``\ :raw-latex:`\n`'b'- ``LGBMClassifer`` and
``LGBMRegressor``\ :raw-latex:`\n`'b':raw-latex:`\n`'b'All of these
projects are ready for production. These projects all have prediction
time in the 1 millisecond range for a single prediction, and are able to
be serialized to disk and loaded into a new environment after
training.:raw-latex:`\n`'b':raw-latex:`\n`'b"Depending on your machine,
they can occasionally be difficult to install, so they are not included
in auto\_ml's default installation. You are responsible for installing
them yourself. auto\_ml will run fine without them installed (we check
what's isntalled before choosing which algorithm to use). If you want to
try the easy install, just ``pip install -r advanced_requirements.txt``,
which will install TensorFlow, Keras, and XGBoost. LightGBM is not
available as a pip install
currently.:raw-latex:`\n`"b':raw-latex:`\n`'b':raw-latex:`\n`'b'##
Feature Responses:raw-latex:`\n`'b'Get linear-model-esque
interpretations from non-linear models. See the
[docs}(http://auto-ml.readthedocs.io/en/latest/feature\_responses.html)
for more information and
caveats.:raw-latex:`\n`'b':raw-latex:`\n`'b':raw-latex:`\n`'b'##
Classification:raw-latex:`\n`'b':raw-latex:`\n`'b"Binary and multiclass
classification are both supported. Note that for now, labels must be
integers (0 and 1 for binary classification). auto\_ml will
automatically detect if it is a binary or multiclass classification
problem- you just have to pass in
``ml_predictor = Predictor(type_of_estimator='classifier', column_descriptions=column_descriptions)``\ :raw-latex:`\n`"b':raw-latex:`\n`'b':raw-latex:`\n`'b'##
Feature Learning:raw-latex:`\n`'b':raw-latex:`\n`'b'Also known as
"finally found a way to make this deep learning stuff useful for my
business". Deep Learning is great at learning important features from
your data. But the way it turns these learned features into a final
prediction is relatively basic. Gradient boosting is great at turning
features into accurate predictions, but it doesn't do any feature
learning.:raw-latex:`\n`'b':raw-latex:`\n`'b"In auto\_ml, you can now
automatically use both types of models for what they're great at. If you
pass ``feature_learning=True, fl_data=some_dataframe`` to ``.train()``,
we will do exactly that: train a deep learning model on your
``fl_data``. We won't ask it for predictions (standard stacking
approach), instead, we'll use it's penultimate layer to get it's 10 most
useful features. Then we'll train a gradient boosted model (or any other
model of your choice) on those features plus all the original
features.:raw-latex:`\n`"b':raw-latex:`\n`'b"Across some problems, we've
witnessed this lead to a 5% gain in accuracy, while still making
predictions in 1-4 milliseconds, depending on model
complexity.:raw-latex:`\n`"b':raw-latex:`\n`'b'``ml_predictor.train(df_train, feature_learning=True, fl_data=df_fl_data)``\ :raw-latex:`\n`'b':raw-latex:`\n`'b'This
feature only supports regression and binary classification currently.
The rest of auto\_ml supports multiclass
classification.:raw-latex:`\n`'b':raw-latex:`\n`'b'## Categorical
Ensembling:raw-latex:`\n`'b':raw-latex:`\n`'b"Ever wanted to train one
market for every store/customer, but didn't want to maintain hundreds of
thousands of independent models? With
``ml_predictor.train_categorical_ensemble()``, we will handle that for
you. You'll still have just one consistent API,
``ml_predictor.predict(data)``, but behind this single API will be one
model for each category you included in your training
data.:raw-latex:`\n`"b':raw-latex:`\n`'b"Just tell us which column holds
the category you want to split on, and we'll handle the rest. As always,
saving the model, loading it in a different environment, and getting
speedy predictions live in production is baked right
in.:raw-latex:`\n`"b':raw-latex:`\n`'b"``ml_predictor.train_categorical_ensemble(df_train, categorical_column='store_name')``\ :raw-latex:`\n`"b':raw-latex:`\n`'b':raw-latex:`\n`'b'###
More details available in the
docs:raw-latex:`\n`'b':raw-latex:`\n`'b'http://auto-ml.readthedocs.io/en/latest/:raw-latex:`\n`'b':raw-latex:`\n`'b':raw-latex:`\n`'b'###
Advice:raw-latex:`\n`'b':raw-latex:`\n`'b"Before you go any further, try
running the code. Load up some data (either a DataFrame, or a list of
dictionaries, where each dictionary is a row of data). Make a
``column_descriptions`` dictionary that tells us which attribute name in
each row represents the value we're trying to predict. Pass all that
into ``auto_ml``, and see what
happens!:raw-latex:`\n`"b':raw-latex:`\n`'b"Everything else in these
docs assumes you have done at least the above. Start there and
everything else will build on top. But this part gets you the output
you're probably interested in, without unnecessary
complexity.:raw-latex:`\n`"b':raw-latex:`\n`'b':raw-latex:`\n`'b'##
Docs:raw-latex:`\n`'b':raw-latex:`\n`'b'The full docs are available at
https://auto\_ml.readthedocs.io:raw-latex:`\n`'b"Again though, I'd
strongly recommend running this on an actual dataset before referencing
the docs any
futher.:raw-latex:`\n`"b':raw-latex:`\n`'b':raw-latex:`\n`'b'## What
this project does:raw-latex:`\n`'b':raw-latex:`\n`'b'Automates the whole
machine learning process, making it super easy to use for both
analytics, and getting real-time predictions in
production.:raw-latex:`\n`'b':raw-latex:`\n`'b'A quick overview of
buzzwords, this project automates::raw-latex:`\n`'b':raw-latex:`\n`'b"-
Analytics (pass in data, and auto\_ml will tell you the relationship of
each variable to what it is you're trying to
predict).:raw-latex:`\n`"b'- Feature Engineering (particularly around
dates, and NLP).:raw-latex:`\n`'b'- Robust Scaling (turning all values
into their scaled versions between the range of 0 and 1, in a way that
is robust to outliers, and works with sparse data).:raw-latex:`\n`'b'-
Feature Selection (picking only the features that actually prove
useful).:raw-latex:`\n`'b'- Data formatting (turning a DataFrame or a
list of dictionaries into a sparse matrix, one-hot encoding categorical
variables, taking the natural log of y for regression problems,
etc).:raw-latex:`\n`'b"- Model Selection (which model works best for
your problem- we try roughly a dozen apiece for classification and
regression problems, including favorites like XGBoost if it's installed
on your machine).:raw-latex:`\n`"b'- Hyperparameter Optimization (what
hyperparameters work best for that model).:raw-latex:`\n`'b"- Big Data
(feed it lots of data- it's fairly efficient with
resources).:raw-latex:`\n`"b'- Unicorns (you could conceivably train it
to predict what is a unicorn and what is not).:raw-latex:`\n`'b'- Ice
Cream (mmm, tasty...).:raw-latex:`\n`'b'- Hugs (this makes it much
easier to do your job, hopefully leaving you more time to hug those
those you care
about).:raw-latex:`\n`'b':raw-latex:`\n`'b':raw-latex:`\n`'b'### Running
the tests:raw-latex:`\n`'b':raw-latex:`\n`'b"If you've cloned the source
code and are making any changes (highly encouraged!), or just want to
make sure everything works in your environment,
run:raw-latex:`\n`"b'``nosetests -v tests``.:raw-latex:`\n`'b':raw-latex:`\n`'b"CI
is also set up, so if you're developing on this, you can just open a PR,
and the tests will run automatically on
Travis-CI.:raw-latex:`\n`"b':raw-latex:`\n`'b'The tests are relatively
comprehensive, though as with everything with auto\_ml, I happily
welcome your contributions
here!:raw-latex:`\n`'b':raw-latex:`\n`'|Analytics|

.. |Build Status| image:: https://travis-ci.org/ClimbsRocks/auto_ml.svg?branch=master
   :target: https://travis-ci.org/ClimbsRocks/auto_ml
.. |Documentation Status| image:: http://readthedocs.org/projects/auto-ml/badge/?version=latest
   :target: http://auto-ml.readthedocs.io/en/latest/?badge=latest
.. |PyPI version| image:: https://badge.fury.io/py/auto_ml.svg
   :target: https://badge.fury.io/py/auto_ml
.. |Coverage Status| image:: https://coveralls.io/repos/github/ClimbsRocks/auto_ml/badge.svg?branch=master&cacheBuster=1
   :target: https://coveralls.io/github/ClimbsRocks/auto_ml?branch=master&cacheBuster=1
.. |license| image:: https://img.shields.io/github/license/mashape/apistatus.svg
   :target: (https://img.shields.io/github/license/mashape/apistatus.svg)
.. |Analytics| image:: https://ga-beacon.appspot.com/UA-58170643-5/auto_ml/pypi
   :target: https://github.com/igrigorik/ga-beacon


