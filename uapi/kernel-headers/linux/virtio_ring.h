/*
 * This file is auto-generated. Modifications will be lost.
 *
 * See https://android.googlesource.com/platform/bionic/+/master/libc/kernel/
 * for more information.
 */
#ifndef _LINUX_VIRTIO_RING_H
#define _LINUX_VIRTIO_RING_H
#include <stdint.h>
#include <linux/types.h>
#include <linux/virtio_types.h>
#define VRING_DESC_F_NEXT 1
#define VRING_DESC_F_WRITE 2
#define VRING_DESC_F_INDIRECT 4
#define VRING_PACKED_DESC_F_AVAIL 7
#define VRING_PACKED_DESC_F_USED 15
#define VRING_USED_F_NO_NOTIFY 1
#define VRING_AVAIL_F_NO_INTERRUPT 1
#define VRING_PACKED_EVENT_FLAG_ENABLE 0x0
#define VRING_PACKED_EVENT_FLAG_DISABLE 0x1
#define VRING_PACKED_EVENT_FLAG_DESC 0x2
#define VRING_PACKED_EVENT_F_WRAP_CTR 15
#define VIRTIO_RING_F_INDIRECT_DESC 28
#define VIRTIO_RING_F_EVENT_IDX 29
struct vring_desc {
  __virtio64 addr;
  __virtio32 len;
  __virtio16 flags;
  __virtio16 next;
};
struct vring_avail {
  __virtio16 flags;
  __virtio16 idx;
  __virtio16 ring[];
};
struct vring_used_elem {
  __virtio32 id;
  __virtio32 len;
};
struct vring_used {
  __virtio16 flags;
  __virtio16 idx;
  struct vring_used_elem ring[];
};
struct vring {
  unsigned int num;
  struct vring_desc * desc;
  struct vring_avail * avail;
  struct vring_used * used;
};
#define VRING_AVAIL_ALIGN_SIZE 2
#define VRING_USED_ALIGN_SIZE 4
#define VRING_DESC_ALIGN_SIZE 16
#define vring_used_event(vr) ((vr)->avail->ring[(vr)->num])
#define vring_avail_event(vr) (* (__virtio16 *) & (vr)->used->ring[(vr)->num])
struct vring_packed_desc_event {
  __le16 off_wrap;
  __le16 flags;
};
struct vring_packed_desc {
  __le64 addr;
  __le32 len;
  __le16 id;
  __le16 flags;
};
#endif
