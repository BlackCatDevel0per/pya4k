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
	
	# We can do this stuff by passing "cmake -DSomeOption=SomeVal .." but the cmake options sometimes don't work with these args..
	if [ "$2" == "cuda" ]; then
		values=("Build_CLI=OFF" "Build_C_Wrapper=ON" "Build_Static_Core=OFF" "Enable_CUDA=ON")
		echo building with cuda..
	else
		values=("Build_CLI=OFF" "Build_C_Wrapper=ON" "Build_Static_Core=OFF" "Enable_CUDA=OFF")
	fi

	for value in "${values[@]}"; do
		# Split the value into the name and the new value
		key=$(echo "$value" | cut -d "=" -f 1)
		value=$(echo "$value" | cut -d "=" -f 2)

		# Replace the old value with the new value using regular expression
		sed -i -r "s/(option\($key\s*\".*\"\s*)(ON|OFF)\)/\1$value)/g" ../CMakeLists.txt

	done

	cmake ..
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