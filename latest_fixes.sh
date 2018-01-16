git clone git://github.com/MythTV/mythtv.git
version=29.0
branch=fixes/29
pushd mythtv
git checkout $branch
git log v29.0..HEAD > ../ChangeLog
newdescrib=$(git describe)
date=$(git log -1 --format=%cd --date=short | tr -d \-)
relversion=$(echo $newdescrib | sed "s/^[^-]*//; s/-/./g; s/^/.$date/")
githash=$(git rev-parse HEAD)
popd
sed -i "s|^%define vers_string .*|%define vers_string $newdescrib|" mythtv.spec
sed -i "s|^%define rel_string .*|%define rel_string $relversion|" mythtv.spec
sed -i "s|^%define githash .*|%define githash $githash|" mythtv.spec
#rpmdev-bumpspec -c "Update to $newdescrib from branch $branch" mythtv.spec
