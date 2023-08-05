"""Base model for deep models.
"""

import os
import glob

import tensorflow as tf
import tensorflow.contrib.slim as slim

from .. import commons


def print_variable_names(var_list=None, list_name=""):
  """Print variable names from a given collection.

  Args:
    var_list: list of variables.
    list_name: name of the list.
  """
  if var_list is None:
    var_list = tf.all_variables()
    if not var_list:
      print "no variable in current graph."
      return
  print "Here are all the variables in list {}:".format(list_name)
  for cur_var in var_list:
    print cur_var.name


def count_trainable_param_number():
  """Count total number of parameters of trainable parameters.
  """
  total_parameters = 0
  for variable in tf.trainable_variables():
    # shape is an array of tf.Dimension
    shape = variable.get_shape()
    variable_parametes = 1
    for dim in shape:
      variable_parametes *= dim.value
    total_parameters += variable_parametes
  return total_parameters


def train_model_given_loss(loss,
                           variables_to_train,
                           train_params,
                           init_fn=None):
  """Train model give na total loss.

  Args:
    train_data: packed train data batch.
    loss: the loss to optimize.
    variables_to_train: if none, train all.
    train_params: params for training.
    init_fn: initialize function, e.g. load pretrained models.
  """
  # create log dir.
  if not os.path.exists(train_params.train_log_dir):
    os.makedirs(train_params.train_log_dir)
  # Specify the optimization scheme.
  global_step = slim.get_or_create_global_step()
  learning_rate = tf.train.exponential_decay(
      train_params.init_learning_rate,
      global_step,
      train_params.decay_steps,
      train_params.decay_rate,
      staircase=True)
  if train_params.opt_method == commons.OPTMethod.SGD:
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
  if train_params.opt_method == commons.OPTMethod.MOMENTUM:
    optimizer = tf.train.MomentumOptimizer(learning_rate,
                                           train_params.momentum)
  if train_params.opt_method == commons.OPTMethod.ADAM:
    optimizer = tf.train.AdamOptimizer(
        train_params.init_learning_rate, epsilon=1.0)
  if train_params.opt_method == commons.OPTMethod.ADAGRAD:
    optimizer = tf.train.AdagradOptimizer(train_params.init_learning_rate)
  if train_params.opt_method == commons.OPTMethod.ADADELTA:
    optimizer = tf.train.AdadeltaOptimizer(train_params.init_learning_rate)
  if train_params.opt_method == commons.OPTMethod.FTRL:
    optimizer = tf.train.FtrlOptimizer(train_params.init_learning_rate)
  if train_params.opt_method == commons.OPTMethod.RMSPROP:
    optimizer = tf.train.RMSPropOptimizer(
        train_params.init_learning_rate, momentum=0.9, epsilon=1.0)

  tf.scalar_summary("learning rate", learning_rate)
  tf.scalar_summary("batch size", train_params.batch_size)
  tf.scalar_summary("losses/total_loss", loss)

  # Set up training.
  train_op = slim.learning.create_train_op(
      loss,
      optimizer,
      global_step=global_step,
      variables_to_train=variables_to_train)
  tf.merge_all_summaries()

  # Run training.
  print "Start training. Good Luck!"
  slim.learning.train(
      train_op=train_op,
      init_fn=init_fn,
      logdir=train_params.train_log_dir,
      is_chief=train_params.task_id == 0,
      number_of_steps=train_params.max_steps,
      log_every_n_steps=10,
      save_summaries_secs=train_params.save_summaries_secs,
      save_interval_secs=train_params.save_interval_secs)


def test_model_given_metrics(metric_args, test_params):
  """Evaluate model given metrics.

  Args:
    metric_args: computed metrics.
    test_params: params for testing.
  """
  # Choose the metrics to compute.
  metrics = slim.metrics.aggregate_metric_map(metric_args)
  names_to_vals, names_to_updates = metrics

  summary_ops = []
  for metric_name, metric_value in names_to_vals.iteritems():
    op = tf.scalar_summary(metric_name, metric_value)
    op = tf.Print(op, [metric_value], metric_name)
    summary_ops.append(op)

  print "starting test loop..."
  slim.evaluation.evaluation_loop(
      "",
      test_params.train_log_dir,
      test_params.test_log_dir,
      num_evals=test_params.max_steps,
      eval_op=names_to_updates.values(),
      summary_op=tf.merge_summary(summary_ops),
      eval_interval_secs=test_params.eval_secs)


def save_model(ckpt_fn, variables_to_save=None, global_step=0):
  """Save model weights.

  Assuming the model graph has been built.

  Args:
    ckpt_fn: checkpoint file path.
    variables_to_save: a list of variables or a name mapping dictionary.
    global_step: step number.
  """
  if variables_to_save is None:
    saver = tf.train.Saver()
  else:
    saver = tf.train.Saver(variables_to_save)
  with tf.Session() as sess:
    saver.save(sess, ckpt_fn, global_step=global_step)
    print "model saved to {}".format(ckpt_fn)


# deprecated since loading is tied to a specific session.
def load_model(ckpt_dir, variables_to_restore=None):
  """Load model weights.

  Assuming the model graph has been built.

  Args:
    ckpt_dir: checkpoint directory.
    variables_to_restore: which variables to load from checkpoint.
  """
  if not os.path.exists(ckpt_dir):
    print "checkpoint dir {} not exist.".format(ckpt_dir)
    return

  ckpts = glob.glob(os.path.join(ckpt_dir, "*.ckpt*"))
  ckpt = ckpts[0]

  if variables_to_restore is None:
    saver = tf.train.Saver()
  else:
    saver = tf.train.Saver(variables_to_restore)
  with tf.Session() as sess:
    # ckpt = tf.train.latest_checkpoint(ckpt_dir)
    if ckpt:
      saver.restore(sess, ckpt)
      print "model loaded from {}".format(ckpt)
    else:
      print "unable to load model from {}".format(ckpt)
  # another way.
  # slim.assign_from_checkpoint_fn(
  #     ckpt,
  #     variables_to_restore,
  #     ignore_missing_vars=True)


def eval_tensor(sess, input_tensor_name, input_val, output_tensor_name):
  """Get output value of a specific tensor.

  Assuming the default graph is used.

  Args:
    sess: tf session object.
    input_tensor_name: name of the input tensor.
    input_val: input value to the network.
    output_tensor_name: name of the output tensor.
  Returns:
    result of output tensor.
  """
  cur_graph = tf.get_default_graph()
  input_tensor = cur_graph.get_tensor_by_name(input_tensor_name)
  output_tensor = cur_graph.get_tensor_by_name(output_tensor_name)
  out_val = output_tensor.eval(
      session=sess, feed_dict={input_tensor: input_val})
  return out_val


class BaseDeepModel(object):
  """Base class for deep models.

  This class serves as the base class for custom
  deep models. To define a new model, just inherit
  from it and implement corresponding methods. All tasks
  related to a particular model are to be included.

  Attributes:
    net_outputs: model output from inputs.
    net_endpoints: dictionary keyed with layer names.
    used for training, taking input queue as input.
    test_net: similar with train, but use placeholder
    as input for prediction.
  """
  net_outputs = None
  net_endpoints = None

  def __init__(self):
    pass

  def build_model(self, inputs, model_params):
    """Construct model architecture.

    Args:
      inputs: input data.
      model_params: parameters related to model.
    """
    pass
