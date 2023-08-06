#pragma once

#include "vmprof.h"
#include "machine.h"
#include "compat.h"

#include <stddef.h>
#include <time.h>
#include <stdlib.h>

#ifndef VMPROF_WINDOWS
#include <sys/time.h>
#include "vmprof_mt.h"
#endif

#ifdef VMPROF_LINUX
#include <syscall.h>
#endif

#define MAX_FUNC_NAME 1024

static long prepare_interval_usec = 0;
static long profile_interval_usec = 0;

static int opened_profile(const char *interp_name, int memory, int proflines, int native, int real_time);

#ifdef VMPROF_UNIX
static int signal_type = SIGPROF;
static int itimer_type = ITIMER_PROF;
static pthread_t *threads = NULL;
static size_t threads_size = 0;
static size_t thread_count = 0;
static size_t threads_size_step = 8;
static struct profbuf_s *volatile current_codes;
#endif

#ifdef VMPROF_UNIX

static inline ssize_t search_thread(pthread_t tid, ssize_t i) {
    if (i < 0)
        i = 0;
    while ((size_t)i < thread_count) {
        if (pthread_equal(threads[i], tid))
            return i;
        i++;
    }
    return -1;
}

ssize_t insert_thread(pthread_t tid, ssize_t i) {
    assert(signal_type == SIGALRM);
    i = search_thread(tid, i);
    if (i > 0)
        return -1;
    if (thread_count == threads_size) {
        threads_size += threads_size_step;
        threads = realloc(threads, sizeof(pid_t) * threads_size);
        assert(threads != NULL);
        memset(threads + thread_count, 0, sizeof(pid_t) * threads_size_step);
    }
    threads[thread_count++] = tid;
    return thread_count;
}

ssize_t remove_thread(pthread_t tid, ssize_t i) {
    assert(signal_type == SIGALRM);
    if (thread_count == 0)
        return -1;
    if (threads == NULL)
        return -1;
    i = search_thread(tid, i);
    if (i < 0)
        return -1;
    threads[i] = threads[--thread_count];
    threads[thread_count] = 0;
    return thread_count;
}

ssize_t remove_threads(void) {
    assert(signal_type == SIGALRM);
    if (threads != NULL) {
        free(threads);
        threads = NULL;
    }
    thread_count = 0;
    threads_size = 0;
    return 0;
}

#endif

#define MAX_STACK_DEPTH   \
    ((SINGLE_BUF_SIZE - sizeof(struct prof_stacktrace_s)) / sizeof(void *))

/*
 * NOTE SHOULD NOT BE DONE THIS WAY. Here is an example why:
 * assume the following struct content:
 * struct ... {
 *    char padding[sizeof(long) - 1];
 *    char marker;
 *    long count, depth;
 *    void *stack[];
 * }
 *
 * Here a table of the offsets on a 64 bit machine:
 * field  | GCC | VSC (windows)
 * ---------------------------
 * marker |   7 |   3
 * count  |   8 |   4
 * depth  |  16 |   8
 * stack  |  24 |   16 (VSC adds 4 padding byte hurray!)
 *
 * This means that win32 worked by chance (because sizeof(void*)
 * is 4, but fails on win32
 */
typedef struct prof_stacktrace_s {
#ifdef VMPROF_WINDOWS
    // if padding is 8 bytes, then on both 32bit and 64bit, the
    // stack field is aligned
    char padding[sizeof(void*) - 1];
#else
    char padding[sizeof(long) - 1];
#endif
    char marker;
    long count, depth;
    void *stack[];
} prof_stacktrace_s;

#define SIZEOF_PROF_STACKTRACE sizeof(long)+sizeof(long)+sizeof(char)

RPY_EXTERN
char *vmprof_init(int fd, double interval, int memory,
                  int proflines, const char *interp_name, int native, int real_time)
{
    if (!(interval >= 1e-6 && interval < 1.0)) {   /* also if it is NaN */
        return "bad value for 'interval'";
    }
    prepare_interval_usec = (int)(interval * 1000000.0);

    if (prepare_concurrent_bufs() < 0)
        return "out of memory";
#if VMPROF_UNIX
    if (real_time) {
        signal_type = SIGALRM;
        itimer_type = ITIMER_REAL;
    } else {
        signal_type = SIGPROF;
        itimer_type = ITIMER_PROF;
    }
    current_codes = NULL;
    assert(fd >= 0);
#else
    if (memory) {
        return "memory tracking only supported on unix";
    }
    if (native) {
        return "native profiling only supported on unix";
    }
#endif
    vmp_set_profile_fileno(fd);
    if (opened_profile(interp_name, memory, proflines, native, real_time) < 0) {
        vmp_set_profile_fileno(0);
        return strerror(errno);
    }
    return NULL;
}

static int opened_profile(const char *interp_name, int memory, int proflines, int native, int real_time)
{
    int success;
    int bits;
    struct {
        long hdr[5];
        char interp_name[259];
    } header;

    const char * machine;
    size_t namelen = strnlen(interp_name, 255);

    machine = vmp_machine_os_name();

    header.hdr[0] = 0;
    header.hdr[1] = 3;
    header.hdr[2] = 0;
    header.hdr[3] = prepare_interval_usec;
    if (strstr(machine, "win64") != 0) {
        header.hdr[4] = 1;
    } else {
        header.hdr[4] = 0;
    }
    header.interp_name[0] = MARKER_HEADER;
    header.interp_name[1] = '\x00';
    header.interp_name[2] = VERSION_TIMESTAMP;
    header.interp_name[3] = memory*PROFILE_MEMORY + proflines*PROFILE_LINES + \
                            native*PROFILE_NATIVE + real_time*PROFILE_REAL_TIME;
#ifdef RPYTHON_VMPROF
    header.interp_name[3] += PROFILE_RPYTHON;
#endif
    header.interp_name[4] = (char)namelen;

    memcpy(&header.interp_name[5], interp_name, namelen);
    success = vmp_write_all((char*)&header, 5 * sizeof(long) + 5 + namelen);
    if (success < 0) {
        return success;
    }

    /* Write the time and the zone to the log file, profiling will start now */
    (void)vmp_write_time_now(MARKER_TIME_N_ZONE);

    /* write some more meta information */
    vmp_write_meta("os", machine);
    bits = vmp_machine_bits();
    if (bits == 64) {
        vmp_write_meta("bits", "64");
    } else if (bits == 32) {
        vmp_write_meta("bits", "32");
    }

    return success;
}


/* Seems that CPython 3.5.1 made our job harder.  Did not find out how
   to do that without these hacks.  We can't use PyThreadState_GET(),
   because that calls PyThreadState_Get() which fails an assert if the
   result is NULL. */
#if PY_MAJOR_VERSION >= 3 && !defined(_Py_atomic_load_relaxed)
                             /* this was abruptly un-defined in 3.5.1 */
void *volatile _PyThreadState_Current;
   /* XXX simple volatile access is assumed atomic */
#  define _Py_atomic_load_relaxed(pp)  (*(pp))
#endif

#ifdef RPYTHON_VMPROF
#ifndef RPYTHON_LL2CTYPES
static PY_STACK_FRAME_T *get_vmprof_stack(void)
{
    struct pypy_threadlocal_s *tl;
    _OP_THREADLOCALREF_ADDR_SIGHANDLER(tl);
    if (tl == NULL)
        return NULL;
    else
        return tl->vmprof_tl_stack;
}
#else
static PY_STACK_FRAME_T *get_vmprof_stack(void)
{
    return 0;
}
#endif

RPY_EXTERN
intptr_t vmprof_get_traceback(void *stack, void *ucontext,
                              intptr_t *result_p, intptr_t result_length)
{
    int n;
    int enabled;
#ifdef VMPROF_WINDOWS
    intptr_t pc = 0;   /* XXX implement me */
#else
    intptr_t pc = ucontext ? (intptr_t)GetPC((ucontext_t *)ucontext) : 0;
#endif
    if (stack == NULL) {
        stack = get_vmprof_stack();
    }
#ifdef VMP_SUPPORTS_NATIVE_PROFILING
    enabled = vmp_native_enabled();
    vmp_native_disable();
#endif
    n = get_stack_trace(stack, result_p, result_length - 2, pc);
#ifdef VMP_SUPPORTS_NATIVE_PROFILING
    if (enabled) {
        vmp_native_enable();
    }
#endif
    return (intptr_t)n;
}
#endif
