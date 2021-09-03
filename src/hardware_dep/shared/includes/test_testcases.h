// SPDX-License-Identifier: Apache-2.0
// Copyright 2018 Eotvos Lorand University, Budapest, Hungary

#pragma once

#include "test_testsuite.h"
#include "gen_model.h"

// ------------------------------------------------------
// Timeouts

#define NO_CTL_REPLY 0
#define CTL_REPLIES 200

#define WAIT_FOR_CTL  FSLEEP(200)

// ------------------------------------------------------
// Testcase steps

#define FDATA(...)    { __VA_ARGS__, "" }

#define FSLEEP(time)  {FAKE_PKT, 0, 0, FDATA(""), time, 0, FDATA("")}
#define FEND          {FAKE_END, 0, 0, FDATA(""),    0, 0, FDATA("")}


// for internal use
#define SIMPLESEND(inport, outport, ctl, pkt, ...)  {FAKE_PKT, 0, inport, FDATA(pkt), ctl, outport, FDATA(pkt), ##__VA_ARGS__}

#define BCAST -1
#define DROP  -2

// this packet is processed on the "fast path"
#define FAST(inport, out, pkt, ...)  SIMPLESEND(inport, out == BCAST ? T4P4S_BROADCAST_PORT : out, NO_CTL_REPLY, pkt, ##__VA_ARGS__)
// this packet is processed on the "slow path": the control plane is contacted while processing the packet
#define SLOW(inport, out, pkt, ...)  SIMPLESEND(inport, out == BCAST ? T4P4S_BROADCAST_PORT : out == DROP ? EGRESS_DROP_VALUE : out, CTL_REPLIES, pkt, ##__VA_ARGS__)

// ------------------------------------------------------
// Header field changes while processing packet

#define CHANGED(from, to)  "[" from "|" to "]"
#define ADDED(part)        CHANGED("", part)
#define REMOVED(part)      CHANGED(part, "")


// ------------------------------------------------------
// Conditions

#define REQ(reqs)       { reqs }
