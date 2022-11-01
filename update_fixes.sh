RAWHIDE=37
REPOS="f36 f35 f34 el8 el7"

if ! [ -d "mythtv" ]; then
    git clone https://github.com/MythTV/mythtv.git
fi
version=32.0
branch=fixes/32
pushd mythtv
git checkout $branch
git pull
git log v$version..HEAD > ../mythtv-ChangeLog
newdescrib=$(git describe)
date=$(git log -1 --format=%cd --date=format:"%Y%m%d")
relversion=$(echo $newdescrib | sed "s/^[^-]*//; s/-/./g; s/\.g/.${date}git/")
githash=$(git rev-parse HEAD)
shorthash=$(echo $githash | cut -b -10)
popd
echo $date
# Clean previous modifications on mythtv.spec
#echo Press enter to run: Clean previous modifications on mythtv.spec; read dummy;
#git checkout mythtv.spec
sed -i "s|global vers_string .*|global vers_string $newdescrib|" mythtv.spec
sed -i "s|global git_date .*|global git_date $date|" mythtv.spec
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

