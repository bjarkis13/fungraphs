#!/usr/bin/env bash

python3 manage.py makemigrations population
python3 manage.py migrate
# Get d3 and nvd3 libs
if [ -d lib/nvd3 ] ; then
    cd lib
    wget https://github.com/novus/nvd3/zipball/master -O nvd3.zip
    mkdir nvd3
    unzip nvd3 -d nvd3
    subdir=$(ls nvd3)
    mv nvd3/$subdir/* nvd3
    rmdir nvd3/$subdir
    rm nvd3.zip
fi
if [ -d lib/d3 ] ; then
    wget https://github.com/mbostock/d3/releases/download/v3.5.10/d3.zip -O d3.zip
    mkdir d3
    unzip d3.zip -d d3
    rm d3.zip
fi

#Insert data into database
python manage.py shell -c "import insert,convert;insert.addChanges();insert.addPopulation();convert.updateAll()"
