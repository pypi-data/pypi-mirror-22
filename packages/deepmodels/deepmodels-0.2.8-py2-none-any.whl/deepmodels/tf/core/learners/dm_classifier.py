"""Template class for image classifier.
"""

import numpy as np

import tensorflow as tf
import tensorflow.contrib.slim as slim

from deepmodels.tf.core import commons
from deepmodels.tf.core import base_model
from deepmodels.tf.core import common_flags
from deepmodels.tf.core.learners.dm_learner import DMLearner
from deepmodels.shared import data_manager

flags = tf.app.flags
FLAGS = flags.FLAGS


def comp_train_accuracy(pred_logits, label_batch):
  """Compute classification accuracy on training data.

  Args:
    pred_logits: prediction logits.
    label_batch: label batch.
  Returns:
    top 1 classfication accuracy.
  """

  # issue with img_folder_data that produces 2 dimensional label_batch
  label_batch = tf.squeeze(label_batch)
  pred_cls = tf.cast(tf.argmax(pred_logits, 1), tf.int32)
  correct_prediction = tf.cast(
      tf.equal(pred_cls, tf.cast(label_batch, tf.int32)), tf.float32)
  accuracy = tf.reduce_mean(correct_prediction)
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  tf.summary.scalar("eval/mean_clf_accuracy", accuracy)
  print "train/pred_cls_shape is: {}".format(tf.shape(pred_cls))
  print "train/label_batch_shape is: {}".format(tf.shape(label_batch))


# TODO(jiefeng): need a good way ensure user writes the exact same function
# header for overriding.
class DMClassifier(DMLearner):
  """Classifier template class.

  Work with general feature input or image feature.
  """

  def compute_losses(self, gt_labels, pred_logits, endpoints):
    """Compute training losses.

    Override only when non-standard loss for a particular model.

    Args:
      gt_labels: ground truth labels in one-hot encoding.
      pred_logits: prediction logits.
      endpoints: endpoints from the model.
    Returns:
      computed loss tensor.
    """
    clf_loss = tf.losses.softmax_cross_entropy(
        onehot_labels=gt_labels,
        logits=pred_logits,
        weights=1.0,
        scope="clf_loss")
    tf.summary.scalar("losses/clf_loss", clf_loss)
    return clf_loss

  def train(self,
            train_input_batch,
            train_label_batch,
            train_params,
            preprocessed=True):
    """Training process of the classifier.

    Args:
      train_input_batch: input batch for training.
      train_label_batch: class id for training.
      train_params: commons.TrainTestParams object.
      preprocessed: if train data has been preprocessed.
    """
    assert train_input_batch is not None, "train input batch is none"
    assert train_label_batch is not None, "train label batch is none"
    assert isinstance(
        train_params,
        commons.TrainTestParams), "train params is not a valid type"
    self.check_dm_model_exist()
    # self.dm_model.use_graph()
    model_params = self.dm_model.net_params
    if not preprocessed:
      train_input_batch = self.dm_model.preprocess(train_input_batch)
    pred_logits, endpoints = self.build_model(train_input_batch)
    self.set_key_vars(train_params.restore_scopes_exclude,
                      train_params.train_scopes)
    comp_train_accuracy(pred_logits, train_label_batch)
    tf.assert_equal(
        tf.reduce_max(train_label_batch),
        tf.convert_to_tensor(
            model_params.cls_num, dtype=tf.int64))
    onehot_labels = tf.one_hot(
        train_label_batch, model_params.cls_num, on_value=1.0, off_value=0.0)
    # onehot_labels = slim.one_hot_encoding(train_label_batch,
    #                                       model_params.cls_num)
    onehot_labels = tf.squeeze(onehot_labels)
    self.compute_losses(onehot_labels, pred_logits, endpoints)
    init_fn = None
    if train_params.fine_tune and not train_params.resume_training:
      init_fn = slim.assign_from_checkpoint_fn(train_params.custom["model_fn"],
                                               self.vars_to_restore)
    # this would not work if a tensorboard is running...
    if not train_params.resume_training:
      data_manager.remove_dir(train_params.train_log_dir)
    # display regularization loss.
    if train_params.use_regularization:
      regularization_loss = tf.add_n(tf.losses.get_regularization_losses())
      tf.summary.scalar("losses/regularization_loss", regularization_loss)

    total_loss = tf.losses.get_total_loss(
        add_regularization_losses=train_params.use_regularization)
    base_model.train_model_given_loss(
        total_loss, self.vars_to_train, train_params, init_fn=init_fn)

  def test(self,
           test_input_batch,
           test_label_batch,
           test_params,
           preprocessed=True):
    """Testing process of the classifier.

    Args:
      test_input_batch: input batch for testing.
      test_label_batch: class id for testing.
      test_params: commons.TrainTestParams object.
      preprocessed: if data has been preprocessed.
    """
    self.check_dm_model_exist()
    # self.dm_model.use_graph()
    assert isinstance(
        test_params,
        commons.TrainTestParams), "test params is not a valid type"
    if not preprocessed:
      test_input_batch = self.dm_model.preprocess(test_input_batch)
    pred_logits, _ = self.build_model(test_input_batch)
    pred_cls = tf.argmax(pred_logits, 1)
    metric_args = {
        "eval/mean_clf_accuracy":
        slim.metrics.streaming_accuracy(pred_cls, test_label_batch)
    }
    base_model.test_model_given_metrics(metric_args, test_params)

  def predict(self, input_data, preprocessed=True):
    """Get prediction value from a tensor.

    Args:
      input_data: raw inputs as numpy array to predict.
      preprocessed: if data has been preprocessed.
    Returns:
      two matrices with each row for each sample and
    ranked label id and probability.
    """
    # self.dm_model.use_graph()
    pred_logits = self.get_outputs(
        input_data,
        preprocessed=preprocessed,
        target_tensor_names=[self.model_pred_tensor_name])
    pred_probs = np.exp(pred_logits) / np.sum(np.exp(pred_logits))
    # pred_prob_tensor = tf.nn.softmax(output_tensor)
    assert len(pred_probs) == 1, "classifier prediction is not valid"
    pred_probs = pred_probs[0]
    sorted_pred_labels = np.argsort(pred_probs, axis=1)[:, ::-1]
    sorted_pred_probs = np.sort(pred_probs, axis=1)[:, ::-1]
    return sorted_pred_labels, sorted_pred_probs
