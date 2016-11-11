#!/bin/bash

# copy all for publishing at web page

echo pack source code and copy them to local web site
echo running ...

VERSION="0.3.10"

# build html
echo copy documentation
make html -C doc
cp -r doc/_build/html/* ~/dokumenty/web/spilkaj2015ciirc/software/CTGViewer/

echo Pack and copy source files and documentation
FILE="CTGViewer-$VERSION.zip"
DIR="CTGViewer-$VERSION"
echo $FILE

# remove existing
rm $FILE

# new dir
mkdir $DIR

echo Copy documentation
echo "$DIR/doc"
mkdir "$DIR/doc"
cp -r doc/_build/html/* "$DIR/doc"

echo Copy source file
cp *.py $DIR
cp *.ui $DIR
cp *.qrc $DIR
#cp default.ini $DIR
cp README.md $DIR
cp LICENSE $DIR
cp -r unittest_files $DIR

echo Packing ....
zip -rq $FILE $DIR
#zip -r $FILE *.py *.ui *.qrc default.ini README unittest_files/*
cp $FILE ~/dokumenty/web/spilkaj2015ciirc/software/

# copy exe files
FILE_EXE="CTGViewer_v${VERSION}_setup.exe"
cp build/$FILE_EXE ~/dokumenty/web/spilkaj2015ciirc/software/$FILE_EXE

rm -r $DIR

echo DONE

