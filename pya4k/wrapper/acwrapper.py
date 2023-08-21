import ctypes
import os
import platform

ac_lib = {
	"Windows": "ac.dll",
	"Linux": "libac.so",
	"Darwin": "libac.dylib",
}

curr_path = os.path.dirname(os.path.realpath(__file__))

if platform.system() == "Linux":
	c_ac = ctypes.cdll.LoadLibrary(os.path.join(curr_path, ac_lib[platform.system()]))
else:
	os.environ["PATH"] += ";" + curr_path
	c_ac = ctypes.windll.LoadLibrary(os.path.join(curr_path, ac_lib[platform.system()]))
# TODO: Add raise error..


class ac_parameters(ctypes.Structure):
	"""
	typedef struct ac_parameters
	{
		int passes;
		int pushColorCount;
		double strengthColor;
		double strengthGradient;
		double zoomFactor;
		ac_bool fastMode;
		ac_bool videoMode;
		ac_bool preprocessing;
		ac_bool postprocessing;
		unsigned char preFilters;
		unsigned char postFilters;
		unsigned int maxThreads;
		ac_bool HDN;
		int HDNLevel;
		ac_bool alpha;
	} ac_parameters;
	"""

	_fields_ = [
		("passes", ctypes.c_int),
		("pushColorCount", ctypes.c_int),
		("strengthColor", ctypes.c_double),
		("strengthGradient", ctypes.c_double),
		("zoomFactor", ctypes.c_double),
		("fastMode", ctypes.c_int),
		("videoMode", ctypes.c_int),
		("preprocessing", ctypes.c_int),
		("postprocessing", ctypes.c_int),
		("preFilters", ctypes.c_uint8),
		("postFilters", ctypes.c_uint8),
		("maxThreads", ctypes.c_uint),
		("HDN", ctypes.c_int),
		("HDNLevel", ctypes.c_int),
		("alpha", ctypes.c_int),
	]


class ac_version(ctypes.Structure):
	"""
	typedef struct ac_version
	{
		char coreVersion[6];
		char wrapperVersion[6];
	} ac_version;
	"""

	_fields_ = [
		("coreVersion", ctypes.c_char * 6),
		("wrapperVersion", ctypes.c_char * 6),
	]


class ac_OpenCLAnime4K09Data(ctypes.Structure):
	"""
	typedef struct ac_OpenCLAnime4K09Data
	{
		unsigned int pID;
		unsigned int dID;
		int OpenCLQueueNum;
		ac_bool OpenCLParallelIO;
	} ac_OpenCLAnime4K09Data;
	"""

	_fields_ = [
		("pID", ctypes.c_uint),
		("dID", ctypes.c_uint),
		("OpenCLQueueNum", ctypes.c_int),
		("OpenCLParallelIO", ctypes.c_int),
	]


class ac_OpenCLACNetData(ctypes.Structure):
	"""
	typedef struct ac_OpenCLACNetData
	{
		unsigned int pID;
		unsigned int dID;
		int OpenCLQueueNum;
		ac_bool OpenCLParallelIO;
		ac_CNNType CNNType;
	} ac_OpenCLACNetData;
	"""

	_fields_ = [
		("pID", ctypes.c_uint),
		("dID", ctypes.c_uint),
		("OpenCLQueueNum", ctypes.c_int),
		("OpenCLParallelIO", ctypes.c_int),
		("CNNType", ctypes.c_int),
	]


class ac_CUDAData(ctypes.Structure):
	"""
	typedef struct ac_CUDAData
	{
		unsigned int dID;
	} ac_CUDAData;
	"""

	_fields_ = [
		("dID", ctypes.c_uint),
	]


class ac_managerData(ctypes.Structure):
	"""
	typedef struct ac_managerData
	{
		ac_OpenCLAnime4K09Data* OpenCLAnime4K09Data;
		ac_OpenCLACNetData* OpenCLACNetData;
		ac_CUDAData* CUDAData;
	} ac_managerData;
	"""

	_fields_ = [
		("OpenCLAnime4K09Data", ctypes.POINTER(ac_OpenCLAnime4K09Data)),
		("OpenCLACNetData", ctypes.POINTER(ac_OpenCLACNetData)),
		("CUDAData", ctypes.POINTER(ac_CUDAData)),
	]


# ac_processType
AC_CPU_Anime4K09 = 0
AC_CPU_ACNet = 1
AC_OpenCL_Anime4K09 = 2
AC_OpenCL_ACNet = 3
AC_Cuda_Anime4K09 = 4
AC_Cuda_ACNet = 5


class ac_manager:
	AC_Manager_OpenCL_Anime4K09 = 1
	AC_Manager_OpenCL_ACNet = 1 << 1
	AC_Manager_Cuda = 1 << 2


# ac_bool
(AC_FALSE, AC_TRUE) = (0, 1)

# ac_error
AC_OK = 0
AC_ERROR_NULL_INSTANCE = 1
AC_ERROR_NULL_PARAMETERS = 2
AC_ERROR_NULL_Data = 3
AC_ERROR_INIT_GPU = 4
AC_ERROR_PORCESSOR_TYPE = 5
AC_ERROR_LOAD_IMAGE = 6
AC_ERROR_LOAD_VIDEO = 7
AC_ERROR_INIT_VIDEO_WRITER = 8
AC_ERROR_GPU_PROCESS = 9
AC_ERROR_SAVE_TO_NULL_POINTER = 10
AC_ERROR_NOT_YUV444 = 11
AC_ERROR_YUV444_AND_RGB32_AT_SAME_TIME = 12
AC_ERROR_CUDA_NOT_SUPPORTED = 13
AC_ERROR_VIDEO_MODE_UNINIT = 14

# ac_codec
AC_OTHER = -1
AC_MP4V = 0
AC_DXVA = 1
AC_AVC1 = 2
AC_VP09 = 3
AC_HEVC = 4
AC_AV01 = 5

ac_instance = ctypes.c_void_p

c_ac.acGetVersion.restype = ac_version

c_ac.acGetInstance2.restype = ac_instance

c_ac.acGetResultDataLength.restype = ctypes.c_size_t

c_ac.acBenchmark2.restype = ctypes.c_double

