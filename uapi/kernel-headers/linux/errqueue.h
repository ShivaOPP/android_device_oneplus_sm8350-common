/*
 * This file is auto-generated. Modifications will be lost.
 *
 * See https://android.googlesource.com/platform/bionic/+/master/libc/kernel/
 * for more information.
 */
#ifndef _LINUX_ERRQUEUE_H
#define _LINUX_ERRQUEUE_H
#include <linux/types.h>
#include <linux/time_types.h>
struct sock_extended_err {
  __u32 ee_errno;
  __u8 ee_origin;
  __u8 ee_type;
  __u8 ee_code;
  __u8 ee_pad;
  __u32 ee_info;
  __u32 ee_data;
};
#define SO_EE_ORIGIN_NONE 0
#define SO_EE_ORIGIN_LOCAL 1
#define SO_EE_ORIGIN_ICMP 2
#define SO_EE_ORIGIN_ICMP6 3
#define SO_EE_ORIGIN_TXSTATUS 4
#define SO_EE_ORIGIN_ZEROCOPY 5
#define SO_EE_ORIGIN_TXTIME 6
#define SO_EE_ORIGIN_TIMESTAMPING SO_EE_ORIGIN_TXSTATUS
#define SO_EE_OFFENDER(ee) ((struct sockaddr *) ((ee) + 1))
#define SO_EE_CODE_ZEROCOPY_COPIED 1
#define SO_EE_CODE_TXTIME_INVALID_PARAM 1
#define SO_EE_CODE_TXTIME_MISSED 2
struct scm_timestamping {
  struct timespec ts[3];
};
struct scm_timestamping64 {
  struct __kernel_timespec ts[3];
};
enum {
  SCM_TSTAMP_SND,
  SCM_TSTAMP_SCHED,
  SCM_TSTAMP_ACK,
};
#endif
