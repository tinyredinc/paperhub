# Performance Case Study: Local LLM Inference on Multi-GPU and PCIe Bandwidth-Constrained Systems

**Author:** Samuel Zhang  
**Date:** 2025-04-30

## Abstract
The open-sourcing of large language models (LLMs), led by DeepSeek and other research institutions, has accelerated the feasibility of local LLM deployment. As access to high-capacity models increases, understanding the hardware factors affecting inference performance becomes essential. This case study evaluates the inference performance of AMD Radeon Instinct MI50 GPUs under different multi-GPU configurations and PCIe bandwidth conditions, using Ollama 0.6.3 as the inference framework on a standard high-memory server platform. Two key questions are explored: (1) whether inference performance improves when additional GPUs are introduced, either to increase compute resources or to provide sufficient combined VRAM for model loading, and (2) how reduced PCIe bandwidth impacts inference efficiency. Five test scenarios are evaluated using a 20 GB reasoning model (deepseek-r1:32b-qwen-distill-q4_K_M) and a 17 GB multimodal model (gemma3:27b-it-q4_K_M).

**All benchmarks were conducted using single-threaded inference to simulate the usage patterns typical of individual researchers or small research teams engaged in interactive prototyping, testing, or fine-tuning workflows.**

The findings aim to inform hardware planning and optimization strategies for efficient local deployment of large-scale LLMs in resource-constrained environments.


## Configuration
The experiments were conducted on a system with the following hardware specifications to ensure consistency across all test scenarios.
```
CPU: E5-2686V4 x 1
CHIPSET: C612
RAM: DDR4 64g x 8 = 512G
DISK: 2T NVME SSD
OS: Ubuntu 22.04
PLAT: ROCm 6.3.4
APP: Ollama 0.6.3
GPU0: AMD Radeon Instinct MI50 - 32G
GPU1: AMD Radeon Instinct MI50 - 32G
GPU2: AMD Radeon Instinct MI50 - 16G
GPU3: AMD Radeon Instinct MI50 - 16G
```

## Evaluation Tasks
Two evaluation tasks were designed to assess the models' capabilities in fact extraction and logical reasoning under varying hardware conditions.
- Task 1: Opinions and Facts Extraction
```
Please read the following paragraphs and list the facts and opinions:

In economics, the term “speculative bubble” refers to a large upward move in an asset’s price driven not by the asset’s fundamentals—that is, by the earnings derivable from the asset—but rather by mere speculation that someone else will be willing to pay a higher price for it. The price increase is then followed by a dramatic decline in price, due to a loss in confidence that the price will continue to rise, and the “bubble” is said to have burst. According to Charles Mackay’s classic nineteenth-century account, the seventeenth-century Dutch tulip market provides an example of a speculative bubble. But the economist Peter Garber challenges Mackay’s view, arguing that there is no evidence that the Dutch tulip market really involved a speculative bubble.

By the seventeenth century, the Netherlands had become a center of cultivation and development of new tulip varieties, and a market had developed in which rare varieties of bulbs sold at high prices. For example, a Semper Augustus bulb sold in 1625 for an amount of gold worth about U.S. $11,000 in 1999. Common bulb varieties, on the other hand, sold for very low prices. According to Mackay, by 1636 rapid price rises attracted speculators, and prices of many varieties surged upward from November 1636 through January 1637. Mackay further states that in February 1637 prices suddenly collapsed; bulbs could not be sold at 10 percent of their peak values. By 1739, the prices of all the most prized kinds of bulbs had fallen to no more than one two-hundredth of 1 percent of Semper Augustus’s peak price.

Garber acknowledges that bulb prices increased dramatically from 1636 to 1637 and eventually reached very low levels. But he argues that this episode should not be described as a speculative bubble, for the increase and eventual decline in bulb prices can be explained in terms of the fundamentals. Garber argues that a standard pricing pattern occurs for new varieties of flowers. When a particularly prized variety is developed, its original bulb sells for a high price. Thus, the dramatic rise in the price of some original tulip bulbs could have resulted as tulips in general, and certain varieties in particular, became fashionable. However, as the prized bulbs become more readily available through reproduction from the original bulb, their price falls rapidly; after less than 30 years, bulbs sell at reproduction cost. But this does not mean that the high prices of original bulbs are irrational, for earnings derivable from the millions of bulbs descendent from the original bulbs can be very high, even if each individual descendent bulb commands a very low price. Given that an original bulb can generate a reasonable return on investment even if the price of descendent bulbs decreases dramatically, a rapid rise and eventual fall of tulip bulb prices need not indicate a speculative bubble.
```
- Task 2: Logical Reasoning
```
There is a pond with an unlimited supply of water. You have two empty jugs, one that holds 5 litres and another that holds 6 litres. How can you use only these two jugs to obtain exactly 3 litres of water from the pond?
``` 

## Models Used
- deepseek-r1:32b-qwen-distill-q4_K_M  (20 GB): A reasoning-focused large language model.
- gemma3:27b-it-q4_K_M (17 GB): A multimodal model capable of language and vision tasks.

## Experimental Setup
LLM inference performance is affected by GPU memory capacity, multi-GPU scaling behavior, and PCIe interconnect bandwidth. While insufficient VRAM leads to fallback on system RAM and severe slowdowns, it remains unclear whether adding GPUs improves performance when a single GPU already has enough VRAM, or how distributing memory across GPUs impacts efficiency. Furthermore, PCIe bandwidth limitations may introduce additional bottlenecks. The following test scenarios are designed to systematically evaluate the impact of these factors on local LLM deployment.

### Test Scenario A
A single GPU with sufficient VRAM to load the model is used as the reference for baseline inference benchmarking.
```
MI50 32G x 1 on PCIE 3.0x16

GPU0: Radeon Instinct MI50 32GB
GUID:           58238
GPU%:           0%
VRAM%:          59%
TEMP_EDGE:      28.0°C
TEMP_VRAM:      29.0°C
POWER:          15.0W
SCLK:           925MHz
MCLK:           350MHz
PCIE:           8.0GT/s x16
```
- deepseek-r1:32b-qwen-distill-q4_K_M  [20G] - reasoning model
```
Task 1: Opinions and Facts Extraction
total duration:       1m12.604296887s
load duration:        42.120645ms
prompt eval count:    622 token(s)
prompt eval duration: 5.85805405s
prompt eval rate:     106.18 tokens/s
eval count:           1042 token(s)
eval duration:        1m6.702135792s
eval rate:            15.62 tokens/s

Task 2: Logical Reasoning
total duration:       59.806017486s
load duration:        46.652581ms
prompt eval count:    56 token(s)
prompt eval duration: 30.186146ms
prompt eval rate:     1855.16 tokens/s
eval count:           1000 token(s)
eval duration:        59.728019966s
eval rate:            16.74 tokens/s
```
- gemma3:27b-it-q4_K_M [17G] - multimodal model
```
Task 1: Opinions and Facts Extraction
total duration:       29.687839743s
load duration:        109.177595ms
prompt eval count:    628 token(s)
prompt eval duration: 64.912495ms
prompt eval rate:     9674.56 tokens/s
eval count:           540 token(s)
eval duration:        29.512635526s
eval rate:            18.30 tokens/s

Task 2: Logical Reasoning
total duration:       13.869249515s
load duration:        84.044473ms
prompt eval count:    60 token(s)
prompt eval duration: 54.104561ms
prompt eval rate:     1108.96 tokens/s
eval count:           267 token(s)
eval duration:        13.730159743s
eval rate:            19.45 tokens/s
```
### Test Scenario B
An additional GPU is added to the system, while the original GPU already possesses sufficient VRAM to load the model, in order to evaluate the impact of multi-GPU configurations on inference performance.
```
MI50 32G x 2 on PCIE 3.0 x16

GPU0: Radeon Instinct MI50 32GB          GPU1: Radeon Instinct MI50 32GB
GUID:           58238                    GUID:           30394
GPU%:           0%                       GPU%:           0%
VRAM%:          59%                      VRAM%:          0%
TEMP_EDGE:      32.0°C                   TEMP_EDGE:      29.0°C
TEMP_VRAM:      34.0°C                   TEMP_VRAM:      31.0°C
POWER:          17.0W                    POWER:          20.0W
SCLK:           925MHz                   SCLK:           930MHz
MCLK:           350MHz                   MCLK:           350MHz
PCIE:           8.0GT/s x16              PCIE:           8.0GT/s x16
```
- deepseek-r1:32b-qwen-distill-q4_K_M  [20G] - reasoning model
```
Task 1: Opinions and Facts Extraction
total duration:       1m7.06004565s
load duration:        34.944414ms
prompt eval count:    622 token(s)
prompt eval duration: 5.807858226s
prompt eval rate:     107.10 tokens/s
eval count:           955 token(s)
eval duration:        1m1.215839114s
eval rate:            15.60 tokens/s

Task 2: Logical Reasoning
total duration:       47.194736457s
load duration:        53.838865ms
prompt eval count:    56 token(s)
prompt eval duration: 169.638914ms
prompt eval rate:     330.11 tokens/s
eval count:           793 token(s)
eval duration:        46.969878417s
eval rate:            16.88 tokens/s
```
- gemma3:27b-it-q4_K_M [17G] - multimodal model
```
Task 1: Opinions and Facts Extraction
total duration:       40.173272493s
load duration:        102.110634ms
prompt eval count:    628 token(s)
prompt eval duration: 6.270755793s
prompt eval rate:     100.15 tokens/s
eval count:           608 token(s)
eval duration:        33.798824802s
eval rate:            17.99 tokens/s

Task 2: Logical Reasoning
total duration:       17.108307042s
load duration:        108.674703ms
prompt eval count:    60 token(s)
prompt eval duration: 589.428334ms
prompt eval rate:     101.79 tokens/s
eval count:           319 token(s)
eval duration:        16.409340464s
eval rate:            19.44 tokens/s
```

### Test Scenario C
Two GPUs are utilized, and their combined VRAM is sufficient to load the model, enabling evaluation of performance in a distributed memory configuration.
```
MI50 16G x 2 on PCIE 3.0 x16

GPU0: Vega 20 [Radeon VII]               GPU1: Vega 20 [Radeon VII]
GUID:           16388                    GUID:           54720
GPU%:           0%                       GPU%:           0%
VRAM%:          0%                       VRAM%:          0%
TEMP_EDGE:      30.0°C                   TEMP_EDGE:      33.0°C
TEMP_VRAM:      36.0°C                   TEMP_VRAM:      38.0°C
POWER:          22.0W                    POWER:          23.0W
SCLK:           808MHz                   SCLK:           808MHz
MCLK:           350MHz                   MCLK:           350MHz
PCIE:           8.0GT/s x16              PCIE:           8.0GT/s x16
```
- deepseek-r1:32b-qwen-distill-q4_K_M  [20G] - reasoning model  
```
Task 1: Opinions and Facts Extraction
total duration:       1m2.405194332s
load duration:        53.80572ms
prompt eval count:    622 token(s)
prompt eval duration: 3.529049785s
prompt eval rate:     176.25 tokens/s
eval count:           903 token(s)
eval duration:        58.82094424s
eval rate:            15.35 tokens/s

Task 2: Logical Reasoning
total duration:       44.148854915s
load duration:        56.067874ms
prompt eval count:    56 token(s)
prompt eval duration: 535.013123ms
prompt eval rate:     104.67 tokens/s
eval count:           738 token(s)
eval duration:        43.554881247s
eval rate:            16.94 tokens/s
```
- gemma3:27b-it-q4_K_M [17G] - multimodal model  
```
Task 1: Opinions and Facts Extraction
total duration:       34.360587039s
load duration:        111.187602ms
prompt eval count:    628 token(s)
prompt eval duration: 6.039297172s
prompt eval rate:     103.99 tokens/s
eval count:           511 token(s)
eval duration:        28.208681659s
eval rate:            18.11 tokens/s

Task 2: Logical Reasoning
total duration:       14.444555087s
load duration:        107.966926ms
prompt eval count:    60 token(s)
prompt eval duration: 576.511747ms
prompt eval rate:     104.07 tokens/s
eval count:           273 token(s)
eval duration:        13.759138125s
eval rate:            19.84 tokens/s
```

### Test Scenario D
A single GPU with sufficient VRAM to load the model is utilized, but connected via a reduced-bandwidth PCIe 3.0 x8 slot, to assess the impact of limited interconnect bandwidth on inference performance.
```
MI50 32G x 1 on PCIE 3.0 x8

GPU0: Radeon Instinct MI50 32GB
GUID:           58238
GPU%:           0%
VRAM%:          0%
TEMP_EDGE:      28.0°C
TEMP_VRAM:      31.0°C
POWER:          22.0W
SCLK:           930MHz
MCLK:           350MHz
PCIE:           8.0GT/s x8
```
- deepseek-r1:32b-qwen-distill-q4_K_M  [20G] - reasoning model
```
Task 1: Opinions and Facts Extraction
total duration:       1m15.667275307s
load duration:        55.662617ms
prompt eval count:    622 token(s)
prompt eval duration: 5.888914011s
prompt eval rate:     105.62 tokens/s
eval count:           1086 token(s)
eval duration:        1m9.719939524s
eval rate:            15.58 tokens/s

Task 2: Logical Reasoning
total duration:       53.442965924s
load duration:        34.707278ms
prompt eval count:    56 token(s)
prompt eval duration: 33.473778ms
prompt eval rate:     1672.95 tokens/s
eval count:           896 token(s)
eval duration:        53.373618995s
eval rate:            16.79 tokens/s
```
- gemma3:27b-it-q4_K_M [17G] - multimodal model
```
Task 1: Opinions and Facts Extraction
total duration:       43.254142337s
load duration:        110.363326ms
prompt eval count:    628 token(s)
prompt eval duration: 6.308619578s
prompt eval rate:     99.55 tokens/s
eval count:           654 token(s)
eval duration:        36.833758767s
eval rate:            17.76 tokens/s

Task 2: Logical Reasoning
total duration:       11.242355808s
load duration:        109.188923ms
prompt eval count:    60 token(s)
prompt eval duration: 589.139789ms
prompt eval rate:     101.84 tokens/s
eval count:           205 token(s)
eval duration:        10.542945484s
eval rate:            19.44 tokens/s
```

### Test Scenario E
Two GPUs are utilized, and their combined VRAM is sufficient to load the model; however, both GPUs are connected via reduced-bandwidth PCIe 3.0 x8 slots, allowing evaluation of performance under limited interconnect conditions.
```
MI50 16G x 2 on PCIE 3.0 x8

GPU0: Vega 20 [Radeon VII]               GPU1: Vega 20 [Radeon VII]
GUID:           16388                    GUID:           54720
GPU%:           0%                       GPU%:           0%
VRAM%:          0%                       VRAM%:          0%
TEMP_EDGE:      30.0°C                   TEMP_EDGE:      34.0°C
TEMP_VRAM:      36.0°C                   TEMP_VRAM:      38.0°C
POWER:          22.0W                    POWER:          23.0W
SCLK:           808MHz                   SCLK:           808MHz
MCLK:           350MHz                   MCLK:           350MHz
PCIE:           8.0GT/s x8               PCIE:           8.0GT/s x8
```
- deepseek-r1:32b-qwen-distill-q4_K_M  [20G] - reasoning model
```
Task 1: Opinions and Facts Extraction
total duration:       1m15.350784948s
load duration:        54.357303ms
prompt eval count:    622 token(s)
prompt eval duration: 3.743334321s
prompt eval rate:     166.16 tokens/s
eval count:           1094 token(s)
eval duration:        1m11.550864786s
eval rate:            15.29 tokens/s

Task 2: Logical Reasoning
total duration:       49.551179655s
load duration:        55.674343ms
prompt eval count:    56 token(s)
prompt eval duration: 369.829767ms
prompt eval rate:     151.42 tokens/s
eval count:           838 token(s)
eval duration:        49.124419454s
eval rate:            17.06 tokens/s
```
- gemma3:27b-it-q4_K_M [17G] - multimodal model
```
Task 1: Opinions and Facts Extraction
total duration:       38.287992779s
load duration:        110.205682ms
prompt eval count:    628 token(s)
prompt eval duration: 6.052284209s
prompt eval rate:     103.76 tokens/s
eval count:           584 token(s)
eval duration:        32.123981551s
eval rate:            18.18 tokens/s

Task 2: Logical Reasoning
total duration:       14.297120406s
load duration:        110.435341ms
prompt eval count:    60 token(s)
prompt eval duration: 581.868484ms
prompt eval rate:     103.12 tokens/s
eval count:           270 token(s)
eval duration:        13.603890199s
eval rate:            19.85 tokens/s
```

## Result Analysis

### Summary Table – `eval rate` (tokens/s)

| Scenario | Mi50 GPU Setup                       | deepseek-r1 T1 | deepseek-r1 T2 | gemma3 T1 | gemma3 T2 |
|----------|----------------------------------|----------------|----------------|-----------|-----------|
| A        | 1×32G PCIe 3.0 x16              | 15.62          | 16.74          | 18.30     | 19.45     |
| B        | 2×32G PCIe 3.0 x16              | 15.60          | 16.88          | 17.99     | 19.44     |
| C        | 2×16G PCIe 3.0 x16              | 15.35          | 16.94          | 18.11     | 19.84     |
| D        | 1×32G PCIe 3.0 x8               | 15.58          | 16.79          | 17.76     | 19.44     |
| E        | 2×16G PCIe 3.0 x8               | 15.29          | 17.06          | 18.18     | 19.85     |

### Impact of Multi-GPU Configurations

#### Scenario A → B: Adding a Second 32GB GPU (Sufficient VRAM)
Adding a second GPU to a setup that already has enough VRAM does **not improve eval rate**:
- **deepseek-r1**:
  - Task 1: 15.62 → 15.60 tokens/s (↓0.13%)
  - Task 2: 16.74 → 16.88 tokens/s (↑0.84%)
- **gemma3**:
  - Task 1: 18.30 → 17.99 tokens/s (↓1.70%)
  - Task 2: 19.45 → 19.44 tokens/s (↓0.05%)

These variations fall within noise margin. The data confirms **no parallelism benefit** when one GPU suffices.

---

#### Scenario A → C: Distributed VRAM with Two 16GB GPUs
Splitting the model across two GPUs with combined VRAM shows **minor degradation or parity**:
- **deepseek-r1**:
  - Task 1: 15.62 → 15.35 tokens/s (↓1.73%)
  - Task 2: 16.74 → 16.94 tokens/s (↑1.19%)
- **gemma3**:
  - Task 1: 18.30 → 18.11 tokens/s (↓1.04%)
  - Task 2: 19.45 → 19.84 tokens/s (↑2.00%)

Distributed loading is feasible without major penalty. Slight performance gain in Task 2 may reflect memory locality advantages.

---

#### Scenario C → E: Distributed VRAM with Reduced PCIe Bandwidth
Moving to x8 lanes on both GPUs incurs **no meaningful eval rate drop**:
- **deepseek-r1**:
  - Task 1: 15.35 → 15.29 tokens/s (↓0.39%)
  - Task 2: 16.94 → 17.06 tokens/s (↑0.71%)
- **gemma3**:
  - Task 1: 18.11 → 18.18 tokens/s (↑0.39%)
  - Task 2: 19.84 → 19.85 tokens/s (↑0.05%)

This indicates **bandwidth is not a bottleneck** even in distributed memory scenarios.

---

#### Scenario A → D: Single GPU on PCIe x16 vs. x8
Reducing PCIe bandwidth from x16 to x8 **does not degrade inference throughput**:
- **deepseek-r1**:
  - Task 1: 15.62 → 15.58 tokens/s (↓0.26%)
  - Task 2: 16.74 → 16.79 tokens/s (↑0.30%)
- **gemma3**:
  - Task 1: 18.30 → 17.76 tokens/s (↓2.95%)
  - Task 2: 19.45 → 19.44 tokens/s (↓0.05%)

Even the largest observed drop (gemma3 Task 1) remains under 3%, suggesting **model load latency is isolated** from token evaluation performance.


## Conclusion

This performance case study demonstrates that local LLM inference using Ollama 0.6.3 on AMD MI50 GPUs is **highly stable and efficient across a range of hardware configurations**, as long as VRAM requirements are met. The findings highlight several practical insights for deploying large models locally:

### Key Takeaways

- **Eval throughput remains consistent across all scenarios**, with less than 3% variation in token generation speed.
- **Adding additional GPUs does not improve performance** unless required for meeting VRAM capacity. Ollama does not leverage multi-GPU compute when unnecessary.
- **Distributing model memory across two GPUs introduces minimal overhead**, making it a viable strategy for running large models with smaller cards.
- **PCIe bandwidth has negligible impact** on eval rate. PCIe 3.0 x8 performs on par with x16 for inference workloads, even in dual-GPU setups.

These results suggest that **memory availability is the primary hardware constraint**, while bandwidth and compute redundancy have limited influence on LLM inference speed. Efficient local deployment should prioritize ensuring adequate VRAM per model and using available PCIe lanes flexibly without overengineering the system.



## Miscellaneous

### Test Log
- [View detailed test log: mi50_llm_testlog.md](mi50_llm_testlog.md)