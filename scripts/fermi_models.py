#!/usr/bin/env python3
"""Transparent first-pass Fermi models for the knowledge base.

Every result is an estimate. Inputs and system boundaries remain the user's
responsibility; these functions intentionally avoid product-specific defaults.
"""

from __future__ import annotations

import argparse
import math


def roofline(peak_tflops: float, bandwidth_tb_s: float, ai_flop_byte: float) -> tuple[float, str]:
    memory_ceiling = bandwidth_tb_s * 1000.0 * ai_flop_byte
    achieved = min(peak_tflops, memory_ceiling)
    bound = "compute" if peak_tflops <= memory_ceiling else "memory"
    return achieved, bound


def coolant_flow(heat_kw: float, delta_c: float, cp_kj_kgk: float = 4.18) -> float:
    if delta_c <= 0 or cp_kj_kgk <= 0:
        raise ValueError("delta_c and cp_kj_kgk must be positive")
    return heat_kw / (cp_kj_kgk * delta_c)


def package_yield(die_yields: list[float], interface_yields: list[float], assembly_yield: float) -> float:
    values = die_yields + interface_yields + [assembly_yield]
    if any(value < 0 or value > 1 for value in values):
        raise ValueError("yield inputs must be between 0 and 1")
    return math.prod(values)


def delivered_compute(peak: float, efficiencies: list[float]) -> float:
    if any(value < 0 or value > 1 for value in efficiencies):
        raise ValueError("efficiencies must be between 0 and 1")
    return peak * math.prod(efficiencies)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI datacenter Fermi estimate helpers")
    sub = parser.add_subparsers(dest="model", required=True)

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
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.model == "roofline":
        value, bound = roofline(args.peak_tflops, args.bandwidth_tb_s, args.ai_flop_byte)
        print(f"estimated_tflops={value:.6g} bound={bound}")
    elif args.model == "cooling":
        value = coolant_flow(args.heat_kw, args.delta_c, args.cp_kj_kgk)
        print(f"estimated_mass_flow_kg_s={value:.6g}")
    elif args.model == "package-yield":
        value = package_yield(args.die_yields, args.interface_yields, args.assembly_yield)
        print(f"estimated_package_yield={value:.6g}")
    elif args.model == "delivered-compute":
        value = delivered_compute(args.peak, args.efficiencies)
        print(f"estimated_delivered_compute={value:.6g}")


if __name__ == "__main__":
    main()
