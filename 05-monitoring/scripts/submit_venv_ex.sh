#!/bin/bash
#SBATCH --account=def-bauer
#SBATCH --cpus-per-task=2
#SBATCH --mem=2G
#SBATCH --time=0-00:10      	# time (DD-HH:MM)

## Loading env
module load python/3.8 cuda cudnn
module load scipy-stack
virtualenv --no-download $SLURM_TMPDIR/vit-test
source $SLURM_TMPDIR/vit-test/bin/activate
pip install --no-index --upgrade pip

## Sending data
mkdir $SLURM_TMPDIR/data
tar xf ~/5CLASS.tar.gz -C $SLURM_TMPDIR/data

mkdir $SLURM_TMPDIR/code
tar xf ~/code.tar.gz -C $SLURM_TMPDIR/code

## Loading dependencies
pip install --no-index -r ./$SLURM_TMPDIR/code/requirements.txt
pip install --no-binary vit-keras
pip install jupyter

## Start jupyter
echo -e '#!/bin/bash\nunset XDG_RUNTIME_DIR\njupyter notebook --ip $(hostname -f) --no-browser' > $SLURM_TMPDIR/$VIRTUAL_ENV/bin/notebook.sh
chmod u+x $SLURM_TMPDIR/$VIRTUAL_ENV/bin/notebook.sh

srun $SLURM_TMPDIR/$VIRTUAL_ENV/bin/notebook.sh
