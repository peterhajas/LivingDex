#!/bin/sh
# Setup script for LivingDex to prepare dependencies and set up the 'static'
# directory for Flask

# Updata our submodules. PokeSprite is a submodule of LivingDex, so it will be
# downloaded & updated

git submodule init
git submodule update

# Activate virtualenv

virtualenv venv

# Generate the PokeSprite spritesheet, CSS and JavaScript

cd pokesprite
./pokesprite.php
cd ..

# Copy the PokeSprite spritesheet, CSS and JavaScript so that Flask's 'url_for'
# can find them in resource lookups

cp pokesprite/output/pokesprite.png static/
cp pokesprite/output/pokesprite.css static/
cp pokesprite/output/pokesprite.js static/
cp pokesprite/output/pokesprite.min.js static/
