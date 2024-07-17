# should be run in the root of the repository
# The files present in the dist folder should correspond to those obtained by this script (as a way to source those blobs)

set -e

DIST_DIR=$(pwd)/web/_js/dist


BOOTSTRAP_TEMP=$(mktemp -d)
echo fetching bootstrap with temp dir $BOOTSTRAP_TEMP
cd $BOOTSTRAP_TEMP
wget https://github.com/twbs/bootstrap/releases/download/v5.3.3/bootstrap-5.3.3-dist.zip -O dist.zip
unzip dist.zip
cp bootstrap-*-dist/js/bootstrap.bundle.min.* $DIST_DIR
rm -r $BOOTSTRAP_TEMP

BOOTSTRAP_ICONS_TEMP=$(mktemp -d)
echo fetching bootstrap-icons with temp dir $BOOTSTRAP_ICONS_TEMP
cd $BOOTSTRAP_ICONS_TEMP
wget https://github.com/twbs/icons/releases/download/v1.11.3/bootstrap-icons-1.11.3.zip -O dist.zip
unzip dist.zip
mkdir -p $DIST_DIR/bootstrap-icons-font/fonts
cp -r bootstrap-icons-*/font/fonts/* $DIST_DIR/bootstrap-icons-font/fonts
cp -r bootstrap-icons-*/font/bootstrap-icons.min.css $DIST_DIR/bootstrap-icons-font/bootstrap-icons.min.css
rm -r $BOOTSTRAP_ICONS_TEMP