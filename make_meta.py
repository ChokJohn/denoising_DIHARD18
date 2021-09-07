import os
from collections import defaultdict
import argparse

parser = argparse.ArgumentParser(
    description='Perform VAD using webrtcvad.', add_help=True)
parser.add_argument(
    '--vad_path', nargs=None, type=str, metavar='STR',
    help='output directory for label files (default: None)')
parser.add_argument(
    '--output_dir', nargs=None, type=str, metavar='STR',
    help='output directory for kaldi style meta files')
parser.add_argument(
    '--wav_scp', nargs=None, type=str, metavar='STR',
    help='wav.scp for dataset')

vad_path = parser.vad_path
save_path = parser.output_dir
wav_scp_path = parser.wav_scp
wav_scp = {}
with open(wav_scp_path,'r') as fh:
    for i,line in enumerate( fh.readlines()) :
        name = os.path.basename(line.strip()).strip('.flac')
        wav_scp[name] = line.strip()

os.makedirs(save_path,exist_ok=True)
os.chdir(vad_path)
files=os.listdir()
data = []
for file in files:
     with open(file,'r') as fh:
         for i,line in enumerate( fh.readlines()) :
             st,et = line.strip().split()
             st = int(float(st)*100)/100
             et = int(float(et)*100)/100
             recor = file.split('.')[0]
             uuid= '%s-%07d-%07d'%(recor,st*100,et*100)
             data.append([uuid,recor,st,et])
os.chdir('../..')
# segments
with open(save_path+'/segments','w') as fh:
    for line in data:
        line = [str(i) for i in line]
        line = ' '.join(line) +'\n'
        fh.write(line)
# wav.scp
with open(save_path+'/wav.scp','w') as fh:
    for line in data:
        wav = line[1]
        path = wav_scp[wav]
        fh.write(wav+' ' + path+'\n')
# utt2spk
spk2utt = defaultdict(list)
with open(save_path+'/utt2spk','w') as fh:
    for line in data:
        wav = line[1]
        utt = line[0]