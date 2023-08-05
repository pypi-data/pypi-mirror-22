"""Data providers for various datasets.
"""

import csv
import glob
import os
import random

import tensorflow as tf

from .. import commons
import common_flags
from deepmodels.tools import data_manager as data_man

flags = tf.app.flags
FLAGS = flags.FLAGS


def load_img_fns(img_dir,
                 img_width,
                 img_height,
                 img_format=commons.ImgFormat.PNG,
                 scaling=True,
                 preprocess_fn=None):
  """Load all image from given files to tf tensor.

  Args:
    img_fns: file names for images.
    img_width: image width.
    img_height: image height.
    img_format: format of image file.
    scaling: scale pixel values.
    preprocess_fn: function for preprocessing.
  Returns:
    imgs: loaded image data.
    img_fns: image file names for logging.
  """
  img_format_str = "*.jpg" if img_format == commons.ImgFormat.JPG else "*.png"
  img_fns = glob.glob(os.path.join(img_dir, img_format_str))
  img_data = []
  for img_fn in img_fns:
    value = tf.read_file(img_fn)
    if img_format == commons.ImgFormat.JPG:
      img_content = tf.image.decode_jpeg(value, channels=3)
    if img_format == commons.ImgFormat.PNG:
      img_content = tf.image.decode_png(value, channels=3)
    img_content = tf.to_float(img_content)
    if scaling:
      img_content = tf.mul(img_content, (1.0 / 255))
    if preprocess_fn is None:
      img_content = tf.image.resize_images(img_content,
                                           (img_width, img_height))
    else:
      img_content = preprocess_fn(img_content, img_height, img_width)
    img_data.append(img_content)
  imgs = tf.pack(img_data)
  return imgs, img_fns


def gen_clf_metadata_from_img_fns(img_dir,
                                  save_fn_prefix,
                                  img_format=commons.ImgFormat.JPG,
                                  train_ratio=0.8):
  """Generate csv files for training and testing data.

  The images are organized by categories in
  each folder. Allow consistent data split and train/test loop.

  Args:
    img_dir: root directory. Each subfolder is a category.
    save_fn_prefix: prefix for saved files. train and test.
    files will have corresponding suffix appended.
    img_format: jpg or png.
    train_ratio: ratio between train and test data.
  """
  # list all category directories.
  cate_dirs = os.listdir(img_dir)
  cate_dirs = [os.path.join(img_dir, x) for x in cate_dirs]
  cate_dirs = [x for x in cate_dirs if os.path.isdir(x)]
  img_ext = "*.png"
  if img_format == commons.ImgFormat.JPG:
    img_ext = "*.jpg"
  train_data = []
  test_data = []
  label_names = []

  # list image files.
  for cate_id, cur_cate_dir in enumerate(cate_dirs):
    cur_cate_name = os.path.basename(cur_cate_dir.strip("/"))
    label_names.append(cur_cate_name)
    cur_fns = glob.glob(os.path.join(cur_cate_dir, img_ext))
    random.shuffle(cur_fns)
    total_fn_num = len(cur_fns)
    all_labels = [cate_id] * total_fn_num
    train_fn_num = int(total_fn_num * train_ratio)
    train_data.extend(zip(cur_fns[:train_fn_num], all_labels[:train_fn_num]))
    test_data.extend(zip(cur_fns[train_fn_num:], all_labels[train_fn_num:]))

  # write to files.
  train_fn = data_man.gen_data_filename(save_fn_prefix,
                                        commons.DataFileType.DATA_TRAIN)
  test_fn = data_man.gen_data_filename(save_fn_prefix,
                                       commons.DataFileType.DATA_TEST)
  label_fn = data_man.gen_data_filename(save_fn_prefix,
                                        commons.DataFileType.DATA_LABEL)
  with open(train_fn, "w") as f:
    writer = csv.writer(f)
    writer.writerows(train_data)
    print "train data has been written to file: {}".format(train_fn)
  with open(test_fn, "w") as f:
    writer = csv.writer(f)
    writer.writerows(test_data)
    print "test data has been written to file: {}".format(test_fn)
  with open(label_fn, "w") as f:
    for cur_label in label_names:
      f.write("{}\n".format(cur_label))
    print "label data has been written to file: {}".format(label_fn)


def gen_triplet_metadata_from_img_fns(img_dir,
                                      save_fn_prefix,
                                      img_format=commons.ImgFormat.JPG,
                                      train_ratio=0.8):
  """Generate csv file containing image triplet.

  Args:
    img_dir: root directory. Each subfolder is a category.
    save_fn_prefix: prefix for saved files.
    img_format: jpg or png.
    train_ratio: 0.8.
  """
  # list all category directories.
  cate_dirs = os.listdir(img_dir)
  cate_dirs = [os.path.join(img_dir, x) for x in cate_dirs]
  cate_dirs = [x for x in cate_dirs if os.path.isdir(x)]
  img_ext = "*.png"
  if img_format == commons.ImgFormat.JPG:
    img_ext = "*.jpg"
  train_data = []
  test_data = []
  label_names = []
  # list image files.
  for cate_id, cur_cate_dir in enumerate(cate_dirs):
    cur_cate_name = os.path.basename(cur_cate_dir.strip("/"))
    label_names.append(cur_cate_name)
    cur_fns = glob.glob(os.path.join(cur_cate_dir, img_ext))
    random.shuffle(cur_fns)
    total_fn_num = len(cur_fns)
    all_labels = [cate_id] * total_fn_num
    train_fn_num = int(total_fn_num * train_ratio)
    train_data.extend(zip(cur_fns[:train_fn_num], all_labels[:train_fn_num]))
    test_data.extend(zip(cur_fns[train_fn_num:], all_labels[train_fn_num:]))


def clf_input_from_image_fns(meta_fn,
                             img_depth=3,
                             img_width=224,
                             img_height=224,
                             batch_size=16,
                             scaling=False,
                             preprocess_fn=None,
                             shuffle=True):
  """Feed images from files.
  Args:
    meta_fn: file of the metadata.
    img_depth: number of channels.
    img_width: width of target image.
    img_height: height of target image.
    batch_size: size of each batch.
    scaling: whether to scale pixel to [0,1].
    preprocess_fn: preprocessing function, <img_data, height, width>.
    shuffle: whether to shuffle or not.
  Returns:
    input queue for batch data.
  """
  # probing
  samp_num = 0
  cls_num = 0
  img_ext = "jpg"
  img_fns = []
  img_labels = []
  with open(meta_fn, "r") as f:
    reader = csv.reader(f)
    for row in reader:
      samp_num += 1
      img_ext = row[0][-3:]
      img_fns.append(row[0])
      img_labels.append(int(row[1]))
    cls_num = len(set(img_labels))

  # build input queue from csv file.
  # filename_queue = tf.train.string_input_producer([meta_fn])
  # text_reader = tf.TextLineReader()
  # _, records = text_reader.read(filename_queue)
  # # decode csv content.
  # record_defaults = [tf.constant([], dtype=tf.string),
  #                    tf.constant([], dtype=tf.int64)]
  # img_fn, img_label = tf.decode_csv(records, record_defaults=record_defaults)

  img_fn_tensor = tf.convert_to_tensor(img_fns, tf.string)
  img_label_tensor = tf.convert_to_tensor(img_labels, tf.int64)
  img_fn, img_label = tf.train.slice_input_producer(
      [img_fn_tensor, img_label_tensor],
      num_epochs=None,
      shuffle=True,
      seed=161803)

  # read image.
  img_content = tf.read_file(img_fn)
  if img_ext == "png":
    img_data = tf.image.decode_png(img_content, img_depth)
  if img_ext == "jpg":
    img_data = tf.image.decode_jpeg(img_content, img_depth)
  img_data = tf.to_float(img_data)
  if scaling:
    img_data = tf.mul(img_data, (1.0 / 255))
  # preprocessing.
  if preprocess_fn is not None:
    img_data = preprocess_fn(img_data, img_height, img_width)
  else:
    img_data = tf.image.resize_images(img_data, (img_height, img_width))
  # create batch
  if shuffle:
    img_batch, label_batch, fn_batch = tf.train.shuffle_batch(
        [img_data, img_label, img_fn],
        batch_size=batch_size,
        capacity=batch_size * 50,
        min_after_dequeue=batch_size * 20)
  else:
    img_batch, label_batch, fn_batch = tf.train.batch(
        [img_data, img_label, img_fn],
        batch_size=batch_size,
        capacity=batch_size * 20)
  return img_batch, label_batch, fn_batch, samp_num, cls_num


def main(_):
  gen_clf_metadata_from_img_fns(
      FLAGS.img_dir, FLAGS.save_prefix, train_ratio=FLAGS.train_ratio)


if __name__ == "__main__":
  tf.app.run()
