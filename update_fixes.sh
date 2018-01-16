git clone git://github.com/MythTV/mythtv.git
version=29.0
branch=fixes/29
pushd mythtv
git checkout $branch
git pull
git log v$version..HEAD > ../ChangeLog
newdescrib=$(git describe)
date=$(git log -1 --format=%cd --date=short | tr -d \-)
relversion=$(echo $newdescrib | sed "s/^[^-]*//; s/-/./g; s/^/.$date/")
githash=$(git rev-parse HEAD)
shorthash=$(echo $githash | cut -b -10)
popd
sed -i "s|^%define vers_string .*|%define vers_string $newdescrib|" mythtv.spec
sed -i "s|^%define rel_string .*|%define rel_string $relversion|" mythtv.spec
sed -i "s|^%define githash .*|%define githash $githash|" mythtv.spec
git checkout mythtv.spec
rpmdev-bumpspec -c "Update to $newdescrib from branch $branch" mythtv.spec
spectool -g mythtv.spec
echo Press enter to run: rfpkg new-sources mythtv-${version}-${shorthash}.tar.gz; read dummy;
rfpkg new-sources mythtv-${version}-${shorthash}.tar.gz
echo Press enter to continue; read dummy;
rfpkg clog && rfpkg commit -F clog && /bin/rm clog && git show
echo Press enter to continue; read dummy;
rfpkg push && rfpkg build --nowait
echo Press enter to continue; read dummy;
git checkout f27 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to continue; read dummy;
git checkout f26 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to continue; read dummy;
git checkout el7 && git merge master && git push && rfpkg build --nowait; git checkout master
