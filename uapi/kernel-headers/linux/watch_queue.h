/*
 * This file is auto-generated. Modifications will be lost.
 *
 * See https://android.googlesource.com/platform/bionic/+/master/libc/kernel/
 * for more information.
 */
#ifndef _LINUX_WATCH_QUEUE_H
#define _LINUX_WATCH_QUEUE_H
#include <linux/types.h>
enum watch_notification_type {
  WATCH_TYPE_META = 0,
  WATCH_TYPE__NR = 1
};
enum watch_meta_notification_subtype {
  WATCH_META_REMOVAL_NOTIFICATION = 0,
  WATCH_META_LOSS_NOTIFICATION = 1,
};
struct watch_notification {
  __u32 type : 24;
  __u32 subtype : 8;
  __u32 info;
#define WATCH_INFO_LENGTH 0x0000007f
#define WATCH_INFO_LENGTH__SHIFT 0
#define WATCH_INFO_ID 0x0000ff00
#define WATCH_INFO_ID__SHIFT 8
#define WATCH_INFO_TYPE_INFO 0xffff0000
#define WATCH_INFO_TYPE_INFO__SHIFT 16
#define WATCH_INFO_FLAG_0 0x00010000
#define WATCH_INFO_FLAG_1 0x00020000
#define WATCH_INFO_FLAG_2 0x00040000
#define WATCH_INFO_FLAG_3 0x00080000
#define WATCH_INFO_FLAG_4 0x00100000
#define WATCH_INFO_FLAG_5 0x00200000
#define WATCH_INFO_FLAG_6 0x00400000
#define WATCH_INFO_FLAG_7 0x00800000
};
struct watch_notification_removal {
  struct watch_notification watch;
  __u64 id;
};
#endif
