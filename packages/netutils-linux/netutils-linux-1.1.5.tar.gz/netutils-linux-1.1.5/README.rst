netutils-linux
==============

.. image:: https://travis-ci.org/strizhechenko/netutils-linux.svg?branch=master
   :target: https://travis-ci.org/strizhechenko/netutils-linux

It's just a bunch of utils to simplify Linux network troubleshooting and performance tuning, developed in order to help `Carbon Reductor`_ techsupport and later automate the whole linux performance tuning process out of box.

.. _Carbon Reductor: http://www.carbonsoft.ru/products/carbon-reductor-5/
Project state
=============
Beta. Few script were gathered together, shortly documented, one has some tests and packed into python package.

Some were cleaned up, some - not. Most of them were being written in bash, not python, maybe they'll be ported later.

In next few weeks, it will receive something like a 'tuned' with autodetection of best settings for all the system feature.

Installation
============
.. code :: shell

  pip install netutils-linux

Utils
=====

irqtop
------
- Show you a rate of interrupts
- based on /proc/interrupts file
- Hides the interrupts with small rate to show a better picture.

Example output:

.. code::

  Total:    1398	1539
            CPU0    CPU1
  22:	    233	    227     IO-APIC-fasteoi	eth1
  28:	    91	    98      PCI-MSI-edge	eth0
  LOC:	    1021	1035	Local	timer	interrupts
  CAL:	    48	    172     Function	call	interrupts


softirq-net-rx-top
------------------
- Show you a rate of receiving packets
- Based on /proc/softirqs
- Sometimes shows much more CPUs than really exists

Example output:

.. code::

  11.22, 11.20, 7.90
  1	2897
  2	2552
  3	0
  4	0

  11.29, 11.21, 7.93
  1	2182
  2	2814
  3	0
  4	0

missed-pkts-monitor
-------------------
- Detects when were packets missed (maybe it will give some idea of correlation with something)
- Easy to use in tactical, not strategic debug, without deployment of graphite/influxdb
- Based on `ip -s -s link` output

link-rx-rate
------------
- Shows how many packets/bytes network interface receives
- Based on /proc/net/dev

Example output:

.. code::

  0 mbit/s 1576 pps
  0 mbit/s 1085 pps
  0 mbit/s 390 pps
  0 mbit/s 673 pps

rss-ladder
----------
Automatically set `smp_affinity_list` for IRQ of NIC rx/tx queues for ixgbe/igb/vmxnet3 drivers (they usually work on CPU0 out of the box).

Based on lscpu's output.

It also supports double/quad ladder in case of multiprocessor systems (but you better explicitly specify queue count == core per socket as NIC's driver's param).

.. code::

  # rss-ladder eth1 0
  - Распределение прерываний eth1 (-TxRx-) на сокете 0
    - eth1: irq 67 eth1-TxRx-0 -> 0
    - eth1: irq 68 eth1-TxRx-1 -> 1
    - eth1: irq 69 eth1-TxRx-2 -> 2
    - eth1: irq 70 eth1-TxRx-3 -> 3
    - eth1: irq 71 eth1-TxRx-4 -> 8
    - eth1: irq 72 eth1-TxRx-5 -> 9
    - eth1: irq 73 eth1-TxRx-6 -> 10
    - eth1: irq 74 eth1-TxRx-7 -> 11

autorps
-------
Enables RPS of NIC on all available CPUs. It may be good for small servers with cheap network cards or a bunch of VLAN.

Later, there will be a support for enabling RPS only for a subgroup of CPUs based on L3 caches.

maximize-cpu-freq
-----------------
Sets every CPU scaling governor mode to performance and set max scaling value for min scaling value. So you will be able to use all power of your processor (useful for latency sensible systems).

rx-buffers-increase
-------------------
rx-buffers-increase utils, that finds and sets compromise-value between avoiding dropped/missing pkts and keeping a latency low.

Example output:

.. code::

  # ethtool -g eth1

  Ring parameters for eth1:
  Pre-set maximums:
  RX:		4096
  RX Mini:	0
  RX Jumbo:	0
  TX:		4096
  Current hardware settings:
  RX:		256
  RX Mini:	0
  RX Jumbo:	0
  TX:		256

  # rx-buffers-increase eth1

  run: ethtool -G eth1 rx 2048

  # rx-buffers-increase eth1

  eth1's rx ring buffer already has fine size.

  # ethtool -g eth1

  Ring parameters for eth1:
  Pre-set maximums:
  RX:		4096
  RX Mini:	0
  RX Jumbo:	0
  TX:		4096
  Current hardware settings:
  RX:		2048
  RX Mini:	0
  RX Jumbo:	0
  TX:		256

server-info
-----------
Much alike lshw but designed for network processing role of server.

.. code::

  # server-info show
  cpu:
    info:
      Architecture: x86_64
      BogoMIPS: 6799.9899999999998
      Byte Order: Little Endian
      CPU MHz: 3399.998
      CPU family: 6
      CPU op-mode(s): 32-bit, 64-bit
      CPU(s): 2
      Core(s) per socket: 1
      Hypervisor vendor: KVM
      L1d cache: 32K
      L1i cache: 32K
      L2 cache: 4096K
      Model: 13
      Model name: QEMU Virtual CPU version (cpu64-rhel6)
      NUMA node(s): 1
      NUMA node0 CPU(s): 0,1
      On-line CPU(s) list: 0,1
      Socket(s): 2
      Stepping: 3
      Thread(s) per core: 1
      Vendor ID: GenuineIntel
      Virtualization type: full
    layout:
      '0': '0'
      '1': '1'
  disk:
    sr0:
      model: QEMU DVD-ROM
    vda:
      model: null
      size: 64424509440
      type: HDD
  memory:
    MemFree: 158932
    MemTotal: 1922096
    SwapFree: 4128764
    SwapTotal: 4128764
  net:
    eth1:
      buffers:
        cur: 2048
        max: 4096
      conf:
        ip: 10.144.63.1/24
        vlan: true
      driver:
        driver: e1000
        version: 7.3.21-k8-NAPI
      queues:
        own: []
        rx: []
        rxtx: []
        shared:
        - virtio1, eth0, eth1
        tx: []
        unknown: []

It also can rate hardware and its features in range of 1..10.

.. code::

  # server-info rate
  cpu:
    BogoMIPS: 7
    CPU MHz: 7
    CPU(s): 1
    Core(s) per socket: 1
    L3 cache: 1
    Socket(s): 10
    Thread(s) per core: 10
    Vendor ID: 10
   disk:
     sr0:
       size: 1
       type: 2
     vda:
       size: 1
       type: 1
   memory:
     MemTotal: 1
     SwapTotal: 10
   net:
     eth1:
       buffers:
         cur: 5
         max: 10
       driver: 1
       queues: 1
   system:
     Hypervisor vendor: 1
     Virtualization type: 1
