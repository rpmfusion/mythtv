git clone git://github.com/MythTV/mythtv.git
branch=fixes/29
pushd mythtv
git checkout $branch
git diff -p --stat v29.0 > ../mythtv-fixes.patch
git log v29.0..HEAD > ../ChangeLog
newdescrib=$(git describe)
date=$(git log -1 --format=%cd --date=short | tr -d \-)
relversion=$(echo $newdescrib | sed "s/^[^-]*//; s/-/./g; s/^/.$date/")
popd
sed -i "s|^%define vers_string .*|%define vers_string $newdescrib|" mythtv.spec
sed -i "s|^%define rel_string .*|%define rel_string $relversion|" mythtv.spec
rpmdev-bumpspec -c "Update to $newdescrib from branch $branch" mythtv.spec
