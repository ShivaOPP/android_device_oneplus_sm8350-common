/*
 * This file is auto-generated. Modifications will be lost.
 *
 * See https://android.googlesource.com/platform/bionic/+/master/libc/kernel/
 * for more information.
 */
#ifndef _LINUX_ELFCORE_H
#define _LINUX_ELFCORE_H
#include <linux/types.h>
#include <linux/signal.h>
#include <linux/time.h>
#include <linux/ptrace.h>
#include <linux/elf.h>
#include <linux/fs.h>
struct elf_siginfo {
  int si_signo;
  int si_code;
  int si_errno;
};
typedef elf_greg_t greg_t;
typedef elf_gregset_t gregset_t;
typedef elf_fpregset_t fpregset_t;
typedef elf_fpxregset_t fpxregset_t;
#define NGREG ELF_NGREG
struct elf_prstatus {
  struct elf_siginfo pr_info;
  short pr_cursig;
  unsigned long pr_sigpend;
  unsigned long pr_sighold;
  pid_t pr_pid;
  pid_t pr_ppid;
  pid_t pr_pgrp;
  pid_t pr_sid;
  struct timeval pr_utime;
  struct timeval pr_stime;
  struct timeval pr_cutime;
  struct timeval pr_cstime;
  elf_gregset_t pr_reg;
  int pr_fpvalid;
};
#define ELF_PRARGSZ (80)
struct elf_prpsinfo {
  char pr_state;
  char pr_sname;
  char pr_zomb;
  char pr_nice;
  unsigned long pr_flag;
  __kernel_uid_t pr_uid;
  __kernel_gid_t pr_gid;
  pid_t pr_pid, pr_ppid, pr_pgrp, pr_sid;
  char pr_fname[16];
  char pr_psargs[ELF_PRARGSZ];
};
typedef struct elf_prstatus prstatus_t;
typedef struct elf_prpsinfo prpsinfo_t;
#define PRARGSZ ELF_PRARGSZ
#endif
