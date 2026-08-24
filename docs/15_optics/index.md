# Datacenter Optics

本模块回答一个核心问题：当高速 electrical links 的 reach、power 与 density 不再可持续时，系统怎样把比特变成光，同时保留可制造性、互操作性与可维护性？

## 核心文章

- [Datacenter Optics：为什么高速 SerDes 最终必须把比特变成光](datacenter_optics.md)

## 学习结果

完成后应能：

- 画出 switch ASIC、SerDes、DSP、laser、modulator、fiber、photodiode 与 TIA 的 data path；
- 比较 retimed pluggable、LPO 与 CPO 的 power、margin、service 和 yield；
- 区分 direct detection 与 coherent 的适用 reach；
- 用 link budget 和 port arithmetic 检验产品主张；
- 把 optics 变化翻译为 packaging、test、supply chain 与 platform strategy。


## Optical architecture comparison

[Pluggable、LPO 与 CPO](pluggable_lpo_cpo.md) 比较 retiming、electrical reach、laser、thermal、yield 与 service boundary，解释为什么三种方案会共存，以及 CPO 如何把瓶颈从 PCB Signal Integrity 移向 photonic packaging 与 fleet repair。
