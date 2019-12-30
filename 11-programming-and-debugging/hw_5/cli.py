import argparse
import os
import sys
import re

parser = argparse.ArgumentParser()

parser.add_argument('--model',
                    '-m',
                    dest='model',
                    type=str,
                    choices=['DT', 'RF', 'GB', 'PCA'],
                    default='DT',
                    help="Name of training model. \
                    Available  to use: DT - decision tree,  \
                                       RF - random forest,  \
                                       GBoost - gradient boosting,  \
                                       PCA - principal component analysis.")

parser.add_argument(dest='input_path',
                    type=str,
                    help="directory or file of input dataset "
                         "can be in format: .csv, .parquet, tar.gz, .tar.bz2, .zip")

parser.add_argument('--target-directory',
                    '-t',
                    dest='target_directory',
                    type=str,
                    default='./',
                    help="Path for storing a trained model.")

parser.add_argument('--compression',
                    '-c',
                    type=str,
                    choices=['xz', 'gzip', 'zip', 'bzip2'],
                    help='Data compression algorithm.', )

# Gradient boosting
parser.add_argument('--loss',
                    dest='loss',
                    type=str,
                    choices=['exponential', 'deviance'],
                    default='deviance',
                    help='Loss function to be optimized. ‘deviance’ refers to deviance '
                         '(= logistic regression) for classification with probabilistic outputs. '
                         'For loss ‘exponential’ gradient boosting recovers the AdaBoost algorithm.')

parser.add_argument('--learning-rate',
                    dest='learning_rate',
                    type=float,
                    default=0.1,
                    help='Learning rate shrinks the contribution of each tree by learning_rate.'
                         'There is a trade-off between learning_rate and n_estimators.')

parser.add_argument('--subsample',
                    dest='subsample',
                    type=float,
                    default=1,
                    help='he fraction of samples to be used for fitting the individual base learners.')

# Decision Tree
parser.add_argument('--splitter',
                    dest='splitter',
                    type=str,
                    choices=['gini', 'entropy'],
                    default='best',
                    help='The strategy used to choose the split at each node.')

# General
parser.add_argument('--count-trees',
                    dest='count_trees',
                    type=int,
                    default=100,
                    help='The number of trees in the forest')

parser.add_argument('--criterion',
                    dest='criterion',
                    type=str,
                    choices=['gini', 'entropy'],
                    default='gini',
                    help='The function to measure the quality of a split.')

parser.add_argument('--max-depth',
                    dest='max_depth',
                    type=int,
                    default=None,
                    help='The maximum depth of the tree. ')

parser.add_argument('--min-samples-split',
                    dest='min_samples_split',
                    type=float,
                    default=2,
                    help='The minimum number of samples required to split an internal node.')

parser.add_argument('--min-samples-leaf',
                    dest='min_samples_leaf',
                    type=float,
                    default=1,
                    help='The minimum number of samples required to be at a leaf node.')

parser.add_argument('--min-weight-fraction-leaf',
                    dest='min_weight_fraction_leaf',
                    type=float,
                    default=0,
                    help='The minimum weighted fraction of the sum total of weights '
                         '(of all the input samples) required to be at a leaf node.')

parser.add_argument('--max-features',
                    dest='max_features',
                    type=str,
                    default='auto',
                    help='The number of features to consider when looking for the best split')

# PCA
parser.add_argument('--n-components',
                    dest='n_components',
                    type=int,
                    default=None,
                    help="Number of components to keep. If n_components is None,"
                         " then n_components is set to min(n_samples, n_features).")

args = parser.parse_args()

input_path = args.input_path
target_directory = args.target_directory
model = args.model

extensions = ('.csv', '.parquet', '.json',
              '.tar.gz', '.tar.bz2', '.zip')

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

if not os.path.isdir(input_path) and not input_path.endswith(extensions):
    sys.exit(f"Not allowed file or dir. Please use on of {extensions} format")

if not os.path.isdir(target_directory) and not os.path.isfile(target_directory):
    if re.match(regex, target_directory) is None:
        sys.exit('Incorrect target path! Please specify a folder or a valid URL!')

if model in ('DT', 'RF', 'GD'):
    count_trees = args.count_trees
    criterion = args.criterion
    max_depth = args.max_depth
    min_samples_split = args.min_samples_split
    min_samples_leaf = args.min_samples_leaf
    min_weight_fraction_leaf = args.min_weight_fraction_leaf
    max_features = args.max_features
    if model == 'DT':
        splitter = args.splitter
    elif model == 'GD':
        loss = args.loss
        learning_rate = args.learning_rate
        subsample = args.subsample
elif model == 'PCA':
    n_components = args.n_components
