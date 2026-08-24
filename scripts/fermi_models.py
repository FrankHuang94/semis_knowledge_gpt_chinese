#!/usr/bin/env python3
"""Transparent Fermi models for AI datacenter engineering.

All outputs are estimates. Callers must define the workload, units, source
labels, and system boundary. Product-specific defaults are intentionally absent.
"""

from __future__ import annotations
import argparse
import math


def positive(name: str, value: float) -> float:
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def fraction(name: str, value: float) -> float:
    if value < 0 or value > 1:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


def roofline(peak_tflops: float, bandwidth_tb_s: float, ai_flop_byte: float) -> tuple[float, str]:
    positive("peak_tflops", peak_tflops)
    positive("bandwidth_tb_s", bandwidth_tb_s)
    positive("ai_flop_byte", ai_flop_byte)
    memory_ceiling = bandwidth_tb_s * 1000.0 * ai_flop_byte
    return min(peak_tflops, memory_ceiling), "compute" if peak_tflops <= memory_ceiling else "memory"


def coolant_flow(heat_kw: float, delta_c: float, cp_kj_kgk: float = 4.18) -> float:
    return positive("heat_kw", heat_kw) / (positive("cp_kj_kgk", cp_kj_kgk) * positive("delta_c", delta_c))


def package_yield(die_yields: list[float], interface_yields: list[float], assembly_yield: float) -> float:
    values = die_yields + interface_yields + [assembly_yield]
    if not values:
        raise ValueError("at least one yield input is required")
    return math.prod(fraction("yield", value) for value in values)


def delivered_compute(peak: float, efficiencies: list[float]) -> float:
    positive("peak", peak)
    if not efficiencies:
        raise ValueError("at least one efficiency is required")
    return peak * math.prod(fraction("efficiency", value) for value in efficiencies)


def kv_cache_gib(layers: int, tokens: int, batch: int, kv_heads: int, head_dim: int, bytes_per_element: float) -> float:
    values = {
        "layers": layers, "tokens": tokens, "batch": batch, "kv_heads": kv_heads,
        "head_dim": head_dim, "bytes_per_element": bytes_per_element,
    }
    for name, value in values.items():
        positive(name, float(value))
    total_bytes = 2 * layers * tokens * batch * kv_heads * head_dim * bytes_per_element
    return total_bytes / (1024 ** 3)


def ring_allreduce_seconds(message_gib: float, ranks: int, effective_gib_s: float) -> float:
    positive("message_gib", message_gib)
    positive("effective_gib_s", effective_gib_s)
    if ranks < 2:
        raise ValueError("ranks must be at least 2")
    traffic_gib = 2 * (ranks - 1) / ranks * message_gib
    return traffic_gib / effective_gib_s


def busbar(power_kw: float, voltage_v: float, resistance_microohm: float) -> tuple[float, float]:
    current_a = positive("power_kw", power_kw) * 1000 / positive("voltage_v", voltage_v)
    resistance_ohm = positive("resistance_microohm", resistance_microohm) * 1e-6
    loss_w = current_a ** 2 * resistance_ohm
    return current_a, loss_w


def good_output(capacities: list[float], final_yield: float) -> float:
    if not capacities:
        raise ValueError("at least one capacity is required")
    for value in capacities:
        positive("capacity", value)
    return min(capacities) * fraction("final_yield", final_yield)


def optical_modules(endpoints: int, ports_per_endpoint: float, links_per_module: int = 1, spare_fraction: float = 0) -> float:
    positive("endpoints", endpoints)
    positive("ports_per_endpoint", ports_per_endpoint)
    positive("links_per_module", links_per_module)
    if spare_fraction < 0:
        raise ValueError("spare_fraction must be non-negative")
    return endpoints * ports_per_endpoint / links_per_module * (1 + spare_fraction)


def self_test() -> None:
    assert roofline(1000, 4, 50) == (1000, "compute")
    assert abs(coolant_flow(100, 10) - 2.392344) < 1e-5
    assert abs(package_yield([0.96] * 4, [0.995] * 6, 0.97) - 0.795883) < 1e-4
    assert abs(delivered_compute(100, [0.75, 0.8, 0.95]) - 57) < 1e-9
    assert abs(kv_cache_gib(80, 16384, 1, 8, 128, 2) - 5) < 1e-9
    assert abs(ring_allreduce_seconds(8, 8, 200) - 0.07) < 1e-9
    current, loss = busbar(120, 50, 100)
    assert abs(current - 2400) < 1e-9 and abs(loss - 576) < 1e-9
    assert abs(good_output([20000, 18000, 15000], 0.92) - 13800) < 1e-9
    assert abs(optical_modules(100000, 1, 1, 0.05) - 105000) < 1e-9
    print("fermi self-test passed")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="AI datacenter Fermi estimate helpers")
    sub = root.add_subparsers(dest="model", required=True)

    roof = sub.add_parser("roofline")
    roof.add_argument("--peak-tflops", type=float, required=True)
    roof.add_argument("--bandwidth-tb-s", type=float, required=True)
    roof.add_argument("--ai-flop-byte", type=float, required=True)

    cooling = sub.add_parser("cooling")
    cooling.add_argument("--heat-kw", type=float, required=True)
    cooling.add_argument("--delta-c", type=float, required=True)
    cooling.add_argument("--cp-kj-kgk", type=float, default=4.18)

    package = sub.add_parser("package-yield")
    package.add_argument("--die-yields", type=float, nargs="+", required=True)
    package.add_argument("--interface-yields", type=float, nargs="*", default=[])
    package.add_argument("--assembly-yield", type=float, required=True)

    delivered = sub.add_parser("delivered-compute")
    delivered.add_argument("--peak", type=float, required=True)
    delivered.add_argument("--efficiencies", type=float, nargs="+", required=True)

    kv = sub.add_parser("kv-cache")
    kv.add_argument("--layers", type=int, required=True)
    kv.add_argument("--tokens", type=int, required=True)
    kv.add_argument("--batch", type=int, required=True)
    kv.add_argument("--kv-heads", type=int, required=True)
    kv.add_argument("--head-dim", type=int, required=True)
    kv.add_argument("--bytes-per-element", type=float, required=True)

    ring = sub.add_parser("ring-allreduce")
    ring.add_argument("--message-gib", type=float, required=True)
    ring.add_argument("--ranks", type=int, required=True)
    ring.add_argument("--effective-gib-s", type=float, required=True)

    power = sub.add_parser("busbar")
    power.add_argument("--power-kw", type=float, required=True)
    power.add_argument("--voltage-v", type=float, required=True)
    power.add_argument("--resistance-microohm", type=float, required=True)

    output = sub.add_parser("good-output")
    output.add_argument("--capacities", type=float, nargs="+", required=True)
    output.add_argument("--final-yield", type=float, required=True)

    optics = sub.add_parser("optical-modules")
    optics.add_argument("--endpoints", type=int, required=True)
    optics.add_argument("--ports-per-endpoint", type=float, required=True)
    optics.add_argument("--links-per-module", type=int, default=1)
    optics.add_argument("--spare-fraction", type=float, default=0)

    sub.add_parser("self-test")
    return root


def main() -> None:
    args = parser().parse_args()
    if args.model == "roofline":
        value, bound = roofline(args.peak_tflops, args.bandwidth_tb_s, args.ai_flop_byte)
        print(f"estimated_tflops={value:.6g} bound={bound}")
    elif args.model == "cooling":
        print(f"estimated_mass_flow_kg_s={coolant_flow(args.heat_kw, args.delta_c, args.cp_kj_kgk):.6g}")
    elif args.model == "package-yield":
        print(f"estimated_package_yield={package_yield(args.die_yields, args.interface_yields, args.assembly_yield):.6g}")
    elif args.model == "delivered-compute":
        print(f"estimated_delivered_compute={delivered_compute(args.peak, args.efficiencies):.6g}")
    elif args.model == "kv-cache":
        print(f"estimated_kv_cache_gib={kv_cache_gib(args.layers, args.tokens, args.batch, args.kv_heads, args.head_dim, args.bytes_per_element):.6g}")
    elif args.model == "ring-allreduce":
        print(f"estimated_seconds={ring_allreduce_seconds(args.message_gib, args.ranks, args.effective_gib_s):.6g}")
    elif args.model == "busbar":
        current, loss = busbar(args.power_kw, args.voltage_v, args.resistance_microohm)
        print(f"estimated_current_a={current:.6g} estimated_loss_w={loss:.6g}")
    elif args.model == "good-output":
        print(f"estimated_good_output={good_output(args.capacities, args.final_yield):.6g}")
    elif args.model == "optical-modules":
        print(f"estimated_modules={optical_modules(args.endpoints, args.ports_per_endpoint, args.links_per_module, args.spare_fraction):.6g}")
    elif args.model == "self-test":
        self_test()


if __name__ == "__main__":
    main()
