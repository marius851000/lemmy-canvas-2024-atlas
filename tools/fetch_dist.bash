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

# That’s what the npm repo recommend
echo "fetching bootstrap-dark"
wget "https://cdn.jsdelivr.net/npm/bootstrap-dark-5@1.1.3/dist/css/bootstrap-dark.min.css" -O $DIST_DIR/bootstrap-dark.min.css

# That’s also what the npm repo recommend, but we pin a version
echo "fetching pwa-update"
wget https://cdn.jsdelivr.net/npm/@pwabuilder/pwaupdate@0.2.1/dist/pwa-update.js -O $DIST_DIR/pwa-update.js

# This one doesn’t specify this as upstream, but that’s was present before when it didn’t fetched a copy of the deps, so I’m just gonna trust it
# ok. This one does fetch data from a google server in the script. Might need more digging, but I’ll keep this as-is for now.
echo "fetching workbox-sw"
wget https://cdn.jsdelivr.net/npm/workbox-sw@6.5.4/build/workbox-sw.js -O $DIST_DIR/workbox-sw.js