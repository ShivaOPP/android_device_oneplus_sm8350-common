/*
 * This file is auto-generated. Modifications will be lost.
 *
 * See https://android.googlesource.com/platform/bionic/+/master/libc/kernel/
 * for more information.
 */
#ifndef UAPI_UFS_IOCTL_H_
#define UAPI_UFS_IOCTL_H_
#ifdef OPLUS_FEATURE_UFSPLUS
#include <linux/types.h>
#define UFS_IOCTL_QUERY 0x5388
#define UFSFEATURE_QUERY_OPCODE 0x5500
struct ufs_ioctl_query_data {
  __u32 opcode;
  __u8 idn;
  __u16 buf_size;
  __u8 buffer[0];
};
#endif
#endif
