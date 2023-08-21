if [ ! -z "$1" ]; then
    export INSTALLATION_PATH=$1
else
    export INSTALLATION_PATH="$HOME/pya4k_wheel/"
fi

TEMP="/tmp/pya4k"

git clone https://github.com/BlackCatDevel0per/pya4k.git $TEMP/pya4k

apt-get update
apt install -y --no-install-recommends libopencv-dev ocl-icd-opencl-dev cmake python3-pip

git clone https://github.com/TianZerL/Anime4KCPP.git $TEMP/anime4kcpp

mkdir -v $TEMP/anime4kcpp/build
cd $TEMP/anime4kcpp/build
cmake -DBuild_CLI=OFF -DBuild_C_wrapper=ON -DBuild_C_wrapper_with_core=ON ..
make -j$(nproc)

mv -v $TEMP/anime4kcpp/build/bin/libac.so $TEMP/pya4k/pya4k/wrapper

cd $TEMP/pya4k

pip3 install -r requirements.txt
pip3 install setuptools
pip3 install wheel

python build

mv -v $TEMP/pya4k/dist $INSTALLATION_PATH

rm -rf $TEMP

echo "All finished."
echo "Your wheel file of pya4k was stored in $INSTALLATION_PATH"
echo "Use pip install $INSTALLATION_PATH$(ls $INSTALLATION_PATH) to install it"
