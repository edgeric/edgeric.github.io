# Hooks, Codelets and muApps

Everything you ran in the three demos is built from three kinds of programs. Codelets are small eBPF
programs that we load into the running gNB, at hooks in its code. xApps run in `jrtc-0`: they receive what
the codelets send, or send them settings. muApps belong to EdgeRIC; they run in `edgeric-0` and make a
decision every TTI.

This page shows how to write each of them. We start by adding a hook to the gNB, using `rlc_dl_ctrl` from
Demo 3. Then come three examples from the repository: `dl_sdu_count`, a telemetry codelet with an xApp
that prints what it sends; `bufcap`, the control codelet behind Demo 3's buffer caps; and `longestq`, a
scheduler muApp for EdgeRIC that you add yourself.

## Where Things Live

A hook is a function call we placed in the gNB's code. With no codelet attached, the call returns right
away. A monitor hook gives its codelet a read-only view (the UE, the bearer, the packet length), and the
codelet sends what it measured on an output channel. A control hook passes a struct that the gNB reads
back after the codelet returns, so a value the codelet writes there takes effect, for example a new queue
limit. The jbpf verifier checks every codelet before the gNB accepts it, so a broken codelet is rejected
instead of taking the cell down.

| What | Where |
|---|---|
| hook declarations | `ocudu-jbpf/srsran_jbpf/verifier/specs/jbpf_srsran_hooks.h` |
| hook contexts | `ocudu-jbpf/include/srsran/jbpf/jbpf_srsran_contexts.h` |
| codelets | `jrtc-apps/codelets/<name>/`: source, protobuf messages, `Makefile`, codeletset YAML |
| xApps | `jrtc-apps/jrtc_apps/<name>/`: the Python app and its deployment YAML |
| muApps | `edgeric-rt/muapps/`, with the schedulers in `edgeric-rt/edgeric_rt/policies.py` |

The pods mount these folders from your clone. `jrtc-0` has `jrtc-apps/jrtc_apps` at `/apps` and
`jrtc-apps/codelets` at `/codelets`, and `edgeric-0` has `edgeric-rt` at `/edgeric`, so you can change
code and reload it without rebuilding an image. [Miscellaneous](miscellaneous.md#hooks-used-in-this-tutorial)
lists every hook the tutorial uses.

## Adding a Hook to the gNB

You only need this when no existing hook fires where your code has to run. We'll go through
`rlc_dl_ctrl`, the control hook Demo 3 uses. The gNB calls it for every downlink SDU on an RLC AM data
bearer, just before it decides whether the SDU still fits in the queue.

**1. The context.** The struct goes in `include/srsran/jbpf/jbpf_srsran_contexts.h`. For a control hook,
mark which fields the gNB fills in and which ones the codelet writes back:

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

**2. The declaration.** `srsran_jbpf/verifier/specs/jbpf_srsran_hooks.h` declares the hook. In
`HOOK_ASSIGN`, the generic context that every codelet receives is pointed at your struct:

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

A hook can also hand over a few plain numbers in `srs_meta_data1` to `srs_meta_data4`. `rlc_dl_new_sdu`,
which Example 1 uses, packs the SDU length and the PDCP sequence number into the first one:
`ctx.srs_meta_data1 = (uint64_t)sdu_length << 32 | pdcp_sn;`.

**3. The call.** In the file where the hook should fire, `DEFINE_JBPF_CTRL_HOOK` creates a control hook
(`DEFINE_JBPF_HOOK` creates a monitor hook), and the gNB calls it like a function. Keep it all inside
`#ifdef JBPF_ENABLED`. From `lib/rlc/rlc_tx_am_entity.cpp`, trimmed:

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

The gNB clamps whatever the codelet asks for. A queue can't shrink below one maximum-size PDCP PDU
(9,007 bytes) or grow past its configured size.

**4. The image.** Rebuild the gNB image and recreate the gNB pod, as in Parts 1 and 2 of the
[tutorial](../open-ai-ran-tutorial.md):

```bash
cd ~/open-ai-ran-tutorial
docker build -t ocudu-gnb-jbpf:ipc -f ocudu-jbpf/docker/Dockerfile ocudu-jbpf
k3d image import ocudu-gnb-jbpf:ipc -c "$CLUSTER"
# then recreate the gNB pod with its containers (Part 2)
```

One thing to watch for: codelets compile against the headers in the jbpf SDK image, and those don't know
about hooks you add yourself. A codelet for a new hook keeps its own copy of the context struct, field
for field. Example 2 does this.

## Example 1: A Telemetry Codelet

`dl_sdu_count` counts the downlink SDUs and bytes that enter RLC, per UE, and sends the totals about once
a second. It runs on the `rlc_dl_new_sdu` monitor hook, and a short xApp prints its messages. The files:

```text
jrtc-apps/codelets/dl_sdu_count/      dl_sdu_count.proto  dl_sdu_count.cpp  Makefile  dl_sdu_count.yaml
jrtc-apps/jrtc_apps/dl_sdu_count/     dl_sdu_count_app.py  deployment.yaml
```

### The message

We describe what the codelet sends in a protobuf file. From it, the build makes a C struct for the
codelet, a serializer that the gNB loads, and a Python class for the xApp.

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

The codelet keeps its state in maps. `counts` holds each UE's running totals and the period they belong
to. When a UE's first SDU of a new period comes in, the codelet sends the totals of the period that just
ended and starts over, so a UE without traffic sends nothing. `out_counts` is the output channel; it
holds up to 64 messages on their way to the xApp.

### What the verifier checks

The gNB only loads a codelet that the verifier can prove safe. These are the rules we ran into first:

- Check `ctx->data` against `ctx->data_end` before you read the context.
- Give every loop a bound. `#pragma unroll` over a constant count works.
- Shift instead of dividing 64-bit numbers, as `PERIOD_SHIFT` does.
- Avoid `static const` tables. The loader can't place them and the verifier reports 0 instructions; a
  `switch` that returns the value works.
- Send one message per call. Our first version of this codelet sent one per UE in the same call, and
  only the first one reached the xApp.
- `make` doesn't track headers. After you edit one, delete the `.o` files in that directory.

### Building it

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

The build runs in the jbpf SDK container and ends with the verifier's verdict:

```text
Building dl_sdu_count
--------- dl_sdu_count.cpp ----------------------------------------------
Program terminates within 115 instructions
```

### The codeletset

`dl_sdu_count.yaml` puts the codelet on its hook and names the output channel and the message on it:

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

The xApp subscribes to the output channel and prints each message. Stream names follow
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

`deployment.yaml` loads the xApp and the codeletset with one command:

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

### Running it

Bring the RAN up with `--telemetry`, which starts the forwarder that `jrtc-ctl` needs, and start some
traffic, as in Part 2. Then copy the codelet directory into the gNB container, because the gNB's jbpf
agent loads the serializer from there, and load the deployment. `jrtc-0` reads the codelets and the
xApps from your clone.

```bash
cd ~/open-ai-ran-tutorial
JRTC() { kubectl exec -n ran jrtc-0 -c jrtc -- bash -c \
  "export JRTC_APPS=/apps JBPF_CODELETS=/codelets; /jrtc/out/bin/jrtc-ctl $*"; }

kubectl cp jrtc-apps/codelets/dl_sdu_count ran/srs-gnb-du1-0:/codelets/ -c ocudujbpf
JRTC 'load -c /apps/dl_sdu_count/deployment.yaml'
kubectl logs -n ran jrtc-0 -c jrtc -f | grep dl_sdu_count
```

In the gNB log you should see `Registered codelet dl_sdu_count to hook rlc_dl_new_sdu`, and the xApp
prints one line per UE about once a second. With two UEs downloading at about 30 Mbit/s each:

```text
[dl_sdu_count] ue 1: 2788 SDUs, 31.2 Mbit/s
[dl_sdu_count] ue 0: 2773 SDUs, 31.1 Mbit/s
[dl_sdu_count] ue 0: 2742 SDUs, 30.7 Mbit/s
[dl_sdu_count] ue 1: 2766 SDUs, 31.0 Mbit/s
```

An RLC SDU is a whole IP packet plus its PDCP header, so these rates come out a few percent above the
goodput that iperf3 reports at the UEs.

To unload it, pass the same file:

```bash
JRTC 'unload -c /apps/dl_sdu_count/deployment.yaml'
```

If you want the counts in Grafana, have the xApp write them to VictoriaMetrics, as the `_emit` function in
`jrtc_apps/upt/upt_app.py` does.

## Example 2: A Control Codelet

`bufcap` is the codelet behind Demo 3's buffer caps. It runs on `rlc_dl_ctrl` and gives the data bearers
of every UE the same byte limit, so the RLC queue drops packets once it holds that many bytes. The limit
is compiled in, so there is no xApp.

```text
jrtc-apps/codelets/bufcap/                 bufcap.cpp  Makefile
buffer-control-experiments/bufcap.sh       builds, loads and unloads it
```

### The codelet

`bufcap.cpp` carries its own copy of the hook's context struct and writes the limit on every call:

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

### Building it

Every limit is a separate object, built from the same source. The `one` target in the `Makefile`
compiles `bufcap.cpp` with `-DCAP_BYTES=<bytes>` and runs the verifier on the result:

```make
one:
	@echo "--------- bufcap.cpp -> bufcap_$(NAME).o (CAP_BYTES=$(CAP)) ---------"
	@$(CXX) $(CXXFLAGS) -DCAP_BYTES=$(CAP) $(INC) -c bufcap.cpp -o bufcap_$(NAME).o
	@$(VERIFIER_BIN) bufcap_$(NAME).o >/dev/null 2>&1 \
		&& echo "verifier: OK" \
		|| { echo "verifier: FAILED -- the gNB would reject bufcap_$(NAME).o"; rm -f bufcap_$(NAME).o; exit 1; }
```

`bufcap.sh build` runs that target in the SDK container, then writes a codeletset and a deployment for
each size:

```bash
cd ~/open-ai-ran-tutorial
bash buffer-control-experiments/bufcap.sh build 64k
```

```text
  --------- bufcap.cpp -> bufcap_64k.o (CAP_BYTES=65536) ---------
  verifier: OK
  built bufcap_64k (65536 bytes)
```

`jrtc-apps/codelets/bufcap/bufcap_64k.yaml` puts the object on the hook:

```yaml
# generated by buffer-control-experiments/bufcap.sh -- fixed RLC DL buffer cap (64k = 65536 bytes; 0 = restore config)
codeletset_id: bufcap
codelet_descriptor:
  - codelet_name: bufcap
    codelet_path: ${JBPF_CODELETS}/bufcap/bufcap_64k.o
    hook_name: rlc_dl_ctrl
    priority: 1
```

and `jrtc-apps/jrtc_apps/bufcap/deployment_64k.yaml` loads it:

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

### Running it

Bring the RAN and the UEs up as in [Demo 3](demo3-buffer-management.md) and start its traffic, a
2 Mbit/s video call plus a download, both to UE 1. Then copy the object into the gNB container and load
the deployment, with the `JRTC` function from Example 1. When the load works, `jrtc-ctl` prints nothing.

```bash
cd ~/open-ai-ran-tutorial
bash buffer-control-experiments/traffic_A.sh start

kubectl exec -n ran srs-gnb-du1-0 -c ocudujbpf -- mkdir -p /codelets/bufcap
kubectl cp jrtc-apps/codelets/bufcap/bufcap_64k.o ran/srs-gnb-du1-0:/codelets/bufcap/ -c ocudujbpf
JRTC 'load -c /apps/bufcap/deployment_64k.yaml'
```

The gNB log should show `Registered codelet bufcap to hook rlc_dl_ctrl`. Watch UE 1 in the gNB console
(`bash scripts/gnb_console.sh`). Before the load, it received 63 Mbit/s and had about 2 MB queued
(`dl_bs`):

```text
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs
   1 4601 |  15 1.0   27    63M 1400    0   0%  1.95M
   1 4601 |  15 1.0   27    63M 1400    0   0%     2M
```

From the next downlink SDU on, the gNB drops every SDU that would push UE 1's queue past 64 KiB. The
queue drains and the rate drops:

```text
 pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs
   1 4601 |  15 1.0   26    24M  618    0   0%      0
   1 4601 |  15 1.0   26    18M  467    0   0%  1.51k
```

The gNB logs each drop to `/tmp/gnb.log` in its container:

```text
[RLC     ] [W] du=0 ue=0 DRB1 DL: Dropped SDU. sdu_len=1503 pdcp_sn=66478 is_retx=false queued_sdus=43 queued_bytes=64629
```

[Demo 3](demo3-buffer-management.md) goes through what each cap size does to the call's RTT and to the
download. To unload the codelet, pass the same file:

```bash
JRTC 'unload -c /apps/bufcap/deployment_64k.yaml'
```

Unloading doesn't undo the cap. The gNB keeps the last limit it was given, and UE 1 stays near
16 Mbit/s. To get the configured queue back, load `bufcap_off`, which writes `cfg_byte_limit` back, wait
for the next downlink packet, then unload it. `bufcap.sh off` does all three:

```bash
bash buffer-control-experiments/bufcap.sh off
```

```text
  loaded bufcap_off
  configured buffer restored; bufcap unloaded
```

After that, UE 1 is back at 63 Mbit/s with 1.5 to 3 MB queued.

### Changing the limit from an xApp

`bufcap` can't change its limit while it runs. A codelet that takes settings at run time needs an input
channel:

- In the codelet, declare the channel and read it on every call:
  `jbpf_control_input_map(ctrl_in, struct my_cmd, 32);` and
  `jbpf_control_input_receive(&ctrl_in, &cmd, sizeof(cmd))`.
- In the codeletset YAML, add `in_io_channel:` with `- name: ctrl_in`.
- In the xApp, open a stream to that channel with `is_rx` set to `False` and a concrete device id
  (`JrtcStreamIdCfg_t(JRTC_ROUTER_REQ_DEST_NONE, 1, ...)`), then send with
  `jrtc_app_router_channel_send_input_msg(app, stream_idx, msg, len(msg))`.

`codelets/bufctl/rlc_ctrl.cpp` and the xApp in `jrtc_apps/bufctl` work this way; the CLI in
[Demo 3](demo3-buffer-management.md) talks to them. EdgeRIC's `rt_ctrl` codelet gets its actions the
same way, as the next example shows.

## Example 3: An EdgeRIC muApp

A muApp is a plain Python process in pod `edgeric-0`. It sits in the gNB's scheduling loop and decides
something every TTI. [Demo 2](demo2-ai-scheduling.md) runs the scheduler muApps that come with the
repository; here we look at how they work, then write a new scheduler.

### The loop

Two codelets on the MAC scheduler connect the gNB to the muApp. After every slot, `rt_report` on the
`mac_sched_slot_report` hook sends out the state of every UE. At the start of every slot, `rt_ctrl` on
`mac_sched_slot_ctrl` looks for an action meant for that slot. In between, the `rt_bridge` xApp in
`jrtc-0` passes the reports to the muApp and the actions back, over Unix sockets:

```text
gNB, MAC scheduler                      jrtc-0                         edgeric-0
rt_report  (mac_sched_slot_report) -->  rt_bridge_app.py --> muapp.sock  --> sched_muapp.py
rt_ctrl    (mac_sched_slot_ctrl)   <--  rt_act_in        <-- bridge.sock <-- weights + target TTI
```

Each report is 1,080 bytes, stamped with the slot's RANtime. The muApp gets it as a numpy record, and a
scheduler mostly needs these fields:

| Field | What it holds |
|---|---|
| `ran_tti` | RANtime, the gNB's slot counter |
| `dl_mask` | which of the next slots are downlink |
| `ue_count`, `ue` | the UEs: the first `ue_count` entries of `ue` are valid |
| `ue[i]["du_ue_index"]`, `ue[i]["rnti"]` | which UE |
| `ue[i]["cqi"]` | its last wideband CQI |
| `ue[i]["dl_pending_bytes"]` | its downlink backlog |
| `ue[i]["dl_prbs"]`, `ue[i]["dl_mcs"]` | what it got in this slot |
| `ue[i]["drb_bytes"]` | the bytes scheduled for it in this slot, the reward when you train with RL |
| `act_status`, `act_seq` | which action ran in this slot, if any |

The muApp answers with a weight per UE, tagged with the RANtime of the slot it is for and a sequence
number. `rt_ctrl` applies it only in that exact slot; we call that a HIT. A late action is dropped, and
a slot without an action runs the gNB's own scheduler. The report of the slot echoes the sequence number,
so the muApp knows which of its actions ran. By default the UE with the highest weight gets the whole
slot, and a tie goes to the UE that was served least recently.

`muapps/sched_muapp.py` runs the loop. Without the logging and the live controls, it comes down to this:

```python
rt = rte2.RtE2(lead=args.lead)                       # reports in, actions out
pol = policies.make(args.scheduler, args, ue_map)    # the scheduler, by name
sel = policies.SlotSelector()

while True:
    reps = rt.poll(timeout=0.5)       # every report newer than the last one, oldest first
    if not reps:
        continue                      # no new slot yet
    for r in reps:
        pol.observe(r)                # e.g. the averages in proportional fair

    newest = reps[-1]                 # act on the newest report only
    w = pol.weights(newest)           # {du_ue_index: weight}, or None
    if w is not None:
        target = rt.target_tti(newest)                # the next downlink slot
        u = sel.pick(target, w, pol.single_mode) if target is not None else None
        if u is not None:
            rt.send(newest, {u: 1})   # tagged with the target TTI and a sequence number
```

`poll()` waits for reports newer than the newest one it has seen. If several arrived while the muApp
was busy, it returns all of them, and the muApp acts on the newest. Every report still goes through
`observe()`, so a policy that keeps averages sees every slot. The action goes out before any bookkeeping,
because it has to reach the gNB within the slot.

### Writing a scheduler

So a scheduler is a class with a `weights()` method: given a report, it returns a weight per UE, or
`None` to leave the slot to the gNB. The ones Demo 2 uses (`rr`, `pf`, `maxcqi`, `maxweight`, `rl` and a
few more) live in `edgeric-rt/edgeric_rt/policies.py`, and most are a few lines long. Max-weight:

```python
class MaxWeight(Policy):
    name = "maxweight"

    def weights(self, rep):
        return {int(u["du_ue_index"]): float(u["cqi"]) * float(u["dl_pending_bytes"]) for u in _with_data(rep)}
```

Let's add longest-queue-first, which serves the UE with the most bytes waiting. Put the class in
`policies.py`, after `MaxWeight`:

```python
class LongestQueue(Policy):
    """Serve the UE with the most bytes queued."""

    name = "longestq"

    def weights(self, rep):
        return {int(u["du_ue_index"]): float(u["dl_pending_bytes"]) for u in _with_data(rep)}
```

Then register its name in `make()`, just before the `raise` at the end:

```python
    if name == "longestq":
        return LongestQueue()
```

`edgeric-0` runs the muApps from your clone, so there is nothing to rebuild. With Demo 2's setup running
(the RAN with `--edgeric`, four UEs on CQI walks and full-buffer UDP), start it and follow its log:

```bash
cd ~/open-ai-ran-tutorial
bash scripts/edgeric_muapp.sh start sched --scheduler longestq --tag longestq
bash scripts/edgeric_muapp.sh logs sched
```

```text
started sched (pid 17)
[sched] longestq | alloc single | lead 1 | strict | hold 0 | min-share 0.02 | reports from /apps/edgeric_rt/run/muapp.sock | run longestq
[sched longestq] tti=87022 |   8.7 Mbps (ue1   2.2 ue2   1.7 ue3   1.2 ue4   3.6) | DL HIT  99.7% of 7001 | report->action p50 114 p99 206 us | slack p1 70 us | RB use 1.03 | lazy-RIC 36 lost 6
[sched longestq] tti=97022 |   6.4 Mbps (ue1   1.8 ue2   1.3 ue3   0.9 ue4   2.4) | DL HIT  99.8% of 7000 | report->action p50 116 p99 211 us | slack p1 63 us | RB use 1.02 | lazy-RIC 49 lost 6
[sched longestq] tti=107023 |   9.0 Mbps (ue1   2.6 ue2   2.5 ue3   1.3 ue4   2.6) | DL HIT  99.7% of 7001 | report->action p50 115 p99 222 us | slack p1 64 us | RB use 1.04 | lazy-RIC 62 lost 6
```

The muApp is in the loop: 99.7 % of the downlink slots ran its action in exactly the TTI it targeted,
about 115 µs after the report. The cell, though, carries only 6 to 13 Mbit/s, split almost evenly
between the four UEs. Press Ctrl-C to leave the log, then switch the same muApp to round robin and to
max-weight, about half a minute apart:

```bash
bash scripts/edgeric_muapp.sh ctl "scheduler rr"
bash scripts/edgeric_muapp.sh ctl "scheduler maxweight"
```

```text
[sched rr] tti=216666 |  26.8 Mbps (ue1  11.4 ue2   2.8 ue3   8.0 ue4   4.6) | DL HIT  99.8% of 7000 | report->action p50 114 p99 212 us | slack p1 56 us | RB use 1.03 | lazy-RIC 287 lost 333
[sched rr] tti=226667 |  32.2 Mbps (ue1  12.7 ue2   0.9 ue3   9.0 ue4   9.5) | DL HIT  99.8% of 7001 | report->action p50 116 p99 197 us | slack p1 55 us | RB use 1.02 | lazy-RIC 302 lost 333
[sched maxweight] tti=306612 |  44.8 Mbps (ue1  15.3 ue2   0.0 ue3  29.5 ue4   0.0) | DL HIT  99.7% of 6960 | report->action p50 127 p99 241 us | slack p1 51 us | RB use 1.04 | lazy-RIC 446 lost 533
[sched maxweight] tti=316581 |  42.2 Mbps (ue1  31.9 ue2   0.0 ue3  10.3 ue4   0.0) | DL HIT  99.2% of 6962 | report->action p50 125 p99 411 us | slack p1 51 us | RB use 1.03 | lazy-RIC 469 lost 560
```

Round robin gives each UE a quarter of the slots, so each UE's rate follows its channel, 15 to
32 Mbit/s in total over the run. Max-weight reached 33 to 45. Longest-queue-first does worse than both,
and the reason is what its weight measures. With full-buffer UDP every queue sits at the RLC limit,
about 6.17 MB. A UE on a good channel takes more bytes off its queue in each slot it gets, so its queue
stays furthest below the limit, and the next slot goes to a UE on a weak channel whose queue has already
filled back up. The muApp saves every TTI to `edgeric-rt/runs/longestq/ttis.npz`, and in this run the UE
with the worst CQI won 53 % of the slots and the one with the best CQI 5 %. Max-weight multiplies the
same backlog by the CQI; with it, the best-CQI UE won 88 % of the slots.

Which UEs starve depends on the weight. Longest-queue-first holds back the strong channels, and
max-weight leaves the weak ones with nothing for seconds at a time (`ue2` and `ue4` above). Stop the
muApp with `bash scripts/edgeric_muapp.sh stop sched`.

A muApp doesn't have to be a scheduler. Any script under `edgeric-rt/` can read the reports with `RtE2`
from `edgeric_rt/rte2.py`, and `bash scripts/edgeric_muapp.sh run <script.py>` runs it in `edgeric-0`.
The bridge feeds one muApp at a time, so stop `sched` first.
