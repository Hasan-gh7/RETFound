## RETFound - A foundation model for retinal images

### Source-only GitHub distribution

This repository publishes source code and documentation. Model weights and
checkpoints, dataset archives, benchmark data and saved results, historical source
exports, and local Python environments are excluded by `.gitignore`; original
local files are retained. Evaluation scripts remain part of the source code.
Git LFS is not required for the included source files and small images.

A fresh clone is not a ready-to-run model installation. Supply the trusted APTOS
classifier locally at `checkpoints/APTOS2019/checkpoint-best.pth` (or the supported
nested layout), set up the model/API dependencies, and provide any optional
datasets or saved results separately. The 15-image dataset demo requires the
excluded `upload_test_images/` assets. Older run reports and local setup claims
below describe the original workspace, not files bundled in a fresh clone.
Keep credentials in the local environment and never commit them. The provider
credential previously embedded in documentation has been removed; its owner
should revoke/replace it if it is still active. No revocation was performed here.

For the folder layout and cleanup decisions, see [Folder guide](docs/FOLDER_GUIDE.md).
Historical ZIP snapshots and generated source exports are organized under `archive/`.

### Retinal image web application and local API

Double-click **`run_web.bat`** to open the new web application at
<http://127.0.0.1:8000>. Upload or drag in a retinal image, run analysis, inspect
the predicted grade and all five model scores, and download the result as JSON.
The workspace also shows the saved evaluation and API integration examples.

**Jev fundus check:** uploads must be identified as retinal fundus photographs
before RETFound runs. Set `OPENROUTER_API_KEY` in the server environment and restart
the server; see [setup instructions](docs/API.md#jev-retinal-fundus-gate).
Images are sent to OpenRouter/TypeSafe. Missing credentials or provider failures
block predictions. Automated screening accuracy has not been validated.

Use **Dataset tests** in the web app, or open
[the local dataset test page](http://127.0.0.1:8000/dataset-tests), to test the 15
labeled IDRiD, MESSIDOR2 and DDR examples individually or sequentially. It displays
reference and predicted grades, five scores, and a JSON session download. Clicking
a test sends images to Jev through OpenRouter; opening the page does not.

Another application on this computer can send an image directly:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/predict" -F "image=@C:/images/retina.jpg"
```

Keep the server window open while using it. The existing classifier loads once,
and the same inference service powers the web page and API. Uploads stay in memory.
The interface and its assets work locally without an external font/CDN service.
Predictions are research outputs, not clinical diagnoses.

API dependencies are already installed in `.runtime/web`, separately from the
working model environment. On a fresh setup, run `setup_web.bat` first.
See [API documentation](docs/API.md) for raw-image requests, Python examples,
limits, response fields, error handling, browser CORS configuration and tests.

### APTOS 1,000-image evaluation software

The new local evaluator audits your labeled `APTOS2019.zip`, selects exactly
1,000 eligible **test** images with seed `20261023`, runs the existing classifier,
and creates an offline viewer with images, true labels, predicted grades, five
uncalibrated scores, filters, a confusion matrix, and CSV/JSON downloads.
The image-upload API is now available separately above. No training or package installation is needed
in the verified `ml-homework` environment.

Double-click `run_aptos_evaluation.bat`, or run it from PowerShell:

```powershell
.\run_aptos_evaluation.bat
```

The launcher uses the ZIP beside it and opens the completed report. Each run gets
a new directory under `results/runs/`; old results are never overwritten.
To use a different ZIP or extracted folder, an explicit device/count, or a new output directory:

```powershell
$retfoundPython = Join-Path $env:USERPROFILE '.conda\envs\ml-homework\python.exe'
& $retfoundPython -B scripts/evaluate_aptos.py 'APTOS2019.zip' --count 1000 --device cuda --open-report
```

Folder/ZIP layout: `[optional dataset folder]/train|val|test/<grade>/<image>`.
Grades may be `0` through `4` or the established named folders `anodr`, `bmilddr`,
`cmoderatedr`, `dseveredr`, `eproliferativedr`/`eprodr`. `validation` is accepted
as `val`. CSV-labeled flat folders are not supported in this version.
Paths in manifests use portable `/` separators; absolute source/checkpoint paths
are recorded separately as local provenance.

Each run includes `audit.json`, `selection.json`, `predictions.json`,
`predictions.csv`, `index.html`, and a completion or failure marker. The audit
decodes and hashes all recognized images, rejects unsafe ZIP paths/links and
unknown labels, excludes conflicting-label groups and test/train/validation
exact-byte overlap, then retains one stable representative per duplicate test
hash. No images are extracted or modified. Oversized requests fail explicitly.
Test-only or incomplete evidence records overlap as unverified. Exact-byte checks
do not establish patient independence, near-duplicate absence, or the checkpoint's
original training split. These are research model predictions, not diagnoses.

Separate validation and selection (use new output paths):

```powershell
& $retfoundPython -B scripts/validate_dataset.py 'APTOS2019.zip' --output results/runs/my-audit/audit.json
& $retfoundPython -B scripts/sample_dataset.py results/runs/my-audit/audit.json --count 1000 --output results/runs/my-audit/selection.json
& $retfoundPython -B -m unittest discover -s tests -v
```

The evaluator always performs its own fresh audit before inference. Standalone
selection does not load the model. Optional real-checkpoint verification:

```powershell
& $retfoundPython -B scripts/verify_inference.py --output results/runs/my-check/inference-verification.json
```

This optional check requires CUDA and also exercises one CPU prediction. It compares
all 34 historical APTOS predictions and the independently verified baseline sample.
See `docs/PROGRESS.md` for actual run results and remaining limitations.

### Local 100-image DR evaluation report

Run in PowerShell from this folder:

```powershell
.\run_benchmark.bat
```

This uses `ml-homework` and the existing APTOS2019 checkpoint. It downloads
34 APTOS2019, 33 IDRiD, and 33 MESSIDOR2 images from the official RETFound
Google Drive **test** folders, then runs actual inference. Sampling is uniform
without replacement with seed `20261023`; hidden notebook copies are excluded.
`gdown` and `scikit-learn` are needed in addition to the prediction dependencies.

Open `results/benchmark100/index.html` for the offline report. Its image gallery
includes dataset ground-truth grades, predictions, all five softmax scores,
dataset/outcome/grade filters, confusion matrices, and CSV export.
`predictions.csv` and `predictions.json` contain machine-readable results.
Source manifests and original sampled images are retained in `benchmark_data`.
Already downloaded samples are reused on subsequent runs.

The same five-grade APTOS-trained model is used on all three datasets. Any-DR
detection means predicted grade 1–4 versus grade 0. PAPILA is excluded because
its ground truth concerns glaucoma rather than DR. These small-sample results
are not full benchmark scores; IDRiD and MESSIDOR2 measure transfer performance.

### Windows prediction with a separately supplied APTOS checkpoint

From PowerShell in this folder, run the included sample:

```powershell
.\run_prediction.bat
```

To predict a different image:

```powershell
.\run_prediction.bat "C:\path\to\retinal-image.jpg"
```

The launcher uses `%USERPROFILE%\.conda\envs\ml-homework\python.exe`
and `predict_aptos.py`. The prediction script
supports both `checkpoints/APTOS2019/checkpoint-best.pth` and the nested
`checkpoints/checkpoints/APTOS2019/checkpoint-best.pth` extraction layout.
It selects CUDA, Apple MPS, or CPU according to availability; pass `--cpu`
after the image path to force CPU execution.

To run directly from the existing `ml-homework` environment:

```powershell
conda activate ml-homework
python predict_aptos.py sample_images/idrid_test.jpg
```

Single-image prediction requires PyTorch, torchvision, and timm (0.9.16).
Training setup is documented
below. The copied macOS `.venv` cannot be used on Windows.


Official repo including a series of foundation models and applications for retinal images.<br>
`[RETFound-MAE]`:[RETFound: a foundation model for generalizable disease detection from retinal images](https://www.nature.com/articles/s41586-023-06555-x).<br>
`[RETFound-DINOv2]`:[Revealing the Impact of Pre-training Data on Medical Foundation Models](https://www.researchsquare.com/article/rs-6080254/v1).<br>
`[DINOv2]`:[General-purpose vision foundation models DINOv2 by Meta](https://github.com/facebookresearch/dinov2).<br>
`[DINOv3]`:[General-purpose vision foundation models DINOv3 by Meta](https://github.com/facebookresearch/dinov3).<br>


Please contact 	**ykzhoua@gmail.com** or **yukun.zhou.19@ucl.ac.uk** if you have questions.


### 📝Key features

- RETFound is pre-trained on 1.6 million retinal images with self-supervised learning
- RETFound has been validated in multiple disease detection tasks
- RETFound can be efficiently adapted to customised tasks


### 🎉News

- 🐉2025/09: **Preprint benchmarking DINOv3, DINOv2, and RETFound is [available](https://arxiv.org/abs/2509.03421)!**
- 🐉2025/09: **We included state-of-the-art DINOv3 into fine-tuning pipeline for retinal applications!**
- 🐉2025/02: **We organised the model weights on HuggingFace, no more manual downloads needed!**
- 🐉2025/02: **Multiple [pre-trained weights](https://huggingface.co/YukunZhou), including MAE-based and DINOV2-based, are added!**
- 🐉2025/02: **We update the version of packages, such as CUDA12+ and PyTorch 2.3+!**
- 🐉2024/01: [Feature vector notebook](https://github.com/rmaphoh/RETFound_MAE/blob/main/latent_feature.ipynb) are now online!
- 🐉2024/01: [Data split and model checkpoints](BENCHMARK.md) for public datasets are now online!
- 🎄2023/12: [Colab notebook](https://colab.research.google.com/drive/1_X19zdMegmAlqPAEY0Ao659fzzzlx2IZ?usp=sharing) is now online - free GPU & simple operation!


### 🔧Install environment

1. Create environment with conda:

```
conda create -n retfound python=3.11.0 -y
conda activate retfound
```

2. Install dependencies

```
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121
git clone https://github.com/rmaphoh/RETFound/
cd RETFound
pip install -r requirements.txt
pip install ipykernel
python -m ipykernel install --user --name retfound --display-name "Python (retfound)"
```


### 🌱Fine-tuning with RETFound weights

1. Get access to the pre-trained models on HuggingFace (register an account and fill in the form) and go to step 2:
<table><tbody>
<!-- START TABLE -->
<!-- TABLE HEADER -->
<th valign="bottom"></th>
<th valign="bottom">ViT-Large</th>
<th valign="bottom">Source</th>
<!-- TABLE BODY -->
<tr><td align="left">RETFound_mae_natureCFP</td>
<td align="center"><a href="https://huggingface.co/YukunZhou/RETFound_mae_natureCFP">access</a></td>
<td align="center"><a href="https://www.nature.com/articles/s41586-023-06555-x">Nature RETFound paper</a></td>
</tr>
<!-- TABLE BODY -->
<tr><td align="left">RETFound_mae_natureOCT</td>
<td align="center"><a href="https://huggingface.co/YukunZhou/RETFound_mae_natureOCT">access</a></td>
<td align="center"><a href="https://www.nature.com/articles/s41586-023-06555-x">Nature RETFound paper</a></td>
</tr>
<!-- TABLE BODY -->
<tr><td align="left">RETFound_mae_meh</td>
<td align="center"><a href="https://huggingface.co/YukunZhou/RETFound_mae_meh">access</a></td>
<td align="center"><a href="https://www.researchsquare.com/article/rs-6080254/v1">FM data paper</a></td>
</tr>
<!-- TABLE BODY -->
<tr><td align="left">RETFound_mae_shanghai</td>
<td align="center"><a href="https://huggingface.co/YukunZhou/RETFound_mae_shanghai">access</a></td>
<td align="center"><a href="https://www.researchsquare.com/article/rs-6080254/v1">FM data paper</a></td>
</tr>
<!-- TABLE BODY -->
<tr><td align="left">RETFound_dinov2_meh</td>
<td align="center"><a href="https://huggingface.co/YukunZhou/RETFound_dinov2_meh">access</a></td>
<td align="center"><a href="https://www.researchsquare.com/article/rs-6080254/v1">FM data paper</a></td>
</tr>
<!-- TABLE BODY -->
<tr><td align="left">RETFound_dinov2_shanghai</td>
<td align="center"><a href="https://huggingface.co/YukunZhou/RETFound_dinov2_shanghai">access</a></td>
<td align="center"><a href="https://www.researchsquare.com/article/rs-6080254/v1">FM data paper</a></td>
</tr>
</tbody></table>

2. Login in your HuggingFace account, where HuggingFace token can be [created and copied](https://huggingface.co/settings/tokens).
```
huggingface-cli login --token YOUR_HUGGINGFACE_TOKEN
```

**Optional**: if your machine and server cannot access HuggingFace due to internet wall, run the command below (Do not run it if you can access):
```
export HF_ENDPOINT=https://hf-mirror.com
```

3. If you would like to fine-tune [DINOv2](https://github.com/facebookresearch/dinov2) and [DINOv3](https://github.com/facebookresearch/dinov3), please visit their GitHub repositories to download the model weights and put them in the RETFound folder.

4. Organise your data into this directory structure (Public datasets used in this study can be [downloaded here](BENCHMARK.md))

```
├── data folder
    ├──train
        ├──class_a
        ├──class_b
        ├──class_c
    ├──val
        ├──class_a
        ├──class_b
        ├──class_c
    ├──test
        ├──class_a
        ├──class_b
        ├──class_c
``` 



5. Start fine-tuning by running `sh train.sh`.


In `train.sh`, the model can be selected by changing the hyperparameters `MODEL`, `MODEL_ARCH`, `FINETUNE`:

**RETFound**:

| MODEL           | MODEL_ARCH               | FINETUNE                 | SIZE                     |
|-----------------|--------------------------|--------------------------|--------------------------|
| RETFound_mae    | retfound_mae             | RETFound_mae_natureCFP   | ~300M                    |
| RETFound_mae    | retfound_mae             | RETFound_mae_natureOCT   | ~300M                    |
| RETFound_mae    | retfound_mae             | RETFound_mae_meh         | ~300M                    |
| RETFound_mae    | retfound_mae             | RETFound_mae_shanghai    | ~300M                    |
| RETFound_dinov2 | retfound_dinov2          | RETFound_dinov2_meh      | ~300M                    |
| RETFound_dinov2 | retfound_dinov2          | RETFound_dinov2_shanghai | ~300M                    |


**DINOv3**:

| MODEL           | MODEL_ARCH               | FINETUNE                         | SIZE                     |
|-----------------|--------------------------|----------------------------------|--------------------------|
| Dinov3          | dinov3_vits16            | dinov3_vits16_pretrain.pth       | ~21M                     |
| Dinov3          | dinov3_vits16plus        | dinov3_vits16plus_pretrain.pth   | ~29M                     |
| Dinov3          | dinov3_vitb16            | dinov3_vitb16_pretrain.pth       | ~86M                     |
| Dinov3          | dinov3_vitl16            | dinov3_vitl16_pretrain.pth       | ~300M                    |
| Dinov3          | dinov3_vith16plus        | dinov3_vith16plus_pretrain.pth   | ~840M                    |
| Dinov3          | dinov3_vit7b16           | dinov3_vit7b16_pretrain.pth      | ~6.7B                    |


**DINOv2**:

| MODEL           | MODEL_ARCH               | FINETUNE                     | SIZE                     |
|-----------------|--------------------------|------------------------------|--------------------------|
| Dinov2          | dinov2_vits14            | dinov2_vits14_pretrain.pth   | ~21M                     |
| Dinov2          | dinov2_vitb14            | dinov2_vitb14_pretrain.pth   | ~86M                     |
| Dinov2          | dinov2_vitl14            | dinov2_vitl14_pretrain.pth   | ~300M                    |
| Dinov2          | dinov2_vitg14            | dinov2_vitg14_pretrain.pth   | ~1.1B                    |


Change the DATA_PATH to your dataset directory.

```
# ==== Model settings ====
# adaptation {finetune,lp}
ADAPTATION="finetune"
MODEL="RETFound_dinov2"
MODEL_ARCH="retfound_dinov2"
FINETUNE="RETFound_dinov2_meh"

# ==== Data settings ====
# change the dataset name and corresponding class number
DATASET="MESSIDOR2"
NUM_CLASS=5

# =======================
DATA_PATH="PATH TO THE DATASET"
TASK="${MODEL_ARCH}_${DATASET}_${ADAPTATION}"

torchrun --nproc_per_node=1 --master_port=48766 main_finetune.py \
  --model "${MODEL}" \
  --model_arch "${MODEL_ARCH}" \
  --finetune "${FINETUNE}" \
  --savemodel \
  --global_pool \
  --batch_size 24 \
  --world_size 1 \
  --epochs 50 \
  --nb_classes "${NUM_CLASS}" \
  --data_path "${DATA_PATH}" \
  --input_size 224 \
  --task "${TASK}" \
  --adaptation "${ADAPTATION}" 

```



6. For evaluation only (download data and model checkpoints [here](BENCHMARK.md); change the DATA_PATH below)


```
# ==== Model/settings (match training) ====
ADAPTATION="finetune"
MODEL="RETFound_dinov2"
MODEL_ARCH="retfound_dinov2"
FINETUNE="RETFound_dinov2_meh"

# ==== Data/settings (match training) ====
DATASET="MESSIDOR2"
NUM_CLASS=5

# =======================
DATA_PATH="PATH TO THE DATASET"
TASK="${MODEL_ARCH}_${DATASET}_${ADAPTATION}"

# Path to the trained checkpoint (adjust if you saved elsewhere)
CKPT="./output_dir/${TASK}/checkpoint-best.pth"

# ==== Evaluation only ====
torchrun --nproc_per_node=1 --master_port=48766 main_finetune.py \
  --model "${MODEL}" \
  --model_arch "${MODEL_ARCH}" \
  --savemodel \
  --global_pool \
  --batch_size 128 \
  --world_size 1 \
  --nb_classes "${NUM_CLASS}" \
  --data_path "${DATA_PATH}" \
  --input_size 224 \
  --task "${TASK}" \
  --adaptation "${ADAPTATION}" \
  --eval \
  --resume "${CKPT}"

```


### 📃Citation

If you find this repository useful, please consider citing this paper:


```
@article{zhou2023foundation,
  title={A foundation model for generalizable disease detection from retinal images},
  author={Zhou, Yukun and Chia, Mark A and Wagner, Siegfried K and Ayhan, Murat S and Williamson, Dominic J and Struyven, Robbert R and Liu, Timing and Xu, Moucheng and Lozano, Mateo G and Woodward-Court, Peter and others},
  journal={Nature},
  volume={622},
  number={7981},
  pages={156--163},
  year={2023},
  publisher={Nature Publishing Group UK London}
}
```

```
@misc{zhou2025generalistversusspecialistvision,
      title={Generalist versus Specialist Vision Foundation Models for Ocular Disease and Oculomics}, 
      author={Yukun Zhou and Paul Nderitu and Jocelyn Hui Lin Goh and Justin Engelmann and Siegfried K. Wagner and Anran Ran and Hongyang Jiang and Lie Ju and Ke Zou and Sahana Srinivasan and Hyunmin Kim and Takahiro Ninomiya and Zheyuan Wang and Gabriel Dawei Yang and Eden Ruffell and Dominic Williamson and Rui Santos and Gabor Mark Somfai and Carol Y. Cheung and Tien Yin Wong and Daniel C. Alexander and Yih Chung Tham and Pearse A. Keane},
      year={2025},
      eprint={2509.03421},
      archivePrefix={arXiv},
      primaryClass={eess.IV},
      url={https://arxiv.org/abs/2509.03421}, 
}
```
