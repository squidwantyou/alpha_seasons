#!/bin/bash
source ~/.bashrc

conda activate base

cd /home/ffallrain/alpha_seasons/housekeeping_download/
python /home/ffallrain/alpha_seasons/housekeeping_download/housekeeping_downloader.py
cd /tmp
