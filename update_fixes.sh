if ! [ -d "mythtv" ]; then
    git clone git://github.com/MythTV/mythtv.git
fi
version=29.1
branch=fixes/29
pushd mythtv
git checkout $branch
git pull
#git log v$version..HEAD > ../ChangeLog
newdescrib=$(git describe)
date=$(git log -1 --format=%cd --date=short | tr -d \-)
relversion=$(echo $newdescrib | sed "s/^[^-]*//; s/-/./g; s/\.g/.${date}git/")
githash=$(git rev-parse HEAD)
shorthash=$(echo $githash | cut -b -10)
popd
# Clean previous modifications on mythtv.spec
echo Press enter to run: Clean previous modifications on mythtv.spec; read dummy;
git checkout mythtv.spec
sed -i "s|^%define vers_string .*|%define vers_string $newdescrib|" mythtv.spec
sed -i "s|^%define rel_string .*|%define rel_string $relversion|" mythtv.spec
sed -i "s|^%define githash .*|%define githash $githash|" mythtv.spec
rpmdev-bumpspec -c "Update to $version$relversion from branch $branch " mythtv.spec
spectool -g mythtv.spec
echo Press enter to run: rfpkg new-sources mythtv-${version}.tar.gz v${version}..${shorthash}.patch; read dummy;
rfpkg new-sources mythtv-${version}.tar.gz v${version}..${shorthash}.patch
echo Press enter to continue; read dummy;
rfpkg ci -c && git show
echo Press enter to build current branch.; read dummy;
rfpkg push && rfpkg build --nowait
echo Press enter to build f29; read dummy;
git checkout f28 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to build f28; read dummy;
git checkout f28 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to build f27; read dummy;
git checkout f27 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to build elf; read dummy;
git checkout el7 && git merge master && git push && rfpkg build --nowait; git checkout master
