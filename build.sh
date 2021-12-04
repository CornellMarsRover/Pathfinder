BASEDIR=$(dirname "$0")
cd $BASEDIR/robot
rm -rf devel/ build/
catkin_make
source devel/setup.bash