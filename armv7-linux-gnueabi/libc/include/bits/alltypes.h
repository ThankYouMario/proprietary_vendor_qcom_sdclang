#define _Addr int
#define _Int64 long long
#define _Reg int

#if defined(__NEED_va_list) && !defined(__DEFINED_va_list) && !defined(__CLANG_VA_LIST_DEFINED)
typedef __builtin_va_list va_list;
#define __DEFINED_va_list
#define __CLANG_VA_LIST_DEFINED
#endif

#if defined(__NEED___isoc_va_list) && !defined(__DEFINED___isoc_va_list) && !defined(__CLANG___ISOC_VA_LIST_DEFINED)
typedef __builtin_va_list __isoc_va_list;
#define __DEFINED___isoc_va_list
#define __CLANG___ISOC_VA_LIST_DEFINED
#endif


#ifndef __cplusplus
#if defined(__NEED_wchar_t) && !defined(__DEFINED_wchar_t) && !defined(__CLANG_WCHAR_T_DEFINED)
typedef unsigned wchar_t;
#define __DEFINED_wchar_t
#define __CLANG_WCHAR_T_DEFINED
#endif

#endif

#if defined(__NEED_float_t) && !defined(__DEFINED_float_t) && !defined(__CLANG_FLOAT_T_DEFINED)
typedef float float_t;
#define __DEFINED_float_t
#define __CLANG_FLOAT_T_DEFINED
#endif

#if defined(__NEED_double_t) && !defined(__DEFINED_double_t) && !defined(__CLANG_DOUBLE_T_DEFINED)
typedef double double_t;
#define __DEFINED_double_t
#define __CLANG_DOUBLE_T_DEFINED
#endif


#if defined(__NEED_max_align_t) && !defined(__DEFINED_max_align_t) && !defined(__CLANG_MAX_ALIGN_T_DEFINED)
typedef struct { long long __ll; long double __ld; } max_align_t;
#define __DEFINED_max_align_t
#define __CLANG_MAX_ALIGN_T_DEFINED
#endif


#if defined(__NEED_time_t) && !defined(__DEFINED_time_t) && !defined(__CLANG_TIME_T_DEFINED)
typedef long time_t;
#define __DEFINED_time_t
#define __CLANG_TIME_T_DEFINED
#endif

#if defined(__NEED_suseconds_t) && !defined(__DEFINED_suseconds_t) && !defined(__CLANG_SUSECONDS_T_DEFINED)
typedef long suseconds_t;
#define __DEFINED_suseconds_t
#define __CLANG_SUSECONDS_T_DEFINED
#endif


#if defined(__NEED_pthread_attr_t) && !defined(__DEFINED_pthread_attr_t) && !defined(__CLANG_PTHREAD_ATTR_T_DEFINED)
typedef struct { union { int __i[9]; volatile int __vi[9]; unsigned __s[9]; } __u; } pthread_attr_t;
#define __DEFINED_pthread_attr_t
#define __CLANG_PTHREAD_ATTR_T_DEFINED
#endif

#if defined(__NEED_pthread_mutex_t) && !defined(__DEFINED_pthread_mutex_t) && !defined(__CLANG_PTHREAD_MUTEX_T_DEFINED)
typedef struct { union { int __i[6]; volatile int __vi[6]; volatile void *volatile __p[6]; } __u; } pthread_mutex_t;
#define __DEFINED_pthread_mutex_t
#define __CLANG_PTHREAD_MUTEX_T_DEFINED
#endif

#if defined(__NEED_mtx_t) && !defined(__DEFINED_mtx_t) && !defined(__CLANG_MTX_T_DEFINED)
typedef struct { union { int __i[6]; volatile int __vi[6]; volatile void *volatile __p[6]; } __u; } mtx_t;
#define __DEFINED_mtx_t
#define __CLANG_MTX_T_DEFINED
#endif

#if defined(__NEED_pthread_cond_t) && !defined(__DEFINED_pthread_cond_t) && !defined(__CLANG_PTHREAD_COND_T_DEFINED)
typedef struct { union { int __i[12]; volatile int __vi[12]; void *__p[12]; } __u; } pthread_cond_t;
#define __DEFINED_pthread_cond_t
#define __CLANG_PTHREAD_COND_T_DEFINED
#endif

#if defined(__NEED_cnd_t) && !defined(__DEFINED_cnd_t) && !defined(__CLANG_CND_T_DEFINED)
typedef struct { union { int __i[12]; volatile int __vi[12]; void *__p[12]; } __u; } cnd_t;
#define __DEFINED_cnd_t
#define __CLANG_CND_T_DEFINED
#endif

#if defined(__NEED_pthread_rwlock_t) && !defined(__DEFINED_pthread_rwlock_t) && !defined(__CLANG_PTHREAD_RWLOCK_T_DEFINED)
typedef struct { union { int __i[8]; volatile int __vi[8]; void *__p[8]; } __u; } pthread_rwlock_t;
#define __DEFINED_pthread_rwlock_t
#define __CLANG_PTHREAD_RWLOCK_T_DEFINED
#endif

#if defined(__NEED_pthread_barrier_t) && !defined(__DEFINED_pthread_barrier_t) && !defined(__CLANG_PTHREAD_BARRIER_T_DEFINED)
typedef struct { union { int __i[5]; volatile int __vi[5]; void *__p[5]; } __u; } pthread_barrier_t;
#define __DEFINED_pthread_barrier_t
#define __CLANG_PTHREAD_BARRIER_T_DEFINED
#endif

#if defined(__NEED_size_t) && !defined(__DEFINED_size_t) && !defined(__CLANG_SIZE_T_DEFINED)
typedef unsigned _Addr size_t;
#define __DEFINED_size_t
#define __CLANG_SIZE_T_DEFINED
#endif

#if defined(__NEED_uintptr_t) && !defined(__DEFINED_uintptr_t) && !defined(__CLANG_UINTPTR_T_DEFINED)
typedef unsigned _Addr uintptr_t;
#define __DEFINED_uintptr_t
#define __CLANG_UINTPTR_T_DEFINED
#endif

#if defined(__NEED_ptrdiff_t) && !defined(__DEFINED_ptrdiff_t) && !defined(__CLANG_PTRDIFF_T_DEFINED)
typedef _Addr ptrdiff_t;
#define __DEFINED_ptrdiff_t
#define __CLANG_PTRDIFF_T_DEFINED
#endif

#if defined(__NEED_ssize_t) && !defined(__DEFINED_ssize_t) && !defined(__CLANG_SSIZE_T_DEFINED)
typedef _Addr ssize_t;
#define __DEFINED_ssize_t
#define __CLANG_SSIZE_T_DEFINED
#endif

#if defined(__NEED_intptr_t) && !defined(__DEFINED_intptr_t) && !defined(__CLANG_INTPTR_T_DEFINED)
typedef _Addr intptr_t;
#define __DEFINED_intptr_t
#define __CLANG_INTPTR_T_DEFINED
#endif

#if defined(__NEED_regoff_t) && !defined(__DEFINED_regoff_t) && !defined(__CLANG_REGOFF_T_DEFINED)
typedef _Addr regoff_t;
#define __DEFINED_regoff_t
#define __CLANG_REGOFF_T_DEFINED
#endif

#if defined(__NEED_register_t) && !defined(__DEFINED_register_t) && !defined(__CLANG_REGISTER_T_DEFINED)
typedef _Reg register_t;
#define __DEFINED_register_t
#define __CLANG_REGISTER_T_DEFINED
#endif


#if defined(__NEED_int8_t) && !defined(__DEFINED_int8_t) && !defined(__CLANG_INT8_T_DEFINED)
typedef signed char     int8_t;
#define __DEFINED_int8_t
#define __CLANG_INT8_T_DEFINED
#endif

#if defined(__NEED_int16_t) && !defined(__DEFINED_int16_t) && !defined(__CLANG_INT16_T_DEFINED)
typedef short           int16_t;
#define __DEFINED_int16_t
#define __CLANG_INT16_T_DEFINED
#endif

#if defined(__NEED_int32_t) && !defined(__DEFINED_int32_t) && !defined(__CLANG_INT32_T_DEFINED)
typedef int             int32_t;
#define __DEFINED_int32_t
#define __CLANG_INT32_T_DEFINED
#endif

#if defined(__NEED_int64_t) && !defined(__DEFINED_int64_t) && !defined(__CLANG_INT64_T_DEFINED)
typedef _Int64          int64_t;
#define __DEFINED_int64_t
#define __CLANG_INT64_T_DEFINED
#endif

#if defined(__NEED_intmax_t) && !defined(__DEFINED_intmax_t) && !defined(__CLANG_INTMAX_T_DEFINED)
typedef _Int64          intmax_t;
#define __DEFINED_intmax_t
#define __CLANG_INTMAX_T_DEFINED
#endif

#if defined(__NEED_uint8_t) && !defined(__DEFINED_uint8_t) && !defined(__CLANG_UINT8_T_DEFINED)
typedef unsigned char   uint8_t;
#define __DEFINED_uint8_t
#define __CLANG_UINT8_T_DEFINED
#endif

#if defined(__NEED_uint16_t) && !defined(__DEFINED_uint16_t) && !defined(__CLANG_UINT16_T_DEFINED)
typedef unsigned short  uint16_t;
#define __DEFINED_uint16_t
#define __CLANG_UINT16_T_DEFINED
#endif

#if defined(__NEED_uint32_t) && !defined(__DEFINED_uint32_t) && !defined(__CLANG_UINT32_T_DEFINED)
typedef unsigned int    uint32_t;
#define __DEFINED_uint32_t
#define __CLANG_UINT32_T_DEFINED
#endif

#if defined(__NEED_uint64_t) && !defined(__DEFINED_uint64_t) && !defined(__CLANG_UINT64_T_DEFINED)
typedef unsigned _Int64 uint64_t;
#define __DEFINED_uint64_t
#define __CLANG_UINT64_T_DEFINED
#endif

#if defined(__NEED_u_int64_t) && !defined(__DEFINED_u_int64_t) && !defined(__CLANG_U_INT64_T_DEFINED)
typedef unsigned _Int64 u_int64_t;
#define __DEFINED_u_int64_t
#define __CLANG_U_INT64_T_DEFINED
#endif

#if defined(__NEED_uintmax_t) && !defined(__DEFINED_uintmax_t) && !defined(__CLANG_UINTMAX_T_DEFINED)
typedef unsigned _Int64 uintmax_t;
#define __DEFINED_uintmax_t
#define __CLANG_UINTMAX_T_DEFINED
#endif


#if defined(__NEED_mode_t) && !defined(__DEFINED_mode_t) && !defined(__CLANG_MODE_T_DEFINED)
typedef unsigned mode_t;
#define __DEFINED_mode_t
#define __CLANG_MODE_T_DEFINED
#endif

#if defined(__NEED_nlink_t) && !defined(__DEFINED_nlink_t) && !defined(__CLANG_NLINK_T_DEFINED)
typedef unsigned _Reg nlink_t;
#define __DEFINED_nlink_t
#define __CLANG_NLINK_T_DEFINED
#endif

#if defined(__NEED_off_t) && !defined(__DEFINED_off_t) && !defined(__CLANG_OFF_T_DEFINED)
typedef _Int64 off_t;
#define __DEFINED_off_t
#define __CLANG_OFF_T_DEFINED
#endif

#if defined(__NEED_ino_t) && !defined(__DEFINED_ino_t) && !defined(__CLANG_INO_T_DEFINED)
typedef unsigned _Int64 ino_t;
#define __DEFINED_ino_t
#define __CLANG_INO_T_DEFINED
#endif

#if defined(__NEED_dev_t) && !defined(__DEFINED_dev_t) && !defined(__CLANG_DEV_T_DEFINED)
typedef unsigned _Int64 dev_t;
#define __DEFINED_dev_t
#define __CLANG_DEV_T_DEFINED
#endif

#if defined(__NEED_blksize_t) && !defined(__DEFINED_blksize_t) && !defined(__CLANG_BLKSIZE_T_DEFINED)
typedef long blksize_t;
#define __DEFINED_blksize_t
#define __CLANG_BLKSIZE_T_DEFINED
#endif

#if defined(__NEED_blkcnt_t) && !defined(__DEFINED_blkcnt_t) && !defined(__CLANG_BLKCNT_T_DEFINED)
typedef _Int64 blkcnt_t;
#define __DEFINED_blkcnt_t
#define __CLANG_BLKCNT_T_DEFINED
#endif

#if defined(__NEED_fsblkcnt_t) && !defined(__DEFINED_fsblkcnt_t) && !defined(__CLANG_FSBLKCNT_T_DEFINED)
typedef unsigned _Int64 fsblkcnt_t;
#define __DEFINED_fsblkcnt_t
#define __CLANG_FSBLKCNT_T_DEFINED
#endif

#if defined(__NEED_fsfilcnt_t) && !defined(__DEFINED_fsfilcnt_t) && !defined(__CLANG_FSFILCNT_T_DEFINED)
typedef unsigned _Int64 fsfilcnt_t;
#define __DEFINED_fsfilcnt_t
#define __CLANG_FSFILCNT_T_DEFINED
#endif


#if defined(__NEED_wint_t) && !defined(__DEFINED_wint_t) && !defined(__CLANG_WINT_T_DEFINED)
typedef unsigned wint_t;
#define __DEFINED_wint_t
#define __CLANG_WINT_T_DEFINED
#endif

#if defined(__NEED_wctype_t) && !defined(__DEFINED_wctype_t) && !defined(__CLANG_WCTYPE_T_DEFINED)
typedef unsigned long wctype_t;
#define __DEFINED_wctype_t
#define __CLANG_WCTYPE_T_DEFINED
#endif


#if defined(__NEED_timer_t) && !defined(__DEFINED_timer_t) && !defined(__CLANG_TIMER_T_DEFINED)
typedef void * timer_t;
#define __DEFINED_timer_t
#define __CLANG_TIMER_T_DEFINED
#endif

#if defined(__NEED_clockid_t) && !defined(__DEFINED_clockid_t) && !defined(__CLANG_CLOCKID_T_DEFINED)
typedef int clockid_t;
#define __DEFINED_clockid_t
#define __CLANG_CLOCKID_T_DEFINED
#endif

#if defined(__NEED_clock_t) && !defined(__DEFINED_clock_t) && !defined(__CLANG_CLOCK_T_DEFINED)
typedef long clock_t;
#define __DEFINED_clock_t
#define __CLANG_CLOCK_T_DEFINED
#endif

#if defined(__NEED_struct_timeval) && !defined(__DEFINED_struct_timeval)
struct timeval { time_t tv_sec; suseconds_t tv_usec; };
#define __DEFINED_struct_timeval
#endif

#if defined(__NEED_struct_timespec) && !defined(__DEFINED_struct_timespec)
struct timespec { time_t tv_sec; long tv_nsec; };
#define __DEFINED_struct_timespec
#endif


#if defined(__NEED_pid_t) && !defined(__DEFINED_pid_t) && !defined(__CLANG_PID_T_DEFINED)
typedef int pid_t;
#define __DEFINED_pid_t
#define __CLANG_PID_T_DEFINED
#endif

#if defined(__NEED_id_t) && !defined(__DEFINED_id_t) && !defined(__CLANG_ID_T_DEFINED)
typedef unsigned id_t;
#define __DEFINED_id_t
#define __CLANG_ID_T_DEFINED
#endif

#if defined(__NEED_uid_t) && !defined(__DEFINED_uid_t) && !defined(__CLANG_UID_T_DEFINED)
typedef unsigned uid_t;
#define __DEFINED_uid_t
#define __CLANG_UID_T_DEFINED
#endif

#if defined(__NEED_gid_t) && !defined(__DEFINED_gid_t) && !defined(__CLANG_GID_T_DEFINED)
typedef unsigned gid_t;
#define __DEFINED_gid_t
#define __CLANG_GID_T_DEFINED
#endif

#if defined(__NEED_key_t) && !defined(__DEFINED_key_t) && !defined(__CLANG_KEY_T_DEFINED)
typedef int key_t;
#define __DEFINED_key_t
#define __CLANG_KEY_T_DEFINED
#endif

#if defined(__NEED_useconds_t) && !defined(__DEFINED_useconds_t) && !defined(__CLANG_USECONDS_T_DEFINED)
typedef unsigned useconds_t;
#define __DEFINED_useconds_t
#define __CLANG_USECONDS_T_DEFINED
#endif


#ifdef __cplusplus
#if defined(__NEED_pthread_t) && !defined(__DEFINED_pthread_t) && !defined(__CLANG_PTHREAD_T_DEFINED)
typedef unsigned long pthread_t;
#define __DEFINED_pthread_t
#define __CLANG_PTHREAD_T_DEFINED
#endif

#else
#if defined(__NEED_pthread_t) && !defined(__DEFINED_pthread_t) && !defined(__CLANG_PTHREAD_T_DEFINED)
typedef struct __pthread * pthread_t;
#define __DEFINED_pthread_t
#define __CLANG_PTHREAD_T_DEFINED
#endif

#endif
#if defined(__NEED_pthread_once_t) && !defined(__DEFINED_pthread_once_t) && !defined(__CLANG_PTHREAD_ONCE_T_DEFINED)
typedef int pthread_once_t;
#define __DEFINED_pthread_once_t
#define __CLANG_PTHREAD_ONCE_T_DEFINED
#endif

#if defined(__NEED_pthread_key_t) && !defined(__DEFINED_pthread_key_t) && !defined(__CLANG_PTHREAD_KEY_T_DEFINED)
typedef unsigned pthread_key_t;
#define __DEFINED_pthread_key_t
#define __CLANG_PTHREAD_KEY_T_DEFINED
#endif

#if defined(__NEED_pthread_spinlock_t) && !defined(__DEFINED_pthread_spinlock_t) && !defined(__CLANG_PTHREAD_SPINLOCK_T_DEFINED)
typedef int pthread_spinlock_t;
#define __DEFINED_pthread_spinlock_t
#define __CLANG_PTHREAD_SPINLOCK_T_DEFINED
#endif

#if defined(__NEED_pthread_mutexattr_t) && !defined(__DEFINED_pthread_mutexattr_t) && !defined(__CLANG_PTHREAD_MUTEXATTR_T_DEFINED)
typedef struct { unsigned __attr; } pthread_mutexattr_t;
#define __DEFINED_pthread_mutexattr_t
#define __CLANG_PTHREAD_MUTEXATTR_T_DEFINED
#endif

#if defined(__NEED_pthread_condattr_t) && !defined(__DEFINED_pthread_condattr_t) && !defined(__CLANG_PTHREAD_CONDATTR_T_DEFINED)
typedef struct { unsigned __attr; } pthread_condattr_t;
#define __DEFINED_pthread_condattr_t
#define __CLANG_PTHREAD_CONDATTR_T_DEFINED
#endif

#if defined(__NEED_pthread_barrierattr_t) && !defined(__DEFINED_pthread_barrierattr_t) && !defined(__CLANG_PTHREAD_BARRIERATTR_T_DEFINED)
typedef struct { unsigned __attr; } pthread_barrierattr_t;
#define __DEFINED_pthread_barrierattr_t
#define __CLANG_PTHREAD_BARRIERATTR_T_DEFINED
#endif

#if defined(__NEED_pthread_rwlockattr_t) && !defined(__DEFINED_pthread_rwlockattr_t) && !defined(__CLANG_PTHREAD_RWLOCKATTR_T_DEFINED)
typedef struct { unsigned __attr[2]; } pthread_rwlockattr_t;
#define __DEFINED_pthread_rwlockattr_t
#define __CLANG_PTHREAD_RWLOCKATTR_T_DEFINED
#endif


#if defined(__NEED_FILE) && !defined(__DEFINED_FILE) && !defined(__CLANG_FILE_DEFINED)
typedef struct _IO_FILE FILE;
#define __DEFINED_FILE
#define __CLANG_FILE_DEFINED
#endif


#if defined(__NEED_mbstate_t) && !defined(__DEFINED_mbstate_t) && !defined(__CLANG_MBSTATE_T_DEFINED)
typedef struct __mbstate_t { unsigned __opaque1, __opaque2; } mbstate_t;
#define __DEFINED_mbstate_t
#define __CLANG_MBSTATE_T_DEFINED
#endif


#if defined(__NEED_locale_t) && !defined(__DEFINED_locale_t) && !defined(__CLANG_LOCALE_T_DEFINED)
typedef struct __locale_struct * locale_t;
#define __DEFINED_locale_t
#define __CLANG_LOCALE_T_DEFINED
#endif


#if defined(__NEED_sigset_t) && !defined(__DEFINED_sigset_t) && !defined(__CLANG_SIGSET_T_DEFINED)
typedef struct __sigset_t { unsigned long __bits[128/sizeof(long)]; } sigset_t;
#define __DEFINED_sigset_t
#define __CLANG_SIGSET_T_DEFINED
#endif


#if defined(__NEED_struct_iovec) && !defined(__DEFINED_struct_iovec)
struct iovec { void *iov_base; size_t iov_len; };
#define __DEFINED_struct_iovec
#endif


#if defined(__NEED_socklen_t) && !defined(__DEFINED_socklen_t) && !defined(__CLANG_SOCKLEN_T_DEFINED)
typedef unsigned socklen_t;
#define __DEFINED_socklen_t
#define __CLANG_SOCKLEN_T_DEFINED
#endif

#if defined(__NEED_sa_family_t) && !defined(__DEFINED_sa_family_t) && !defined(__CLANG_SA_FAMILY_T_DEFINED)
typedef unsigned short sa_family_t;
#define __DEFINED_sa_family_t
#define __CLANG_SA_FAMILY_T_DEFINED
#endif


#undef _Addr
#undef _Int64
#undef _Reg
