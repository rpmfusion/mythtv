RAWHIDE=34
REPOS="f33 f32"

if ! [ -d "mythtv" ]; then
    git clone git://github.com/MythTV/mythtv.git
fi
version=31.0
branch=fixes/31
pushd mythtv
git checkout $branch
git pull
git log v$version..HEAD > ../mythtv-ChangeLog
newdescrib=$(git describe)
date=$(git log -1 --format=%cd --date=short | tr -d \-)
relversion=$(echo $newdescrib | sed "s/^[^-]*//; s/-/./g; s/\.g/.${date}git/")
githash=$(git rev-parse HEAD)
shorthash=$(echo $githash | cut -b -10)
popd
# Clean previous modifications on mythtv.spec
#echo Press enter to run: Clean previous modifications on mythtv.spec; read dummy;
#git checkout mythtv.spec
sed -i "s|global vers_string .*|global vers_string $newdescrib|" mythtv.spec
sed -i "s|global rel_string .*|global rel_string $relversion|" mythtv.spec
sed -i "s|global githash .*|global githash $githash|" mythtv.spec
rpmdev-bumpspec -c "Update to $version$relversion from branch $branch " mythtv.spec
spectool -g mythtv.spec
rfpkg scratch-build --srpm

echo Press enter to run: rfpkg new-sources mythtv-${version}.tar.gz v${version}..${shorthash}.patch; read dummy;
rfpkg new-sources mythtv-${version}.tar.gz v${version}..${shorthash}.patch
echo Press enter to continue; read dummy;
rfpkg ci -c && git show
echo Press enter to build current branch.; read dummy;
rfpkg push && rfpkg build --nowait
for repo in $REPOS ; do
echo Press enter to build on branch $repo; read dummy;
git checkout $repo && git merge master && git push && rfpkg build --nowait; git checkout master
done

