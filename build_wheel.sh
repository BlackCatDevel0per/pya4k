PYV=$1

if [[ ! $PYV ]]; then  # XD
	PYV=3
fi

echo Selected python version: $PYV

LIBDIR=$PWD

PLATFORM=linux_x86_64
BINARY=$LIBDIR/anime4kcpp/build/bin/libac.so


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
	if [ "$2" == "cuda" ]; then
		cmake -DBuild_CLI:BOOL=OFF -DBuild_C_Wrapper:BOOL=ON -DBuild_Static_Core:BOOL=OFF -DEnable_CUDA:BOOL=ON ..
		echo building with cuda..
	else
		cmake -DBuild_CLI:BOOL=OFF -DBuild_C_Wrapper:BOOL=ON -DBuild_Static_Core:BOOL=OFF ..
	fi
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