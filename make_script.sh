#!/bin/bash

if [ $# -ne 2 ]; then
    echo Usage: $0 filename scriptname
    exit
fi

modname=`dirname $1 | tr '/' '.'`.`basename $1 .py`

echo Script $2 will launch module $modname

cat <<EOF > scripts/$2
#!/bin/bash
python -m $modname
EOF

chmod u+x scripts/$2
