"""This module contains RQ jobs"""
from rq.decorators import job
from rq import get_current_job
from xcessiv import redis_conn
from xcessiv import functions
from xcessiv import exceptions
from xcessiv import models
import numpy as np
import os
import sys
import traceback
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold


def extraction_data_statistics(path):
    """ Generates data statistics for the given data extraction setup stored
    in Xcessiv notebook.

    This is in rqtasks.py but not as a job yet. Temporarily call this directly
    while I'm figuring out Javascript lel.

    Args:
        path (str, unicode): Path to xcessiv notebook
    """
    with functions.DBContextManager(path) as session:
        extraction = session.query(models.Extraction).first()
        X, y = extraction.return_main_dataset()
        functions.verify_dataset(X, y)

        if extraction.test_dataset['method'] == 'split_from_main':
            X, X_test, y, y_test = train_test_split(
                X,
                y,
                test_size=extraction.test_dataset['split_ratio'],
                random_state=extraction.test_dataset['split_seed'],
                stratify=y
            )
        elif extraction.test_dataset['method'] == 'source':
            if 'source' not in extraction.test_dataset or not extraction.test_dataset['source']:
                raise exceptions.UserError('Source is empty')

            extraction_code = extraction.test_dataset["source"]
            extraction_function = functions.\
                import_object_from_string_code(extraction_code, "extract_test_dataset")
            X_test, y_test = extraction_function()
        else:
            X_test, y_test = None, None

        if extraction.meta_feature_generation['method'] == 'holdout_split':
            X, X_holdout, y, y_holdout = train_test_split(
                X,
                y,
                test_size=extraction.meta_feature_generation['split_ratio'],
                random_state=extraction.meta_feature_generation['seed'],
                stratify=y
            )
        elif extraction.meta_feature_generation['method'] == 'holdout_source':
            if 'source' not in extraction.meta_feature_generation or \
                    not extraction.meta_feature_generation['source']:
                raise exceptions.UserError('Source is empty')

            extraction_code = extraction.meta_feature_generation["source"]
            extraction_function = functions.\
                import_object_from_string_code(extraction_code,
                                               "extract_holdout_dataset")
            X_holdout, y_holdout = extraction_function()
        else:
            X_holdout, y_holdout = None, None

        data_stats = dict()
        data_stats['train_data_stats'] = functions.verify_dataset(X, y)
        if X_test is not None:
            data_stats['test_data_stats'] = functions.verify_dataset(X_test, y_test)
        else:
            data_stats['test_data_stats'] = None
        if X_holdout is not None:
            data_stats['holdout_data_stats'] = functions.verify_dataset(X_holdout, y_holdout)
        else:
            data_stats['holdout_data_stats'] = None

        extraction.data_statistics = data_stats

        session.add(extraction)
        session.commit()


@job('default', connection=redis_conn, timeout=86400)
def generate_meta_features(path, base_learner_id):
    """Generates meta-features for specified base learner

    After generation of meta-features, the file is saved into the meta-features folder

    Args:
        path (str): Path to Xcessiv notebook

        base_learner_id (str): Base learner ID
    """
    with functions.DBContextManager(path) as session:
        base_learner = session.query(models.BaseLearner).filter_by(id=base_learner_id).first()
        if not base_learner:
            raise exceptions.UserError('Base learner {} '
                                       'does not exist'.format(base_learner_id))

        base_learner.job_id = get_current_job().id
        base_learner.job_status = 'started'

        session.add(base_learner)
        session.commit()

        try:
            est = base_learner.return_estimator()
            extraction = session.query(models.Extraction).first()
            X, y = extraction.return_train_dataset()

            if extraction.meta_feature_generation['method'] == 'cv':
                cv = StratifiedKFold(
                    n_splits=extraction.meta_feature_generation['folds'],
                    shuffle=True,
                    random_state=extraction.meta_feature_generation['seed']
                )
                meta_features_list = []
                trues_list = []
                for train_index, test_index in cv.split(X, y):
                    X_train, X_test = X[train_index], X[test_index]
                    y_train, y_test = y[train_index], y[test_index]
                    est = est.fit(X_train, y_train)
                    meta_features_list.append(
                        getattr(est, base_learner.base_learner_origin.
                                meta_feature_generator)(X_test)
                    )
                    trues_list.append(y_test)
                meta_features = np.concatenate(meta_features_list, axis=0)
                y_true = np.concatenate(trues_list)

            else:
                X_holdout, y_holdout = extraction.return_holdout_dataset()
                est = est.fit(X, y)
                meta_features = getattr(est, base_learner.base_learner_origin.
                                        meta_feature_generator)(X_holdout)
                y_true = y_holdout

            for key in base_learner.base_learner_origin.metric_generators:
                metric_generator = functions.import_object_from_string_code(
                    base_learner.base_learner_origin.metric_generators[key],
                    'metric_generator'
                )
                base_learner.individual_score[key] = metric_generator(y_true, meta_features)

            meta_features_path = base_learner.meta_features_path(path)

            if not os.path.exists(os.path.dirname(meta_features_path)):
                os.makedirs(os.path.dirname(meta_features_path))

            np.save(meta_features_path, meta_features, allow_pickle=False)
            base_learner.job_status = 'finished'
            base_learner.meta_features_exists = True
            session.add(base_learner)
            session.commit()

        except:
            session.rollback()
            base_learner.job_status = 'errored'
            base_learner.description['error_type'] = repr(sys.exc_info()[0])
            base_learner.description['error_value'] = repr(sys.exc_info()[1])
            base_learner.description['error_traceback'] = \
                traceback.format_exception(*sys.exc_info())
            session.add(base_learner)
            session.commit()
            raise


@job('default', connection=redis_conn, timeout=86400)
def evaluate_stacked_ensemble(path, ensemble_id):
    """Evaluates the ensemble and updates the database when finished/

    Args:
        path (str): Path to Xcessiv notebook

        ensemble_id (str): Ensemble ID
    """
    with functions.DBContextManager(path) as session:
        stacked_ensemble = session.query(models.StackedEnsemble).filter_by(
            id=ensemble_id).first()
        if not stacked_ensemble:
            raise exceptions.UserError('Stacked ensemble {} '
                                       'does not exist'.format(ensemble_id))

        stacked_ensemble.job_id = get_current_job().id
        stacked_ensemble.job_status = 'started'

        session.add(stacked_ensemble)
        session.commit()

        try:
            meta_features_list = []
            for base_learner in stacked_ensemble.base_learners:
                mf = np.load(base_learner.meta_features_path(path))
                if len(mf.shape) == 1:
                    mf = mf.reshape(-1, 1)
                meta_features_list.append(mf)

            secondary_features = np.concatenate(meta_features_list, axis=1)

            # Get data
            extraction = session.query(models.Extraction).first()
            if extraction.meta_feature_generation['method'] == 'cv':
                X, y = extraction.return_train_dataset()
                #  We need to retrieve original order of meta-features
                cv = StratifiedKFold(
                    n_splits=extraction.meta_feature_generation['folds'],
                    shuffle=True,
                    random_state=extraction.meta_feature_generation['seed']
                )
                indices_list = [test_index for train_index, test_index in cv.split(X, y)]
                indices = np.concatenate(indices_list)
                X, y = X[indices], y[indices]
            else:
                X, y = extraction.return_holdout_dataset()

            if stacked_ensemble.append_original:
                secondary_features = np.concatenate((secondary_features, X), axis=1)

            est = stacked_ensemble.return_secondary_learner()

            cv = StratifiedKFold(
                n_splits=5,
                shuffle=True,
                random_state=8
            )
            preds = []
            trues_list = []
            for train_index, test_index in cv.split(secondary_features, y):
                X_train, X_test = secondary_features[train_index], secondary_features[test_index]
                y_train, y_test = y[train_index], y[test_index]
                est = est.fit(X_train, y_train)
                preds.append(
                    getattr(est, stacked_ensemble.base_learner_origin.
                            meta_feature_generator)(X_test)
                )
                trues_list.append(y_test)
            preds = np.concatenate(preds, axis=0)
            y_true = np.concatenate(trues_list)

            for key in stacked_ensemble.base_learner_origin.metric_generators:
                metric_generator = functions.import_object_from_string_code(
                    stacked_ensemble.base_learner_origin.metric_generators[key],
                    'metric_generator'
                )
                stacked_ensemble.individual_score[key] = metric_generator(y_true, preds)

            stacked_ensemble.job_status = 'finished'
            session.add(stacked_ensemble)
            session.commit()

        except:
            session.rollback()
            stacked_ensemble.job_status = 'errored'
            stacked_ensemble.description['error_type'] = repr(sys.exc_info()[0])
            stacked_ensemble.description['error_value'] = repr(sys.exc_info()[1])
            stacked_ensemble.description['error_traceback'] = \
                traceback.format_exception(*sys.exc_info())
            session.add(stacked_ensemble)
            session.commit()
            raise
