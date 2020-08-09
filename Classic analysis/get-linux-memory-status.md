# C/C++ tip: How to get the physical memory size of a system

September 14, 2012  

Topics: [C/C++](http://nadeausoftware.com/articles/c_c)

API functions  to get  the size of physical memory (RAM) differ between Windows, Linux, OSX, AIX, BSD, Solaris, and other UNIX-style OSes. **This article provides a cross-platform function  to  get the physical memory size,  and explains what works on what OS.**

## Table of Contents

1.  [How to get physical memory size](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#Howtogetphysicalmemorysize)

1.  [Code](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#Code)
2.  [Usage](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#Usage)
3.  [Discussion](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#Discussion)

1.  [GlobalMemoryStatus( ) and GlobalMemoryStatusEx( )](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#GlobalMemoryStatusnbspandGlobalMemoryStatusEx)
2.  [sysconf( )](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#sysconfnbsp)
3.  [sysctl( )](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#sysctl)
4.  [sysinfo( )](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#sysinfonbsp)
5.  [/proc/meminfo](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#procmeminfo)
6.  [Other](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#Other)
5.  [Downloads](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#Downloads)
6.  [Further reading](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#Furtherreading)

1.  [Related articles at NadeauSoftware.com](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#RelatedarticlesatNadeauSoftwarecom)
2.  [Web articles](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#Webarticles)

## How to get physical memory size

Physical memory is the RAM installed on a system.  The size of physical memory is a hard upper bound on the size of a process before parts of it have to be paged to disk or SSD. In practice, some of physical memory is permanently allocated to the kernel and other services that have to stay resident in memory. The remainder of physical memory is managed by the OS and shared among all running processes. No one process will ever get all of physical memory.

Each OS has command-line or user interface tools to report the physical memory size, but checking it programmatically is useful for large high-performance code that automatically adjusts memory use to different system sizes. Unfortunately, API functions to get the memory size are not standardized and differ from OS to OS.

### Code

The following    **`getMemorySize( )`** function works for most OSes (copy and paste, or download [getMemorySize.c](http://nadeausoftware.com/sites/NadeauSoftware.com/files/getMemorySize.c)). Linking with the default libraries is sufficient.

See the sections that follow for discussion, caveats, and why this code requires so many `#ifdef`'s.

```
<pre class="code-example">
/*
 * Author:  David Robert Nadeau
 * Site:    http://NadeauSoftware.com/
 * License: Creative Commons Attribution 3.0 Unported License
 *          http://creativecommons.org/licenses/by/3.0/deed.en_US
 */
#if defined(_WIN32)

#include <Windows.h>

#elif defined(__unix__) || defined(__unix) || defined(unix) || (defined(__APPLE__) && defined(__MACH__))
#include <unistd.h>
#include <sys/types.h>
#include <sys/param.h>
#if defined(BSD)
#include <sys/sysctl.h>
#endif

#else
#error "Unable to define getMemorySize( ) for an unknown OS."
#endif

/**
 * Returns the size of physical memory (RAM) in bytes.
 */
size_t **getMemorySize**( )
{
#if defined(_WIN32) && (defined(__CYGWIN__) || defined(__CYGWIN32__))
	/* Cygwin under Windows. ------------------------------------ */
	/* New 64-bit MEMORYSTATUSEX isn't available.  Use old 32.bit */
	MEMORYSTATUS status;
	status.dwLength = sizeof(status);
	GlobalMemoryStatus( &status );
	return (size_t)status.dwTotalPhys;

#elif defined(_WIN32)
	/* Windows. ------------------------------------------------- */
	/* Use new 64-bit MEMORYSTATUSEX, not old 32-bit MEMORYSTATUS */
	MEMORYSTATUSEX status;
	status.dwLength = sizeof(status);
	GlobalMemoryStatusEx( &status );
	return (size_t)status.ullTotalPhys;

#elif defined(__unix__) || defined(__unix) || defined(unix) || (defined(__APPLE__) && defined(__MACH__))
	/* UNIX variants. ------------------------------------------- */
	/* Prefer sysctl() over sysconf() except sysctl() HW_REALMEM and HW_PHYSMEM */

#if defined(CTL_HW) && (defined(HW_MEMSIZE) || defined(HW_PHYSMEM64))
	int mib[2];
	mib[0] = CTL_HW;
#if defined(HW_MEMSIZE)
	mib[1] = HW_MEMSIZE;            /* OSX. --------------------- */
#elif defined(HW_PHYSMEM64)
	mib[1] = HW_PHYSMEM64;          /* NetBSD, OpenBSD. --------- */
#endif
	int64_t size = 0;               /* 64-bit */
	size_t len = sizeof( size );
	if ( sysctl( mib, 2, &size, &len, NULL, 0 ) == 0 )
		return (size_t)size;
	return 0L;			/* Failed? */

#elif defined(_SC_AIX_REALMEM)
	/* AIX. ----------------------------------------------------- */
	return (size_t)sysconf( _SC_AIX_REALMEM ) * (size_t)1024L;

#elif defined(_SC_PHYS_PAGES) && defined(_SC_PAGESIZE)
	/* FreeBSD, Linux, OpenBSD, and Solaris. -------------------- */
	return (size_t)sysconf( _SC_PHYS_PAGES ) *
		(size_t)sysconf( _SC_PAGESIZE );

#elif defined(_SC_PHYS_PAGES) && defined(_SC_PAGE_SIZE)
	/* Legacy. -------------------------------------------------- */
	return (size_t)sysconf( _SC_PHYS_PAGES ) *
		(size_t)sysconf( _SC_PAGE_SIZE );

#elif defined(CTL_HW) && (defined(HW_PHYSMEM) || defined(HW_REALMEM))
	/* DragonFly BSD, FreeBSD, NetBSD, OpenBSD, and OSX. -------- */
	int mib[2];
	mib[0] = CTL_HW;
#if defined(HW_REALMEM)
	mib[1] = HW_REALMEM;		/* FreeBSD. ----------------- */
#elif defined(HW_PYSMEM)
	mib[1] = HW_PHYSMEM;		/* Others. ------------------ */
#endif
	unsigned int size = 0;		/* 32-bit */
	size_t len = sizeof( size );
	if ( sysctl( mib, 2, &size, &len, NULL, 0 ) == 0 )
		return (size_t)size;
	return 0L;			/* Failed? */
#endif /* sysctl and sysconf variants */

#else
	return 0L;			/* Unknown OS. */
#endif
}
</pre>
```

### Usage

Just call the function to get the memory size in bytes. If the returned value is zero, the call failed due to OS limitations.

<pre>
size_t memorySize = **getMemorySize**( );
</pre>

## Discussion

Each OS has one or more ways of getting  the physical memory size:

OS                | CPU time                                                                      
----------------- | ------------------------------------------------------------------------------
**AIX**           | `sysconf( ) with _SC_AIX_REALMEM`                                             
**Cygwin**        | `GlobalMemoryStatus( )`                                                       
**DragonFly BSD** | `sysctl( ) with HW_PHYSMEM`                                                   
**FreeBSD**       | `sysconf( ) with _SC_PHYS_PAGES, or sysctl( ) with HW_REALMEM or HW_PHYSMEM`  
**Linux**         | `sysconf( ) with _SC_PHYS_PAGES,  sysinfo( ), or /proc/meminfo`               
**NetBSD**        | `sysctl( ) with HW_PHYSMEM64 or HW_PHYSMEM`                                   
**OpenBSD**       | `sysconf( ) with _SC_PHYS_PAGES, or sysctl( ) with HW_PHYSMEM64 or HW_PHYSMEM`
**OSX**           | `sysconf( ) with _SC_PHYS_PAGES, or sysctl( ) with HW_MEMSIZE or HW_PHYSMEM`  
**Solaris**       | `sysconf( ) with _SC_PHYS_PAGES`                                              
**Windows**       | `GlobalMemoryStatus( ) or GlobalMemoryStatusEx( )`                            

Each of these is discussed below.

### GlobalMemoryStatus( ) and GlobalMemoryStatusEx( )

On Windows and  [Cygwin](http://www.cygwin.com/) (Linux compatibility  for Windows), the [`GlobalMemoryStatus( )`](http://msdn.microsoft.com/en-us/library/aa366586.aspx) function fills a [`MEMORYSTATUS`](http://msdn.microsoft.com/en-us/library/aa366772.aspx) struct with information about system memory. Structure fields include:

<pre>
typedef struct _MEMORYSTATUS {
	DWORD  dwLength;
	DWORD  dwMemoryLoad;
	**SIZE_T dwTotalPhys;**
	SIZE_T dwAvailPhys;
	SIZE_T dwTotalPageFile;
	SIZE_T dwAvailPageFile;
	SIZE_T dwTotalVirtual;
	SIZE_T dwAvailVirtual;
} MEMORYSTATUS, *LPMEMORYSTATUS;
</pre>

The `dwTotalPhys` field contains the physical memory size in bytes. _However_, the field is only large enough to hold a 32-bit integer. For systems with more than 4 Gbytes of memory, the field is set to -1.

On Windows, but not Cygwin, the new  [`GlobalMemoryStatusEx( )`](http://msdn.microsoft.com/en-us/library/aa366589(VS.85).aspx) function fills a 64-bit safe [`MEMORYSTATUSEX`](http://msdn.microsoft.com/en-us/library/aa366770(v=vs.85).aspx) struct with information about physical and virtual memory. Structure fields include:

<pre>
typedef struct _MEMORYSTATUSEX {
	DWORD     dwLength;
	DWORD     dwMemoryLoad;
	**DWORDLONG ullTotalPhys;**
	DWORDLONG ullAvailPhys;
	DWORDLONG ullTotalPageFile;
	DWORDLONG ullAvailPageFile;
	DWORDLONG ullTotalVirtual;
	DWORDLONG ullAvailVirtual;
	DWORDLONG ullAvailExtendedVirtual;
} MEMORYSTATUSEX, *LPMEMORYSTATUSEX;
</pre>

The 64-bit `ullTotalPhys` field contains the physical memory size in bytes.

_Beware:_ The [`GetPhysicallyInstalledSystemMemory( )`](http://msdn.microsoft.com/en-us/library/windows/desktop/cc300158(v=vs.85).aspx) function (from Vista onwards) returns the size of _all_ memory installed on the system. This value comes from the BIOS and may be larger than the value reported by `GlobalMemoryStatusEx( )` if the BIOS and low level drivers reserve some memory for memory-mapped devices. While the value from `GetPhysicallyInstalledSystemMemory( )` may be more literally correct, it's less useful. The amount of memory actually available for use by the OS and processes is usually what we want.

**Availability:** Cygwin and Windows XP and later.

Get memory size:

<pre>
\#include <Windows.h>
...

\#if defined(__CYGWIN__) || defined(__CYGWIN32__)
	MEMORYSTATUS status;
	status.dwLength = sizeof(status);
	**GlobalMemoryStatus**( &status );
	return (size_t)status.dwTotalPhys;
\#else
	MEMORYSTATUSEX status;
	status.dwLength = sizeof(status);
	**GlobalMemoryStatusEx**( &status );
	return (size_t)status.ullTotalPhys;
#endif
</pre>

### sysconf( )

On AIX, FreeBSD, Linux, OpenBSD,  and Solaris, `sysconf( )` returns  basic system configuration information (see man pages for [AIX,](http://pic.dhe.ibm.com/infocenter/aix/v7r1/index.jsp?topic=/com.ibm.aix.basetechref/doc/basetrf2/sysconf.htm) [FreeBSD,](http://www.freebsd.org/cgi/man.cgi?query=sysconf&apropos=0&sektion=3&manpath=FreeBSD+9-current&arch=default&format=html) [Linux,](http://www.kernel.org/doc/man-pages/online/pages/man3/sysconf.3.html) [OpenBSD](http://www.openbsd.org/cgi-bin/man.cgi?query=sysconf&sektion=3&format=html), [OSX,](http://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man3/sysconf.3.html) and [Solaris](http://docs.oracle.com/cd/E19683-01/816-0213/6m6ne38dd/index.html)). For FreeBSD and OpenBSD,  the function is available but  `sysctl( )`  provides more information and a more accurate measure of physical memory (see below).

The `sysconf( )` function takes an attribute argument and returns a long integer giving the attribute's value. Though `sysconf( )` is defined by POSIX, the  attribute for physical memory size is not standardized and varies among the OSes:

OS                                    | sysconf( ) attribute | Value                            
------------------------------------- | -------------------- | ---------------------------------
**AIX**                               | `_SC_AIX_REALMEM`    | Physical memory size in kilobytes
**FreeBSD, Linux, OpenBSD,  Solaris** | `_SC_PHYS_PAGES`     | Physical memory size in pages    

For  `_SC_AIX_REALMEM`, the return value is in kilobytes.

For `_SC_PHYS_PAGES`, the return value is in pages. To convert to bytes, multiply it by the page size from `sysconf( )` using the `_SC_PAGESIZE` (or legacy `_SC_PAGE_SIZE`) attribute. FreeBSD, Linux, and OpenBSD, also provide a `[getPageSize( )](http://www.kernel.org/doc/man-pages/online/pages/man2/getpagesize.2.html)` function that returns the same value. The physical memory size calculated using the page size is rounded down to the nearest page boundary and may be a bit less than the actual memory on the system.

**Availability:** AIX, FreeBSD, Linux, OpenBSD,  and Solaris.

Get  memory size:

<pre>
#include <sys/sysctl.h>
#include <sys/types.h>
...

#if defined(_SC_AIX_REALMEM)
	return (size_t)**sysconf**( _SC_AIX_REALMEM ) * (size_t)1024L;

#elif defined(_SC_PHYS_PAGES) && defined(_SC_PAGESIZE)
	return (size_t)**sysconf**( _SC_PHYS_PAGES ) * (size_t)**sysconf**( _SC_PAGESIZE );

#elif defined(_SC_PHYS_PAGES) && defined(_SC_PAGE_SIZE)
	return (size_t)**sysconf**( _SC_PHYS_PAGES ) * (size_t)**sysconf**( _SC_PAGE_SIZE );
#endif
</pre>

### sysctl( )

On BSD and OSX, `sysctl( )` is the preferred method to get  a wide variety of system configuration information (see man pages for [DragonFly BSD,](http://leaf.dragonflybsd.org/cgi/web-man?command=sysctl&section=3) [FreeBSD,](http://www.freebsd.org/cgi/man.cgi?query=sysctl&apropos=0&sektion=3&manpath=FreeBSD+9-current&arch=default&format=html) [NetBSD](http://netbsd.gw.com/cgi-bin/man-cgi?sysctl+3+NetBSD-current), [OpenBSD,](http://www.openbsd.org/cgi-bin/man.cgi?query=sysctl&apropos=0&sektion=3&manpath=OpenBSD+Current&arch=i386&format=html) and [OSX](http://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man3/sysctl.3.html#//apple_ref/doc/man/3/sysctl)). Linux also provides the function, but it's [deprecated and strongly discouraged](http://www.kernel.org/doc/man-pages/online/pages/man2/sysctl.2.html) in favor of `sysconf( )` (see above).

The `sysctl( )` function takes an array of integers that select a configuration attribute to query. On success, the function fills a variable with the attribute's value. Attributes are grouped hierarchically and include information about system hardware, the kernel, the network, virtual memory, and more. Hardware attributes are grouped under `CTL_HW`. The hardware attribute for physical memory size varies among the OSes:

OS                                               | CTL_HW attribute | Value                                         
------------------------------------------------ | ---------------- | ----------------------------------------------
**FreeBSD**                                      | `HW_REALMEM`     | Physical memory size in bytes (32-bit integer)
**DragonFly BSD, FreeBSD, NetBSD, OpenBSD, OSX** | `HW_PHYSMEM`     | Physical memory size in bytes (32-bit integer)
**NetBSD, OpenBSD**                              | `HW_PHYSMEM64`   | Physical memory size in bytes (64-bit integer)
**OSX**                                          | `HW_MEMSIZE`     | Physical memory size in bytes (64-bit integer)

The older `HW_PHYSMEM` attribute is available for BSD and OSX, but it returns a 32-bit unsigned integer that's  too small to hold memory sizes larger than 2 Gbytes. For memory size as a _64-bit integer_, use `HW_PHYSMEM64` on NetBSD and OpenBSD, and `HW_MEMSIZE` on OSX. Unfortunately, FreeBSD and DragonFly BSD currently do not support an attribute to get the memory size in 64-bits.

FreeBSD and OpenBSD provide both `sysctl( )` and `sysconf( )` (see above) to get the physical memory size. The `sysctl( )` method is more accurate since it returns the size in bytes, while `sysconf( )` returns the size rounded down to the nearest page boundary.

FreeBSD provides both `HW_REALMEM` and `HW_PHYSMEM`. Both return 32-bit integers, but `HW_PHYSMEM`'s value is rounded down to the nearest page boundary, like the value computed from `sysconf( )`, while `HW_REALMEM`'s value is not. Between, `HW_PHYSMEM` and `sysconf( )`, the latter is the better choice. While `sysconf( )` returns a 32-bit integer too, it's in units of the page size, which is usually 4 Kbytes. This adds another 12 bits to the maximum memory size that can be reported (which is 16 Tbytes).

**Availability:** DragonFly BSD, FreeBSD, NetBSD, OpenBSD, and OSX.

Get  memory size: 

<pre>
#include <unistd.h>
...

	int mib[2];
	mib[0] = CTL_HW;
#if defined(HW_MEMSIZE)
	mib[1] = HW_MEMSIZE;		/* OSX. --------------------- */
	int64_t size = 0;		/* 64-bit */
#elif defined(HW_PHYSMEM64)
	mib[1] = HW_PHYSMEM64;		/* NetBSD, OpenBSD. --------- */
	int64_t size = 0;		/* 64-bit */
#elif defined(HW_REALMEM)
	mib[1] = HW_REALMEM;		/* FreeBSD. ----------------- */
	unsigned int size = 0;		/* 32-bit */
#elif defined(HW_PHYSMEM)
	mib[1] = HW_PHYSMEM;		/* DragonFly BSD. ----------- */
	unsigned int size = 0;		/* 32-bit */
#endif
	size_t len = sizeof( size );
	if ( sysctl( mib, 2, &size, &len, NULL, 0 ) == 0 )
		return (size_t)size;
	return 0L;	
</pre>

### sysinfo( )

On Linux, the `sysinfo( )` function fills a `sysinfo` struct with system statistics. The struct has the following fields:

<pre>
struct sysinfo {
	long uptime;   		 /* Seconds since boot */
	unsigned long loads[3];  /* 1, 5, and 15 minute load averages */
	**unsigned long totalram;  /* Total usable main memory size */**
	unsigned long freeram;   /* Available memory size */
	unsigned long sharedram; /* Amount of shared memory */
	unsigned long bufferram; /* Memory used by buffers */
	unsigned long totalswap; /* Total swap space size */
	unsigned long freeswap;  /* swap space still available */
	unsigned short procs;    /* Number of current processes */
	unsigned long totalhigh; /* Total high memory size */
	unsigned long freehigh;  /* Available high memory size */
	unsigned int mem_unit;   /* Memory unit size in bytes */
	char _f[20-2*sizeof(long)-sizeof(int)]; /* Padding for libc5 */
};
</pre>

Prior to Linux 2.3.23 (late 2003), the `sysinfo` struct omitted the last four fields and all sizes were in bytes. Today, the larger struct is used and all sizes are in units  given by the `mem_unit` field. The `totalram` field times the `mem_unit` field gives the size of physical memory in bytes.

The memory size computed from the `sysinfo` struct is the same as that computed from `sysconf( )` and the page size (see above). Since the method is redundant, this article's `getMemorySize( )` function uses `sysconf( )` instead of `sysinfo( )`.

**Availability:** Linux.

Get memory size:

<pre>
#include <sys/sysinfo.h>
...

struct sysinfo info;
**sysinfo**( &info );
return (size_t)info.totalram * (size_t)info.mem_unit;
</pre>

### /proc/meminfo

On Linux, the [`/proc`](http://www.kernel.org/doc/man-pages/online/pages/man5/proc.5.html) pseudo-file system includes several pseudo-files filled with system configuration information. `/proc/meminfo` contains detailed information about memory use. Here's sample output from 64-bit Ubuntu Linux 12:

<pre>
**MemTotal:        3016120 kB**
MemFree:         2188204 kB
Buffers:           25852 kB
Cached:           322260 kB
SwapCached:            0 kB
Active:           420580 kB
Inactive:         293120 kB
Active(anon):     366248 kB
Inactive(anon):    16356 kB
Active(file):      54332 kB
Inactive(file):   276764 kB
Unevictable:          12 kB
Mlocked:              12 kB
SwapTotal:       1046524 kB
SwapFree:        1046524 kB
Dirty:                16 kB
Writeback:             0 kB
AnonPages:        365632 kB
Mapped:            94504 kB
Shmem:             17016 kB
Slab:              37596 kB
SReclaimable:      19352 kB
SUnreclaim:        18244 kB
KernelStack:        2552 kB
PageTables:        22428 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:     2554584 kB
Committed_AS:    2037044 kB
VmallocTotal:   34359738367 kB
VmallocUsed:       21548 kB
VmallocChunk:   34359713720 kB
HardwareCorrupted:     0 kB
AnonHugePages:         0 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
DirectMap4k:       38848 kB
DirectMap2M:     3106816 kB
</pre>

The format of the file varies a little from Linux to Linux, but all of them have a **MemTotal** line giving the _usable_ physical memory size in kilobytes. This value may be a bit less than actual physical memory since it excludes memory used by the kernel.

Parsing `/proc/meminfo` is slower and more involved than calling `sysinfo( )` or `sysconf( )` (see above). This article's `getMemorySize( )` function therefore uses the simpler `sysconf( )`.

**Availability:** Linux.

Get memory size:

<pre>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
...

	FILE* fp = fopen( "**/proc/meminfo**", "r" );
	if ( fp != NULL )
	{
		size_t bufsize = 1024 * sizeof(char);
		char* buf      = (char*)malloc( bufsize );
		long value     = -1L;
		while ( getline( &buf, &bufsize, fp ) >= 0 )
		{
			if ( strncmp( buf, "MemTotal", 8 ) != 0 )
				continue;
			sscanf( buf, "%*s%ld", amp;&value );
			break;
		}
		fclose( fp );
		free( (void*)buf );
		if ( value != -1L )
			return (size_t)value * 1024L );
	}
</pre>

### Other

Every OS with a windowing interface has a control panel somewhere that shows the installed memory size. On Windows, see the "System" control panel. On OSX, select "About This Mac" from the Apple menu. On Solaris, select "About Oracle Solaris" from the "System" menu. For Ubuntu Linux, select the "Details" control panel. And so forth.

Every OS with a command line has commands to show the system configuration. On Windows, see the [`systeminfo`](http://technet.microsoft.com/en-us/library/cc771190(v=WS.10).aspx) command. On Linux, see [`free`](http://linux.die.net/man/1/free)` `and [`vmstat.`](http://linux.die.net/man/8/vmstat)     On BSD and OSX, use `[sysctl.](https://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man8/sysctl.8.html)` On OSX, use [`system_profiler`.](https://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man8/system_profiler.8.html) On Solaris, use [`prtconf.`](http://docs.oracle.com/cd/E23824_01/html/821-1462/prtconf-1m.html)  And so on.

## Downloads

* [getMemorySize.c](http://nadeausoftware.com/sites/NadeauSoftware.com/files/getMemorySize.c) provides the above C function. Compile it with any standard C compiler. The source is licensed under the [Creative Commons Attribution 3.0 Unported License.](http://creativecommons.org/licenses/by/3.0/deed.en_US)

## Further reading

### Related articles at NadeauSoftware.com

* [C/C++ tip: How to use compiler predefined macros to detect the operating system](http://nadeausoftware.com/articles/2012/01/c_c_tip_how_use_compiler_predefined_macros_detect_operating_system) explains how to use `#ifdef` macros for OS-specific code. A lot of these are used in the code above to detect Windows, OSX, Linux, BSD, etc.
* [C/C++ tip: How to get the process resident set size (physical memory use)](http://nadeausoftware.com/articles/2012/07/c_c_tip_how_get_process_resident_set_size_physical_memory_use) provides functions to get the amount of physical memory in use by a process.

### Web articles

* [Memory Limits for Windows Releases](http://msdn.microsoft.com/en-us/library/aa366778.aspx) at Microsoft.com lists the maximum memory sizes allowed by different Windows versions and their licenses.
* [Pushing the Limits of Windows:  Physical Memory](http://blogs.technet.com/b/markrussinovich/archive/2008/07/21/3092070.aspx) explains  Windows memory management and its various limits.

## Comments

### [Very helpful info!](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#comment-4424)

    Submitted by Anonymous (not verified) on September 26, 2012 - 6:38am.  

Very helpful info! Thanks!

But is sysctl() HW_REALMEM on FreeBSD really "Physical memory size in bytes (64-bit integer)"? Seems to me it is "unsigned long" (4 bytes on 32-bit FreeBSD, 8 bytes on 64-bit FreeBSD).

* [reply](http://nadeausoftware.com/comment/reply/114/4424)

### [Re:  Very helpful info!](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#comment-4599)

    Submitted by Dave_Nadeau on September 30, 2012 - 7:24pm.  

Thanks for catching a bug.  The proper return type for FreeBSD's 
<tt>HW_REALMEM</tt> is a 32-bit integer, not the 64-bit integer used in the original version of this article.

* [reply](http://nadeausoftware.com/comment/reply/114/4599)

### [Code for HP-UX](http://nadeausoftware.com/articles/2012/09/c_c_tip_how_get_physical_memory_size_system#comment-12788)

    Submitted by Anonymous (not verified) on October 31, 2012 - 9:25pm.  
    
    Following code will make the program work on HP-UX as well.

<pre style="code">
/* HP-UX. --------------------------------------------------- */
struct pst_static pst;

if (pstat_getstatic(&pst, sizeof(pst), (size_t) 1, 0) != -1)
	return (size_t)pst.physical_memory * (size_t)pst.page_size;
return 0L;
</pre>

* [reply](http://nadeausoftware.com/comment/reply/114/12788)

## 