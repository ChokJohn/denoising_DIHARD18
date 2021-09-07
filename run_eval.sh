#!/bin/bash
# This script demonstrates how to run speech enhancement and VAD. For full documentation,
# please consult the docstrings of ``main_denoising.py`` and ``main_get_vad.py``.

# There is no need for doing any further enhancemnt on librispeech, which is already clean data.


###################################
# Perform VAD using enhanced audio
###################################

wav_scp=path/to/train-clean/wav.scp
scpf=train-clean.scp
awk -F "{print $6}" $wav_scp> $scpf

VAD_DIR=vad/train-clean  # Output directory for label files containing VAD output.
HOPLENGTH=30  # Duration in milliseconds of frames for VAD. Also controls step size.
MODE=3  # WebRTC aggressiveness. 0=least agressive and  3=most aggresive.
NJOBS=1  # Number of parallel processes to use.
python main_get_vad.py \
       --verbose -S $scpf\
       --wav_dir $SE_WAV_DIR --output_dir $VAD_DIR \
       --mode $MODE --hoplength $HOPLENGTH \
       --n_jobs $NJOBS || exit 1
python make_meta.py \
      --vad_path $VAD_DIR\
      --output_dir train-clean_seg\
      --wav_scp $wav_scp

wav_scp=path/to/dev-clean/wav.scp
scpf=dev-clean.scp
awk -F "{print $6}" $wav_scp> $scpf

python main_get_vad.py \
       --verbose -S $scpf\
       --wav_dir $SE_WAV_DIR --output_dir $VAD_DIR \
       --mode $MODE --hoplength $HOPLENGTH \
       --n_jobs $NJOBS || exit 1
python make_meta.py \
      --vad_path $VAD_DIR\
      --output_dir dev-clean_seg\
      --wav_scp $wav_scp

# copy dev-clean_seg and  train-clean_seg  to  EEND/egs/minilibrispeech/v1/data/
