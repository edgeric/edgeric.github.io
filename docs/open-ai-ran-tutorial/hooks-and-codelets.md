# Hooks and Codelets

Every demo in this tutorial runs on codelets: small eBPF programs that you load into the running gNB
at a hook, and unload again, with no rebuild and no restart. This page shows how to add a hook to the
gNB, then how to write, build and load your own codelets. It walks through two examples from the
repository: a telemetry codelet that reports each UE's downlink traffic, and the control codelet behind
Demo 3's buffer caps.

## How the Pieces Fit

- A **hook** is a call in the gNB's source where codelets can run. With no codelet loaded, the call
  does nothing.
- A **monitor hook** gives the codelet a read-only context, such as the UE, the bearer and a packet
  size. The codelet measures and sends results on an **output channel**. An xApp in `jrtc-0` receives
  them.
- A **control hook** gives the codelet a struct that the gNB reads back after the call. What the codelet
  writes there, the gNB applies. An xApp can send it settings on an **input channel**.
- jbpf's verifier checks every codelet, so a codelet cannot crash the gNB or loop forever.

| What | Where |
|---|---|
| hook declarations | `ocudu-jbpf/srsran_jbpf/verifier/specs/jbpf_srsran_hooks.h` |
| hook contexts | `ocudu-jbpf/include/srsran/jbpf/jbpf_srsran_contexts.h` |
| codelets | `jrtc-apps/codelets/<name>/`: source, messages, `Makefile`, codeletset YAML |
| xApps | `jrtc-apps/jrtc_apps/<name>/`: Python app and deployment YAML |

[Miscellaneous](miscellaneous.md#hooks-used-in-this-tutorial) lists the hooks this tutorial uses.

## Add a Hook to the gNB

Skip this part if an existing hook already fires where you need it. The steps below are the ones that
added `rlc_dl_ctrl`, the control hook of Example 2. It fires for every downlink SDU on an RLC AM data
bearer, before the gNB decides whether the SDU fits in the queue.

**1. Define the context** in `include/srsran/jbpf/jbpf_srsran_contexts.h`. For a control hook, say which
fields the codelet writes:

```c
struct jbpf_rlc_ctrl_info {
    uint16_t du_ue_index;
    uint8_t  is_srb;   /* always 0 (kept for layout compatibility) */
    uint8_t  rb_id;    /* DRB id */
    uint32_t cur_byte_limit;   /* srsRAN -> codelet: the queue's current byte limit */
    uint32_t new_byte_limit;   /* codelet -> srsRAN: desired byte limit (0 = leave unchanged) */
    uint32_t cur_sdu_limit;    /* srsRAN -> codelet: the queue's current SDU-count limit */
    uint32_t new_sdu_limit;    /* codelet -> srsRAN: desired SDU-count limit (0 = leave unchanged) */
    uint32_t cfg_byte_limit;   /* srsRAN -> codelet: CONFIGURED byte limit (queue-bytes); write it back to reset */
    uint32_t cfg_sdu_limit;    /* srsRAN -> codelet: CONFIGURED SDU limit (queue-size = queue capacity) */
};
```

**2. Declare the hook** in `srsran_jbpf/verifier/specs/jbpf_srsran_hooks.h`. `HOOK_ASSIGN` points the
generic context the codelet receives at your struct:

```c
DECLARE_JBPF_HOOK(rlc_dl_ctrl,
    struct jbpf_ran_generic_ctx ctx,
    ctx,
    HOOK_PROTO(
        struct jbpf_rlc_ctrl_info *info),
    HOOK_ASSIGN(
        ctx.data = (uint64_t)info;
        ctx.data_end = (uint64_t) ((uint8_t*)info + sizeof(struct jbpf_rlc_ctrl_info));
    )
)
```

A hook can also pass a few numbers in `srs_meta_data1` to `srs_meta_data4`. The monitor hook
`rlc_dl_new_sdu`, used in Example 1, packs the SDU length and PDCP sequence number this way:
`ctx.srs_meta_data1 = (uint64_t)sdu_length << 32 | pdcp_sn;`.

**3. Define and call the hook** in the source file where it fires. `DEFINE_JBPF_CTRL_HOOK` creates a
control hook and `DEFINE_JBPF_HOOK` a monitor hook. Keep the code inside `#ifdef JBPF_ENABLED`. From
`lib/rlc/rlc_tx_am_entity.cpp`, trimmed:

```cpp
DEFINE_JBPF_CTRL_HOOK(rlc_dl_ctrl);

void rlc_tx_am_entity::handle_jbpf_rlc_ctrl()
{
  struct jbpf_rlc_ctrl_info ci = {0};
  ci.du_ue_index    = ue_index;
  ci.is_srb         = 0;
  ci.rb_id          = drb_id_to_uint(rb_id.get_drb_id());
  ci.cur_byte_limit = sdu_queue.get_byte_limit();
  ci.cur_sdu_limit  = sdu_queue.get_sdu_limit();
  ci.cfg_byte_limit = sdu_queue.get_cfg_byte_limit();
  ci.cfg_sdu_limit  = sdu_queue.get_capacity();
  hook_rlc_dl_ctrl(&ci);

  if (ci.new_byte_limit != 0) {
    uint32_t old_limit = sdu_queue.get_byte_limit();
    uint32_t new_limit = sdu_queue.clamp_byte_limit(ci.new_byte_limit);
    if (new_limit != old_limit) {
      sdu_queue.set_byte_limit(new_limit);
    }
  }
  // ... the same for new_sdu_limit
}

void rlc_tx_am_entity::handle_sdu(byte_buffer sdu_buf, bool is_retx)
{
  ...
#ifdef JBPF_ENABLED
  if (not rb_id.is_srb()) {
    handle_jbpf_rlc_ctrl();
  }
#endif
  ...
```

The gNB clamps the requested limit before it applies it, so a codelet cannot shrink a queue below one
maximum-size PDCP PDU or grow it past the configured size.

**4. Rebuild the gNB image** and put it in the pod, as in Part 1 and Part 2 of the
[tutorial](../open-ai-ran-tutorial.md):

```bash
cd ~/open-ai-ran-tutorial
docker build -t ocudu-gnb-jbpf:ipc -f ocudu-jbpf/docker/Dockerfile ocudu-jbpf
k3d image import ocudu-gnb-jbpf:ipc -c "$CLUSTER"
# then recreate the gNB pod with its containers (Part 2)
```

Codelets compile against the jbpf SDK image, and its headers do not have the hooks added here. A
codelet for a new hook therefore keeps its own copy of the context struct, field for field. Example 2
does this.

## Example 1: A Telemetry Codelet

`dl_sdu_count` runs on the `rlc_dl_new_sdu` monitor hook, which fires for every downlink SDU that enters
RLC. It counts SDUs and bytes per UE and, about once a second, sends one message per active UE. An xApp
prints them.

The files:

```text
jrtc-apps/codelets/dl_sdu_count/      dl_sdu_count.proto  dl_sdu_count.cpp  Makefile  dl_sdu_count.yaml
jrtc-apps/jrtc_apps/dl_sdu_count/     dl_sdu_count_app.py  deployment.yaml
```

### The message

`dl_sdu_count.proto` defines what the codelet sends. The build turns it into a C struct for the codelet,
a serializer for the gNB and a Python class for the xApp.

```proto
syntax = "proto2";

// One message per UE per period: the downlink SDUs and bytes that entered RLC.
message dl_sdu_count {
  required uint64 timestamp = 1;
  required uint32 du_ue_index = 2;
  required uint32 sdus = 3;
  required uint64 bytes = 4;
}
```

### The codelet

`dl_sdu_count.cpp`:

```cpp
// dl_sdu_count: count the downlink SDUs and bytes that enter RLC, per UE, and report them
// once per period (2^30 ns, about 1.07 s).
// Hook: rlc_dl_new_sdu (monitor). ctx->data is a jbpf_rlc_ctx_info, and the hook packs
// sdu_length << 32 | pdcp_sn into srs_meta_data1.

#include <linux/bpf.h>

#include "jbpf_srsran_contexts.h"
#include "dl_sdu_count.pb.h"

#include "../utils/misc_utils.h"   // JBPF_CODELET_SUCCESS, JBPF_CODELET_FAILURE

#define SEC(NAME) __attribute__((section(NAME), used))

#include "jbpf_defs.h"
#include "jbpf_helper.h"

#define MAX_UE       16
#define PERIOD_SHIFT 30

struct ue_count {
    uint64_t period;   // the period these counts belong to
    uint64_t bytes;
    uint32_t sdus;
};

// Per-UE counters, indexed by du_ue_index.
struct jbpf_load_map_def SEC("maps") counts = {
    .type        = JBPF_MAP_TYPE_ARRAY,
    .key_size    = sizeof(uint32_t),
    .value_size  = sizeof(struct ue_count),
    .max_entries = MAX_UE,
};

// Output channel to the xApp, one dl_sdu_count message per entry.
jbpf_ringbuf_map(out_counts, dl_sdu_count, 64);

extern "C" SEC("jbpf_srsran_generic")
uint64_t jbpf_main(void* state)
{
    struct jbpf_ran_generic_ctx* ctx = (struct jbpf_ran_generic_ctx*)state;
    const struct jbpf_rlc_ctx_info* rlc = (const struct jbpf_rlc_ctx_info*)ctx->data;

    // The verifier rejects any read of ctx->data without this check.
    if ((const uint8_t*)rlc + sizeof(*rlc) > (const uint8_t*)ctx->data_end) {
        return JBPF_CODELET_FAILURE;
    }
    // Count data bearers only.
    if (rlc->is_srb) {
        return JBPF_CODELET_SUCCESS;
    }

    uint32_t ue = rlc->du_ue_index % MAX_UE;
    struct ue_count* c = (struct ue_count*)jbpf_map_lookup_elem(&counts, &ue);
    if (!c) {
        return JBPF_CODELET_FAILURE;
    }

    // This UE's first SDU in a new period: send the last period's counts, then start over.
    uint64_t period = jbpf_time_get_ns() >> PERIOD_SHIFT;
    if (c->period != period) {
        if (c->sdus > 0) {
            dl_sdu_count msg = {};
            msg.timestamp   = period << PERIOD_SHIFT;
            msg.du_ue_index = ue;
            msg.sdus        = c->sdus;
            msg.bytes       = c->bytes;
            jbpf_ringbuf_output(&out_counts, &msg, sizeof(msg));
        }
        c->period = period;
        c->sdus   = 0;
        c->bytes  = 0;
    }

    c->sdus += 1;
    c->bytes += ctx->srs_meta_data1 >> 32;
    return JBPF_CODELET_SUCCESS;
}
```

Codelets keep their state in maps. `counts` holds each UE's totals and the period they belong to. A
UE's counts go out with its first SDU of the next period, so a UE without traffic stays quiet.
`out_counts` is the output channel, holding up to 64 messages on their way to the xApp.

### What the verifier checks

The verifier rejects a codelet that it cannot prove safe. The rules you will meet first:

- Check `ctx->data` against `ctx->data_end` before reading the context.
- Bound every loop. `#pragma unroll` over a constant count works.
- Avoid 64-bit division; shift instead, as `PERIOD_SHIFT` does.
- Avoid `static const` tables. The loader cannot place them, and the verifier then reports
  0 instructions. Use a `switch` that returns the value.
- Send one message per call. When a codelet sent several in one call, only the first reached the
  xApp.
- After editing a header, delete the directory's `.o` files: `make` does not track headers.

### Build

The `Makefile` lists each message as `<proto file>^<message>`:

```make
PROTO_AND_SCHEMA := \
	dl_sdu_count^dl_sdu_count

include ../Makefile.defs
include ../Makefile.common
```

```bash
cd ~/open-ai-ran-tutorial/jrtc-apps/codelets
./make.sh -d dl_sdu_count
```

The build runs in the jbpf SDK container and ends with the verifier's result:

```text
Building dl_sdu_count
--------- dl_sdu_count.cpp ----------------------------------------------
Program terminates within 115 instructions
```

### The codeletset

`dl_sdu_count.yaml` attaches the codelet to its hook and names its output channel and message:

```yaml
codeletset_id: dl_sdu_count

codelet_descriptor:
  - codelet_name: dl_sdu_count
    codelet_path: ${JBPF_CODELETS}/dl_sdu_count/dl_sdu_count.o
    hook_name: rlc_dl_new_sdu
    priority: 1
    out_io_channel:
      - name: out_counts
        forward_destination: DestinationNone
        serde:
          file_path: ${JBPF_CODELETS}/dl_sdu_count/dl_sdu_count:dl_sdu_count_serializer.so
          protobuf:
            package_path: ${JBPF_CODELETS}/dl_sdu_count/dl_sdu_count.pb
            msg_name: dl_sdu_count
```

### The xApp

`dl_sdu_count_app.py` subscribes to the output channel and prints each message. The stream name is
`<deployment>://jbpf_agent/<codeletset>/<codelet>`.

```python
# dl_sdu_count_app: print the per-UE downlink SDU counts that the dl_sdu_count codelet sends.

import ctypes
import os
import sys
from dataclasses import dataclass

sys.path.append(os.environ["JRTC_APP_PATH"])
from jrtc_app import *

from dl_sdu_count import struct__dl_sdu_count  # generated from dl_sdu_count.proto

PERIOD_S = (1 << 30) / 1e9  # the codelet's report period


@dataclass
class AppState:
    app: JrtcApp


def app_handler(timeout: bool, stream_idx: int, data_entry: struct_jrtc_router_data_entry, state: AppState):
    if timeout:
        return
    msg = ctypes.cast(data_entry.data, ctypes.POINTER(struct__dl_sdu_count)).contents
    mbps = msg.bytes * 8 / PERIOD_S / 1e6
    print(f"[dl_sdu_count] ue {msg.du_ue_index}: {msg.sdus} SDUs, {mbps:.1f} Mbit/s", flush=True)


def jrtc_start_app(capsule):
    streams = [
        JrtcStreamCfg_t(
            JrtcStreamIdCfg_t(
                JRTC_ROUTER_REQ_DEST_ANY,
                JRTC_ROUTER_REQ_DEVICE_ID_ANY,
                b"dl_sdu_count://jbpf_agent/dl_sdu_count/dl_sdu_count",  # deployment://jbpf_agent/codeletset/codelet
                b"out_counts"),                                          # the codelet's output channel
            True,   # receive
            None)
    ]
    cfg = JrtcAppCfg_t(
        b"dl_sdu_count",                              # context
        100,                                          # queue size
        len(streams),
        (JrtcStreamCfg_t * len(streams))(*streams),
        10.0,                                         # initialization timeout, s
        0.25,                                         # sleep timeout, s
        2.0)                                          # inactivity timeout, s
    state = AppState(app=None)
    state.app = jrtc_app_create(capsule, cfg, app_handler, state)
    jrtc_app_run(state.app)
    jrtc_app_destroy(state.app)
```

`deployment.yaml` loads the xApp and the codeletset together:

```yaml
name: dl_sdu_count

decoder:
  - type: decodergrpc
    host: jrtc-decoder.ran.svc.cluster.local
    port: 20789

app:
  - name: dl_sdu_count_app
    path: ${JRTC_APPS}/dl_sdu_count/dl_sdu_count_app.py
    type: python
    host: jrtc-service.ran.svc.cluster.local
    port: 3001
    modules:
      - ${JBPF_CODELETS}/dl_sdu_count/dl_sdu_count.py

jbpf:
  device:
    - id: 1
      host: srs-gnb-du1-proxy.ran.svc.cluster.local
      port: 30450
  codelet_set:
    - device: 1
      config: ${JBPF_CODELETS}/dl_sdu_count/dl_sdu_count.yaml
```

### Run it

Bring the RAN up with `--telemetry`, which starts the forwarder that `jrtc-ctl` needs, and start
traffic (Part 2). Then copy the codelet directory into the gNB container, where the gNB's jbpf agent
loads the serializer from, and load the deployment. `jrtc-0` reads the codelets and xApps from your
clone.

```bash
cd ~/open-ai-ran-tutorial
JRTC() { kubectl exec -n ran jrtc-0 -c jrtc -- bash -c \
  "export JRTC_APPS=/apps JBPF_CODELETS=/codelets; /jrtc/out/bin/jrtc-ctl $*"; }

kubectl cp jrtc-apps/codelets/dl_sdu_count ran/srs-gnb-du1-0:/codelets/ -c ocudujbpf
JRTC 'load -c /apps/dl_sdu_count/deployment.yaml'
kubectl logs -n ran jrtc-0 -c jrtc -f | grep dl_sdu_count
```

The gNB log shows `Registered codelet dl_sdu_count to hook rlc_dl_new_sdu`, and the xApp prints one line
per UE about once a second. With two UEs downloading at about 30 Mbit/s each:

```text
[dl_sdu_count] ue 1: 2788 SDUs, 31.2 Mbit/s
[dl_sdu_count] ue 0: 2773 SDUs, 31.1 Mbit/s
[dl_sdu_count] ue 0: 2742 SDUs, 30.7 Mbit/s
[dl_sdu_count] ue 1: 2766 SDUs, 31.0 Mbit/s
```

The counts include RLC retransmissions, so they read a little above the goodput the UEs measure.

Unload it with the same file:

```bash
JRTC 'unload -c /apps/dl_sdu_count/deployment.yaml'
```

To chart the counts in Grafana, have the xApp write them to VictoriaMetrics, as
`jrtc_apps/upt/upt_app.py` does in its `_emit` function.

## Example 2: A Control Codelet

`bufcap` is the codelet behind Demo 3's buffer caps. It runs on the `rlc_dl_ctrl` control hook and sets
the same byte limit on every UE's data bearers, so the RLC queue drops packets once it holds that many
bytes. It needs no xApp: the limit is built in.

```text
jrtc-apps/codelets/bufcap/                 bufcap.cpp  Makefile
buffer-control-experiments/bufcap.sh       builds, loads and unloads it
```

### The codelet

`bufcap.cpp` copies the hook's context struct from the gNB, then writes the limit on each call:

```cpp
// Copyright (c) Microsoft Corporation. Licensed under the MIT license.
//
// bufcap - fixed RLC DL buffer cap, for Demo 3 of the tutorial.
//
// HOOK: rlc_dl_ctrl (control hook in rlc_tx_am_entity::handle_sdu). Fires once per DL SDU
// on each RLC AM DRB, before the enqueue/tail-drop decision.
//
// One source, built once per cap: -DCAP_BYTES=<bytes>. While loaded it asserts that byte
// limit on every DRB of every UE, so the queue tail-drops once it holds CAP_BYTES.
//
// CAP_BYTES=0 builds "bufcap_off": it writes the bearer's CONFIGURED limits back
// (cfg_* from the hook context). The gNB keeps the last limit after a codelet is
// unloaded, so bufcap.sh loads bufcap_off for a moment to undo a cap.
//
// The gNB clamps the byte limit to [one max PDCP PDU (~9 kB), configured queue-bytes].

#include <linux/bpf.h>
#include <string.h>

#include "jbpf_srsran_contexts.h"

#include "../utils/misc_utils.h"

#define SEC(NAME) __attribute__((section(NAME), used))

#include "jbpf_defs.h"
#include "jbpf_helper.h"

#ifndef CAP_BYTES
#define CAP_BYTES (65536)
#endif

// Layout MUST MATCH struct jbpf_rlc_ctrl_info in
// ocudu-jbpf/include/srsran/jbpf/jbpf_srsran_contexts.h (see bufctl/rlc_ctrl.cpp).
struct jbpf_rlc_ctrl_info {
    uint16_t du_ue_index;
    uint8_t  is_srb;           // always 0: the hook only fires for DRBs
    uint8_t  rb_id;            // DRB id
    uint32_t cur_byte_limit;   // gNB -> codelet
    uint32_t new_byte_limit;   // codelet -> gNB (0 = leave unchanged)
    uint32_t cur_sdu_limit;    // gNB -> codelet
    uint32_t new_sdu_limit;    // codelet -> gNB (0 = leave unchanged)
    uint32_t cfg_byte_limit;   // gNB -> codelet: configured byte limit
    uint32_t cfg_sdu_limit;    // gNB -> codelet: configured SDU limit
};

extern "C" SEC("jbpf_srsran_generic")
uint64_t jbpf_main(void* state)
{
    struct jbpf_ran_generic_ctx* ctx = (jbpf_ran_generic_ctx*)state;

    struct jbpf_rlc_ctrl_info* ci = (struct jbpf_rlc_ctrl_info*)ctx->data;
    if (reinterpret_cast<uint8_t*>(ci) + sizeof(struct jbpf_rlc_ctrl_info) >
        reinterpret_cast<uint8_t*>(ctx->data_end)) {
        return JBPF_CODELET_FAILURE;
    }
    if (ci->is_srb) {
        return JBPF_CODELET_SUCCESS;
    }
#if CAP_BYTES == 0
    ci->new_byte_limit = ci->cfg_byte_limit;
    ci->new_sdu_limit  = ci->cfg_sdu_limit;
#else
    ci->new_byte_limit = CAP_BYTES;
#endif
    return JBPF_CODELET_SUCCESS;
}
```

### Build

Each limit is its own object. The `Makefile`'s `one` target compiles `bufcap.cpp` with
`-DCAP_BYTES=<bytes>` and runs the verifier on the result:

```make
one:
	@echo "--------- bufcap.cpp -> bufcap_$(NAME).o (CAP_BYTES=$(CAP)) ---------"
	@$(CXX) $(CXXFLAGS) -DCAP_BYTES=$(CAP) $(INC) -c bufcap.cpp -o bufcap_$(NAME).o
	@$(VERIFIER_BIN) bufcap_$(NAME).o >/dev/null 2>&1 \
		&& echo "verifier: OK" \
		|| { echo "verifier: FAILED -- the gNB would reject bufcap_$(NAME).o"; rm -f bufcap_$(NAME).o; exit 1; }
```

`bufcap.sh build` runs that target in the jbpf SDK container, then writes the codeletset and the
deployment for each size:

```bash
cd ~/open-ai-ran-tutorial
bash buffer-control-experiments/bufcap.sh build 64k
```

```text
  --------- bufcap.cpp -> bufcap_64k.o (CAP_BYTES=65536) ---------
  verifier: OK
  built bufcap_64k (65536 bytes)
```

`jrtc-apps/codelets/bufcap/bufcap_64k.yaml` attaches the object to the hook:

```yaml
# generated by buffer-control-experiments/bufcap.sh -- fixed RLC DL buffer cap (64k = 65536 bytes; 0 = restore config)
codeletset_id: bufcap
codelet_descriptor:
  - codelet_name: bufcap
    codelet_path: ${JBPF_CODELETS}/bufcap/bufcap_64k.o
    hook_name: rlc_dl_ctrl
    priority: 1
```

`jrtc-apps/jrtc_apps/bufcap/deployment_64k.yaml` loads it, with no xApp:

```yaml
# generated by buffer-control-experiments/bufcap.sh
name: bufcap
jbpf:
  device:
    - id: 1
      host: srs-gnb-du1-proxy.ran.svc.cluster.local
      port: 30450
  codelet_set:
    - device: 1
      config: ${JBPF_CODELETS}/bufcap/bufcap_64k.yaml
```

### Run it

With the RAN and the UEs up as in [Demo 3](demo3-buffer-management.md), start its traffic: a 2 Mbit/s
video call and a download, both to UE 1. Then copy the object into the gNB container and load the
deployment with the `JRTC` function from Example 1. `jrtc-ctl` prints nothing when the load works.

```bash
cd ~/open-ai-ran-tutorial
bash buffer-control-experiments/traffic_A.sh start

kubectl exec -n ran srs-gnb-du1-0 -c ocudujbpf -- mkdir -p /codelets/bufcap
kubectl cp jrtc-apps/codelets/bufcap/bufcap_64k.o ran/srs-gnb-du1-0:/codelets/bufcap/ -c ocudujbpf
JRTC 'load -c /apps/bufcap/deployment_64k.yaml'
```

The gNB log shows `Registered codelet bufcap to hook rlc_dl_ctrl`. Watch UE 1 in the gNB console
(`bash scripts/gnb_console.sh`). Before the load, UE 1 receives 63 Mbit/s with about 2 MB queued
(`dl_bs`):

```text
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs
   1 4601 |  15 1.0   27    63M 1400    0   0%  1.95M
   1 4601 |  15 1.0   27    63M 1400    0   0%     2M
```

From the next downlink SDU on, the gNB drops any SDU that would take UE 1's queue past 64 KiB. The
queue drains and the rate falls:

```text
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs
   1 4601 |  15 1.0   26    24M  618    0   0%      0
   1 4601 |  15 1.0   26    18M  467    0   0%  1.51k
```

`/tmp/gnb.log` in the gNB container records each drop:

```text
[RLC     ] [W] du=0 ue=0 DRB1 DL: Dropped SDU. sdu_len=1503 pdcp_sn=66478 is_retx=false queued_sdus=43 queued_bytes=64629
```

[Demo 3](demo3-buffer-management.md) measures what each cap size does to the call's RTT and the
download's throughput.

Unload the codelet with the same file:

```bash
JRTC 'unload -c /apps/bufcap/deployment_64k.yaml'
```

The gNB keeps the last limit after the codelet is gone, and UE 1 stays near 16 Mbit/s. To
restore the configured queue, load `bufcap_off`, which writes `cfg_byte_limit` back, until the next
downlink packet has passed, then unload it. `bufcap.sh off` does both:

```bash
bash buffer-control-experiments/bufcap.sh off
```

```text
  loaded bufcap_off
  configured buffer restored; bufcap unloaded
```

UE 1 is back at 63 Mbit/s, with 1.5 to 3 MB queued.

### Set the limit from an xApp

To change the limit while the gNB runs, give the codelet an input channel:

- In the codelet, declare the channel and drain it on each call:
  `jbpf_control_input_map(ctrl_in, struct my_cmd, 32);` and
  `jbpf_control_input_receive(&ctrl_in, &cmd, sizeof(cmd))`.
- In the codeletset YAML, add `in_io_channel:` with `- name: ctrl_in`.
- In the xApp, open a stream to that channel with `is_rx` set to `False` and a concrete device id
  (`JrtcStreamIdCfg_t(JRTC_ROUTER_REQ_DEST_NONE, 1, ...)`), then send with
  `jrtc_app_router_channel_send_input_msg(app, stream_idx, msg, len(msg))`.

`codelets/bufctl/rlc_ctrl.cpp` and its xApp in `jrtc_apps/bufctl` set a limit per UE and bearer this
way, from the CLI in [Demo 3](demo3-buffer-management.md).
