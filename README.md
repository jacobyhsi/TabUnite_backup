# TabUnite: An Efficient Encoding Framework for Tabular Data Generation
Official Implementation of the Paper TabUnite: An Efficient Encoding Framework for Tabular Data Generation.

## Usage

Clone this repository and navigate to it in your terminal.

Create environment. This environment can be used for everything apart from eval_quality:

```
conda create -n tabunite python=3.10
conda activate tabunite
```

Install pytorch via conda:

```
conda install pytorch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 pytorch-cuda=11.7 -c pytorch -c nvidia
```

For eval_quality, create the following environment:
```
conda create -n tabunite_quality python=3.10
conda activate tabunite_quality

pip install synthcity
pip install category_encoders
```

Any missing dependencies can be installed using pip. Once all the dependencies are installed, the scripts should run accordingly as follows.

## Preparing Datasets
