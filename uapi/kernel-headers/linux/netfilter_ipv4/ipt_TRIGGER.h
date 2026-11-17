/*
 * This file is auto-generated. Modifications will be lost.
 *
 * See https://android.googlesource.com/platform/bionic/+/master/libc/kernel/
 * for more information.
 */
#include <linux/types.h>
#ifndef _IPT_PORTTRIGGER_H_target
#define _IPT_PORTTRIGGER_H_target
#define TRIGGER_TIMEOUT 600
#define IPT_MULTI_PORTS 15
enum porttrigger_mode {
  MODE_TRIGGER_DNAT,
  MODE_TRIGGER_FORWARD_IN,
  MODE_TRIGGER_FORWARD_OUT
};
struct ipt_mport {
  unsigned short pflags;
  unsigned short ports[IPT_MULTI_PORTS];
};
struct ipt_porttrigger_info {
  enum porttrigger_mode mode;
  unsigned short trigger_proto;
  unsigned short forward_proto;
  unsigned int timer;
  struct ipt_mport trigger_ports;
  struct ipt_mport forward_ports;
};
#endif
