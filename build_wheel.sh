PYV=$1

if [[ ! $PYV ]]; then  # XD
	PYV=3
fi

echo Python version: $PYV

LIBDIR=$PWD

PLATFORM=linux_x86_64
BINARY=$LIBDIR/anime4kcpp/build/bin/libac.so

CMAKE_ARGS="-DBuild_CLI=OFF -DBuild_C_wrapper=ON -DBuild_C_wrapper_with_core=ON"

if [ "$2" == "cuda" ]; then
	CMAKE_ARGS="${CMAKE_ARGS} -DEnable_CUDA=ON"
	echo building with cuda..
fi

echo "Removing temps.."

if [ ! -e $BINARY ]; then
	rm -rf $LIBDIR/anime4kcpp/build/*
fi
rm -rf $LIBDIR/dist/*.whl
rm -rf $LIBDIR/dist/*.tar.gz

if [ ! -e $BINARY ]; then
	git clone https://github.com/TianZerL/Anime4KCPP.git anime4kcpp

	mkdir -v anime4kcpp/build
	cd anime4kcpp/build
	cmake  ..  # Standard
	# cmake -DBuild_CLI=OFF -DBuild_C_wrapper=ON -DBuild_C_wrapper_with_core=ON -DEnable_CUDA=on ..  # CUDA (NVidia)
	make -j$(nproc)
fi

cd $LIBDIR

# ls $LIBDIR/anime4kcpp/build/bin/
# ls $LIBDIR/pya4k/wrapper

cp $BINARY $LIBDIR/pya4k/wrapper

echo "Building wheel (build).."
python$PYV -m build --w -C="--build-option=--plat-name ${PLATFORM}"

# pip$PYV install -U --force-reinstall $LIBDIR/dist/*.whl

echo "Done!"