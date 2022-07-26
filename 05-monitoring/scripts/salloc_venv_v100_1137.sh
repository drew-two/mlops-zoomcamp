#!/bin/bash

module load python/3.8 cuda cudnn
module load scipy-stack

source ~/vit-test/bin/activate

echo -e '#!/bin/bash\nunset XDG_RUNTIME_DIR\njupyter notebook --ip $(hostname -f) --no-browser' > \
	$VIRTUAL_ENV/bin/notebook.sh
chmod u+x $VIRTUAL_ENV/bin/notebook.sh

salloc --time=0-$1:00 \
	--gres=gpu:v100:1 \
	--nodelist=gra1337 \
	--cpus-per-task=3 \
	--mem=32G \
	--account=def-bauer \
	--mail-user=akatoch2@uwo.ca \
	--mail-type=ALL \
	srun $VIRTUAL_ENV/bin/notebook.sh
