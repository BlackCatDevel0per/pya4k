PYV=3.8

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
	git clone -b v2.5.0 https://github.com/TianZerL/Anime4KCPP.git anime4kcpp

	mkdir -v anime4kcpp/build
	cd anime4kcpp/build
	cmake -DBuild_CLI=OFF -DBuild_C_wrapper=ON -DBuild_C_wrapper_with_core=ON ..  # Standard
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