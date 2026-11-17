/*
 * This file is auto-generated. Modifications will be lost.
 *
 * See https://android.googlesource.com/platform/bionic/+/master/libc/kernel/
 * for more information.
 */
#ifndef _MIC_IOCTL_H_
#define _MIC_IOCTL_H_
#include <linux/types.h>
struct mic_copy_desc {
  struct iovec * iov;
  __u32 iovcnt;
  __u8 vr_idx;
  __u8 update_used;
  __u32 out_len;
};
#define MIC_VIRTIO_ADD_DEVICE _IOWR('s', 1, struct mic_device_desc *)
#define MIC_VIRTIO_COPY_DESC _IOWR('s', 2, struct mic_copy_desc *)
#define MIC_VIRTIO_CONFIG_CHANGE _IOWR('s', 5, __u8 *)
#endif
