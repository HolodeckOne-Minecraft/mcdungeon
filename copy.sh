#!/bin/bash

rm -r -f $1/mcdungeon
mkdir -p $1/mcdungeon
cp -Ra . $1/mcdungeon
rm -r -f $1/mcdungeon/build.sh
rm -r -f $1/mcdungeon/copy.sh
rm -r -f $1/mcdungeon/.git
rm -r -f $1/mcdungeon/pymclevel/.git
