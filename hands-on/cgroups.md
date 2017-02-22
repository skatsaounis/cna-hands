# Cgroups

Create a "red" control group, making all the tunables of the `memory`,`cpu`,
`cpuset` controllers writable by nanastop

```
sudo cgcreate -a nanastop -g cpu,cpuset:red
sudo cgcreate -a nanastop -g cpu,cpuset:blue
```

```
ls -l /sys/fs/cgroup/cpu/red
[nanastop@nanastop-vm:~ ->0]$ ls -l /sys/fs/cgroup/cpu/red
total 0
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cgroup.clone_children
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cgroup.procs
-r--r--r-- 1 nanastop root 0 Feb 22 11:40 cpuacct.stat
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cpuacct.usage
-r--r--r-- 1 nanastop root 0 Feb 22 11:40 cpuacct.usage_percpu
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cpu.cfs_period_us
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cpu.cfs_quota_us
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cpu.shares
-r--r--r-- 1 nanastop root 0 Feb 22 11:40 cpu.stat
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 notify_on_release
-rw-r--r-- 1 root     root 0 Feb 22 11:40 tasks
[nanastop@nanastop-vm:~ ->0]$ ls -l /sys/fs/cgroup/cpuset/red
total 0
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cgroup.clone_children
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cgroup.procs
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cpuset.cpu_exclusive
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cpuset.cpus
-r--r--r-- 1 nanastop root 0 Feb 22 11:40 cpuset.effective_cpus
-r--r--r-- 1 nanastop root 0 Feb 22 11:40 cpuset.effective_mems
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cpuset.mem_exclusive
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cpuset.mem_hardwall
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cpuset.memory_migrate
-r--r--r-- 1 nanastop root 0 Feb 22 11:40 cpuset.memory_pressure
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cpuset.memory_spread_page
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cpuset.memory_spread_slab
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cpuset.mems
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cpuset.sched_load_balance
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 cpuset.sched_relax_domain_level
-rw-r--r-- 1 nanastop root 0 Feb 22 11:40 notify_on_release
-rw-r--r-- 1 root     root 0 Feb 22 11:40 tasks
```

```
sudo cgdelete -g cpu,cpuset:blue
sudo cgdelete -g cpu,cpuset:read
```

```
[nanastop@nanastop-vm:~ ->1]$ cat /sys/fs/cgroup/cpu/red/cpu.shares 
1024
[nanastop@nanastop-vm:~ ->0]$ cat /sys/fs/cgroup/cpu/blue/cpu.shares 
1024
```

```
echo 10000000 > /sys/fs/cgroup/memory/red/memory.kmem.limit_in_bytes
```

```
[nanastop@nanastop-vm:~ ->0]$ echo 0 > /sys/fs/cgroup/cpuset/red/cpuset.cpus 
[nanastop@nanastop-vm:~ ->0]$ echo 0 > /sys/fs/cgroup/cpuset/red/cpuset.mems 
[nanastop@nanastop-vm:~ ->0]$ echo 0 > /sys/fs/cgroup/cpuset/blue/cpuset.mems 
[nanastop@nanastop-vm:~ ->0]$ echo 0 > /sys/fs/cgroup/cpuset/blue/cpuset.cpus
```

```
dd if=/dev/zero of=/dev/null &
dd if=/dev/zero of=/dev/null &
```

```
ps aux|grep dd
```

```
sudo cgclassify -g cpu,cpuset:red 5045
sudo cgclassify -g cpu,cpuset:blue 5092
```


```
echo 768 > /sys/fs/cgroup/cpu/red/cpu.shares 
echo 256 > /sys/fs/cgroup/cpu/blue/cpu.shares 
```

