PYV=$1

if [[ ! $PYV ]]; then  # XD
	PYV=3
fi

echo Selected python version: $PYV

LIBDIR=$PWD

PLATFORM=linux_x86_64
BINARY_PATH=$LIBDIR/anime4kcpp/build/bin
BIN_LIBAC=$BINARY_PATH/libac.so


echo "Removing temps.."

# Use clang as default compiler if exists
if [[ -e "/usr/bin/ccache" && -e "/usr/bin/clang" ]]; then
	echo Using llvm with ccache
	export LD="ccache lld"
	export CC="ccache clang"
	export CXX="ccache clang++"
	export AR="ccache llvm-ar"  
	export AS="ccache llvm-as"
	export RANLIB=llvm-ranlib
elif [ -e "/usr/bin/clang" ]; then
	echo Using llvm
	export RANLIB=llvm-ranlib
	export LD="lld"
	export CC="clang"
	export CXX="clang++"
	export AR="llvm-ar"  
	export AS="llvm-as"
	export RANLIB=llvm-ranlib
fi


if [ ! -e $BIN_LIBAC ]; then
	rm -rf $LIBDIR/anime4kcpp/build/*
fi
rm -rf $LIBDIR/dist/*.whl
rm -rf $LIBDIR/dist/*.tar.gz

values_default=("Build_CLI=OFF" "Build_C_Wrapper=ON" "Build_Static_Core=OFF")

values_o2=(
	# Advanced libs [Need install!]
	# "Build_VapourSynth_Plugin=ON"  # Better and modern then avisynthplus (Don't forget to install one of TBB, OpenMP, PPL or other parallel lib..)
	# "Build_AviSynthPlus_Plugin=ON"  # (it's old..)
	"Use_Eigen3=ON"

	# "Enable_OpenCV_DNN=ON"  # Well for much RAM. Need external models, see anime4kcpp/core/models/ (copy near script path)
	# "Enable_NCNN=ON"  # Well for much RAM..?

	# Proc instructions
	"Enable_AVX=ON"
	"Enable_AVX2=ON"
	"Enable_SSE42=ON"

	# Proc optimizations
	# "Ryzen_Optimization=ON"  # Uncomment if you have AMD CPU
	"Enable_Fast_Math=ON"
	"Native_Optimization=ON"
	# Core lib optimizations
	"Other_Optimization_For_Core=ON" "Other_Optimization_For_Other=ON"

	# "Enable_OpenCL=OFF"  # will use CUDA Only..? (If have..)
)
values_o2+=(${values_default[@]})
values+=(${values_o2[@]})


##
if [ ! -e $BIN_LIBAC ]; then
	git clone https://github.com/TianZerL/Anime4KCPP.git anime4kcpp

	cd $LIBDIR/anime4kcpp
	# WARN! (TODO: Add dir check..)
	git checkout .
	mkdir -v build
	cd build
	
	# We can do this stuff by passing "cmake -DSomeOption=SomeVal .." but the cmake options sometimes don't work with these args..
	if [ "$2" == "CUDA" ]; then
		# Advanced options for common use (on google colab for example..)
		values+=("Enable_CUDA=ON")
		echo building with cuda..
	# build with some plugins & optimizations..
	elif [ "$2" == "O2" ]; then
		values+=("Enable_CUDA=OFF")
		echo building with some optimizations..
	
	# build with some plugins & optimizations, but no parallel tasks.. (Use it If you don't have much RAM or VRAM..)
	elif [ "$2" == "O2_NOP" ]; then
		values+=("Enable_CUDA=OFF")
		values+=("Disable_Parallel=ON")
		echo building with some optimizations and NO Parallel..
	else
		values=(${values_default[@]})
	fi

	for value in "${values[@]}"; do
		# Split the value into the name and the new value
		key=$(echo "$value" | cut -d "=" -f 1)
		value=$(echo "$value" | cut -d "=" -f 2)

		# Replace the old value with the new value using regular expression
		sed -i -r "s/(option\($key\s*\".*\"\s*)(ON|OFF)\)/\1$value)/g" ../CMakeLists.txt

	done

	# TODO: Check if build success.. If not, just stop script..
	cmake ..
	make -j$(nproc)
fi

cd $LIBDIR

# ls $LIBDIR/anime4kcpp/build/bin/
# ls $LIBDIR/pya4k/wrapper

# FIXME: Link new Core lib to new path..
cp $BINARY_PATH/*.so $LIBDIR/pya4k/wrapper
# mv $BINARY_PATH/*.so $LIBDIR/pya4k/wrapper

echo "Building wheel (build).."
python$PYV -m build --w -C="--build-option=--plat-name ${PLATFORM}"

# pip$PYV install -U --force-reinstall $LIBDIR/dist/*.whl

echo "Done!"
