#!/bin/bash

module load python/3.8 cuda cudnn
module load scipy-stack

source ~/vit-test/bin/activate

echo -e '#!/bin/bash\nunset XDG_RUNTIME_DIR\njupyter notebook --ip $(hostname -f) --no-browser' > \
	$VIRTUAL_ENV/bin/notebook.sh
chmod u+x $VIRTUAL_ENV/bin/notebook.sh

salloc --time=0-$1:00 \
	--gres=gpu:t4:2 \
	--cpus-per-task=6 \
	--mem=32G \
	--account=def-bauer \
	--mail-type=BEGIN \
	srun $VIRTUAL_ENV/bin/notebook.sh
