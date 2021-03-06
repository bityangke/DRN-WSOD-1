#!/usr/bin/env python3

# Copyright (c) 2017-present, Facebook, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################

"""Train a network with Detectron."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import cv2  # NOQA (Must import before importing caffe2 due to bug in cv2)
import logging
import numpy as np
import pprint
import sys

from caffe2.python import workspace

from detectron.core.config import assert_and_infer_cfg
from detectron.core.config import cfg
from detectron.core.config import merge_cfg_from_file
from detectron.core.config import merge_cfg_from_list
from detectron.core.test_engine_wsl_vis import run_inference
from detectron.utils.logging import setup_logging
import detectron.utils.c2 as c2_utils
import detectron.utils.train_wsl

c2_utils.import_contrib_ops()
c2_utils.import_detectron_ops()
c2_utils.import_custom_ops()

# OpenCL may be enabled by default in OpenCV3; disable it because it's not
# thread safe and causes unwanted GPU memory allocations.
cv2.ocl.setUseOpenCL(False)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Train a network with Detectron'
    )
    parser.add_argument(
        '--cfg',
        dest='cfg_file',
        help='Config file for training (and optionally testing)',
        default=None,
        type=str
    )
    parser.add_argument(
        '--multi-gpu-testing',
        dest='multi_gpu_testing',
        help='Use cfg.NUM_GPUS GPUs for inference',
        action='store_true'
    )
    parser.add_argument(
        '--skip-test',
        dest='skip_test',
        help='Do not test the final model',
        action='store_true'
    )
    parser.add_argument(
        'opts',
        help='See detectron/core/config.py for all options',
        default=None,
        nargs=argparse.REMAINDER
    )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


def main():
    # Initialize C2
    workspace.GlobalInit(
        ['caffe2', '--caffe2_log_level=0', '--caffe2_gpu_memory_tracking=1']
    )
    # Set up logging and load config options
    logger = setup_logging(__name__)
    logging.getLogger('detectron.roi_data.loader').setLevel(logging.INFO)
    args = parse_args()
    logger.info('Called with args:')
    logger.info(args)
    if args.cfg_file is not None:
        merge_cfg_from_file(args.cfg_file)
    if args.opts is not None:
        merge_cfg_from_list(args.opts)
    assert_and_infer_cfg()
    smi_output, cuda_ver, cudnn_ver = c2_utils.get_nvidia_info()
    logger.info("cuda version : {}".format(cuda_ver))
    logger.info("cudnn version: {}".format(cudnn_ver))
    logger.info("nvidia-smi output:\n{}".format(smi_output))
    logger.info('Training with config:')
    logger.info(pprint.pformat(cfg))
    # Note that while we set the numpy random seed network training will not be
    # deterministic in general. There are sources of non-determinism that cannot
    # be removed with a reasonble execution-speed tradeoff (such as certain
    # non-deterministic cudnn functions).
    np.random.seed(cfg.RNG_SEED)
    # Execute the training run
    checkpoints = detectron.utils.train_wsl.train_model()
    # Test the trained model
    if not args.skip_test:
        # test_model(checkpoints['final'], args.multi_gpu_testing, args.opts)
        # print('reprint snapshot name for the result: ', checkpoints['final'])

        if 'voc_' in cfg.TRAIN.DATASETS[0]:
            TEST_DATASETS = cfg.TEST.DATASETS
            TEST_PROPOSAL_FILES = cfg.TEST.PROPOSAL_FILES
            cfg.immutable(False)
            cfg.TEST.DATASETS = cfg.TRAIN.DATASETS
            cfg.TEST.PROPOSAL_FILES = cfg.TRAIN.PROPOSAL_FILES
            cfg.immutable(True)
            test_model(checkpoints['final'], args.multi_gpu_testing, args.opts)
            print('reprint snapshot name for the result: ', checkpoints['final'])

            cfg.immutable(False)
            cfg.TEST.DATASETS = TEST_DATASETS
            cfg.TEST.PROPOSAL_FILES = TEST_PROPOSAL_FILES
            cfg.immutable(True)

        cfg.immutable(False)
        cfg.TEST.BBOX_AUG.ENABLED = False
        cfg.VIS = False
        cfg.immutable(True)

        # _ = checkpoints.pop('final', None)
        # for snapshot in sorted(checkpoints.keys(), reverse=True):
            # test_model(checkpoints[snapshot], args.multi_gpu_testing, args.opts)
            # print('reprint snapshot name for the result: ', snapshot, checkpoints[snapshot])


def test_model(model_file, multi_gpu_testing, opts=None):
    """Test a model."""
    # Clear memory before inference
    workspace.ResetWorkspace()
    # Run inference
    run_inference(
        model_file, multi_gpu_testing=multi_gpu_testing,
        check_expected_results=True,
    )


if __name__ == '__main__':
    main()
