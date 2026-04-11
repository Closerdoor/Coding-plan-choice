# 模型能力榜单（自动生成）

- 生成时间（UTC）：2026-04-11T13:17:53+00:00
- 说明：按 5 个榜单（代码优先）做分位数标准化后加权平均；缺失榜单不计入分母。
- 权重：SWE-bench 0.30、LiveCodeBench 0.30、Arena 0.15、HELM 0.15、OpenCompass 0.10。
- 过滤规则（Top3 输出用）：排除 distill/quant/int4/int8/gguf/awq/gptq 以及 mini/small/lite/tiny 等小模型。

## 全局排名
| Rank | Provider    | Model                               | Score(0..1) | SWE   | LCB   | Arena | HELM | OC    |
| ---- | ----------- | ----------------------------------- | ----------- | ----- | ----- | ----- | ---- | ----- |
| 1    | Google      | Gemini-2.5-Pro-06-05                | 1.0000      |       | 1.000 |       |      |       |
| 2    | Anthropic   | claude-opus-4-5                     | 0.9873      | 0.987 |       |       |      |       |
| 3    | ByteDance   | Doubao-Seed-1.6                     | 0.9747      | 0.975 |       |       |      |       |
| 4    | Google      | Gemini-3-Pro-Preview                | 0.9715      | 0.962 |       |       |      | 1.000 |
| 5    | Anthropic   | claude-4-5-opus                     | 0.9494      | 0.949 |       |       |      |       |
| 6    | Anthropic   | claude-opus-4-5-20251101            | 0.9467      | 1.000 |       | 0.840 |      |       |
| 7    | Google      | Gemini-2.5-Flash-04-17              | 0.9375      |       | 0.938 |       |      |       |
| 8    | OpenAI      | gpt-5                               | 0.9367      | 0.937 |       |       |      |       |
| 9    | Anthropic   | claude-opus-4-6                     | 0.9156      | 0.873 |       | 1.000 |      |       |
| 10   | Google      | gemini-2.5-pro-06-17                | 0.9114      | 0.911 |       |       |      |       |
| 11   | Google      | gemini-3-flash-preview              | 0.8987      | 0.899 |       |       |      |       |
| 12   | DeepSeek    | DeepSeek-R1-0528                    | 0.8750      |       | 0.875 |       |      |       |
| 13   | Google      | gemini-2.5-pro-preview-06-05        | 0.8608      | 0.861 |       |       |      |       |
| 14   | Anthropic   | claude-sonnet-4-5                   | 0.8481      | 0.848 |       |       |      |       |
| 15   | Anthropic   | claude-4-sonnet-20250514            | 0.8354      | 0.835 |       |       |      |       |
| 16   | OpenAI      | gpt-4.1                             | 0.8228      | 0.823 |       |       |      |       |
| 17   | OpenAI      | gpt-5-2025-08-07                    | 0.8101      | 0.810 |       |       |      |       |
| 18   | Zhipu AI    | GLM-5                               | 0.8010      | 0.772 |       | 0.800 |      | 0.889 |
| 19   | Anthropic   | claude-4-opus-20250514              | 0.7975      | 0.797 |       |       |      |       |
| 20   | Google      | gemini-3-flash                      | 0.7912      | 0.747 |       | 0.880 |      |       |
| 21   | OpenAI      | GPT-5-2025-08-07 (high)             | 0.7778      |       |       |       |      | 0.778 |
| 22   | OpenAI      | GPT-4-Turbo-2024-04-09              | 0.7500      |       | 0.750 |       |      |       |
| 23   | OpenAI      | gpt-5-2-codex                       | 0.7499      | 0.785 |       | 0.680 |      |       |
| 24   | OpenAI      | gpt-5.2-2025-12-11                  | 0.7342      | 0.734 |       |       |      |       |
| 25   | Anthropic   | claude-sonnet-4-5-20250929          | 0.7259      | 0.709 |       | 0.760 |      |       |
| 26   | Google      | gemini-3-pro                        | 0.7251      | 0.608 |       | 0.960 |      |       |
| 27   | OpenAI      | openai/gpt-5-2025-08-07             | 0.7215      | 0.722 |       |       |      |       |
| 28   | OpenAI      | gpt-5-2                             | 0.7063      | 0.759 |       | 0.600 |      |       |
| 29   | MiniMax     | minimax-m2.5                        | 0.6974      | 0.886 |       | 0.320 |      |       |
| 30   | OpenAI      | gpt-4o                              | 0.6962      | 0.696 |       |       |      |       |
| 31   | Anthropic   | claude-sonnet-4-20250514            | 0.6960      | 0.924 |       | 0.240 |      |       |
| 32   | Zhipu AI    | GLM-4.7                             | 0.6853      |       |       | 0.920 |      | 0.333 |
| 33   | Google      | gemini-2.5-pro                      | 0.6704      | 0.646 |       | 0.720 |      |       |
| 34   | Alibaba     | Qwen3.5-397B-A17B                   | 0.6667      |       |       |       |      | 0.667 |
| 35   | Moonshot AI | Kimi-K2.5                           | 0.6326      | 0.658 |       |       |      | 0.556 |
| 36   | OpenAI      | O3 (High)                           | 0.6250      |       | 0.625 |       |      |       |
| 37   | Alibaba     | Qwen/Qwen3-Coder-480B-A35B-Instruct | 0.6203      | 0.620 |       |       |      |       |
| 38   | Moonshot AI | kimi-k2-0905-preview                | 0.6157      | 0.684 |       | 0.480 |      |       |
| 39   | MiniMax     | minimax-2.5                         | 0.5949      | 0.595 |       |       |      |       |
| 40   | OpenAI      | gpt-4.1-2025-04-14                  | 0.5939      | 0.671 |       | 0.440 |      |       |
| 41   | Meta        | meta-llama/Llama-3.3-70B-Instruct   | 0.5823      | 0.582 |       |       |      |       |
| 42   | Zhipu AI    | zai-org/GLM-4.6                     | 0.5696      | 0.570 |       |       |      |       |
| 43   | OpenAI      | gpt-5.1-codex                       | 0.5678      | 0.532 |       | 0.640 |      |       |
| 44   | OpenAI      | GPT-4O-2024-08-06                   | 0.5400      | 0.392 | 0.688 |       |      |       |
| 45   | OpenAI      | gpt-5.1-2025-11-13                  | 0.5190      | 0.519 |       |       |      |       |
| 46   | DeepSeek    | DeepSeek-V3.2                       | 0.5072      | 0.633 |       | 0.520 |      | 0.111 |
| 47   | Moonshot AI | moonshot/kimi-k2-0711-preview       | 0.5063      | 0.506 |       |       |      |       |
| 48   | DeepSeek    | DeepSeek-V3                         | 0.5012      | 0.190 | 0.812 |       |      |       |
| 49   | Anthropic   | Claude-3-Haiku                      | 0.5000      |       | 0.500 |       |      |       |
| 50   | OpenAI      | o1-preview                          | 0.4937      | 0.494 |       |       |      |       |
| 51   | Anthropic   | claude-haiku-4-5-20251001           | 0.4913      | 0.557 |       | 0.360 |      |       |
| 52   | Zhipu AI    | zai-org/GLM-4.5                     | 0.4810      | 0.481 |       |       |      |       |
| 53   | OpenAI      | o3-2025-04-16                       | 0.4567      | 0.405 |       | 0.560 |      |       |
| 54   | DeepSeek    | DeepSeek-V3.2-Speciale              | 0.4444      |       |       |       |      | 0.444 |
| 55   | Anthropic   | Claude-Sonnet-4 (Thinking)          | 0.4375      |       | 0.438 |       |      |       |
| 56   | Anthropic   | Claude-3.5-Sonnet-20241022          | 0.4313      | 0.456 | 0.562 | 0.120 |      |       |
| 57   | DeepSeek    | deepseek-v3.2-reasoner              | 0.4304      | 0.430 |       |       |      |       |
| 58   | Unknown     | agentica-org/DeepSWE-Preview        | 0.4177      | 0.418 |       |       |      |       |
| 59   | Anthropic   | claude-3-7-sonnet-20250219          | 0.3895      | 0.544 |       | 0.080 |      |       |
| 60   | Anthropic   | Claude-Opus-4 (Thinking)            | 0.3750      |       | 0.375 |       |      |       |
| 61   | Zhipu AI    | glm-4.6                             | 0.3671      | 0.367 |       |       |      |       |
| 62   | Zhipu AI    | GLM-4.5                             | 0.3544      | 0.354 |       |       |      |       |
| 63   | Moonshot AI | Kimi-K2-Thinking                    | 0.3513      | 0.468 |       |       |      | 0.000 |
| 64   | Mistral     | devstral-2512                       | 0.3418      | 0.342 |       |       |      |       |
| 65   | Moonshot AI | Kimi-K2-Instruct                    | 0.3291      | 0.329 |       |       |      |       |
| 66   | Alibaba     | Qwen3-Coder-480B-A35B-Instruct      | 0.3198      | 0.380 |       | 0.200 |      |       |
| 67   | Google      | gemini-2.5-pro-preview-05-06        | 0.3165      | 0.316 |       |       |      |       |
| 68   | Anthropic   | Claude-Opus-4                       | 0.3125      |       | 0.312 |       |      |       |
| 69   | DeepSeek    | deepseek-reasoner                   | 0.3038      | 0.304 |       |       |      |       |
| 70   | MiniMax     | minimax-m2                          | 0.2954      | 0.443 |       | 0.000 |      |       |
| 71   | Google      | gemini-2.0-flash-exp                | 0.2911      | 0.291 |       |       |      |       |
| 72   | Amazon      | amazon.nova-premier-v1:0            | 0.2785      | 0.278 |       |       |      |       |
| 73   | DeepSeek    | DeepSeek-V3-0324                    | 0.2658      | 0.266 |       |       |      |       |
| 74   | StepFun     | Step-3.5-Flash                      | 0.2569      |       |       | 0.280 |      | 0.222 |
| 75   | Anthropic   | claude-3.5-sonnet-latest            | 0.2532      | 0.253 |       |       |      |       |
| 76   | Anthropic   | Claude-Sonnet-4                     | 0.2500      |       | 0.250 |       |      |       |
| 77   | Meta        | Llama3-SWE-RL-70B                   | 0.2405      | 0.241 |       |       |      |       |
| 78   | Alibaba     | Qwen 2.5                            | 0.2278      | 0.228 |       |       |      |       |
| 79   | Google      | gemini-2.5-flash                    | 0.2262      | 0.139 |       | 0.400 |      |       |
| 80   | Anthropic   | claude-3-haiku-20240307             | 0.2152      | 0.215 |       |       |      |       |
| 81   | OpenAI      | gpt-4o-2024-05-13                   | 0.2025      | 0.203 |       |       |      |       |
| 82   | Google      | Gemini-2.5-Pro-05-06                | 0.1875      |       | 0.188 |       |      |       |
| 83   | Anthropic   | claude-4-sonnet                     | 0.1772      | 0.177 |       |       |      |       |
| 84   | OpenAI      | gpt-5-nano-2025-08-07               | 0.1646      | 0.165 |       |       |      |       |
| 85   | DeepSeek    | deepseek-chat                       | 0.1519      | 0.152 |       |       |      |       |
| 86   | OpenAI      | gpt-4-1106-preview                  | 0.1266      | 0.127 |       |       |      |       |
| 87   | Google      | Gemini-2.5-Flash-05-20              | 0.1250      |       | 0.125 |       |      |       |
| 88   | OpenAI      | gpt-4-0613                          | 0.1013      | 0.101 |       |       |      |       |
| 89   | Alibaba     | Qwen3-235B-A22B                     | 0.0950      |       | 0.062 | 0.160 |      |       |
| 90   | OpenAI      | gpt-oss-120b                        | 0.0893      | 0.114 |       | 0.040 |      |       |
| 91   | OpenAI      | gpt-4o-20241120                     | 0.0886      | 0.089 |       |       |      |       |
| 92   | Meta        | llama-4-maverick-instruct           | 0.0759      | 0.076 |       |       |      |       |
| 93   | OpenAI      | gpt-4-0125-preview                  | 0.0633      | 0.063 |       |       |      |       |
| 94   | Anthropic   | claude-3-opus-20240229              | 0.0506      | 0.051 |       |       |      |       |
| 95   | Google      | gemini-2.0-flash                    | 0.0380      | 0.038 |       |       |      |       |
| 96   | Meta        | llama-4-scout-instruct              | 0.0253      | 0.025 |       |       |      |       |
| 97   | Anthropic   | claude-2                            | 0.0127      | 0.013 |       |       |      |       |
| 98   | OpenAI      | XBai-o4-medium                      | 0.0000      |       | 0.000 |       |      |       |
| 99   | Unknown     | SWE-Llama                           | 0.0000      | 0.000 |       |       |      |       |

## 数据源

- LiveCodeBench: https://livecodebench.github.io/
- SWE-bench: https://www.swebench.com/
- Arena: https://lmarena.ai/leaderboard
- HELM: https://crfm.stanford.edu/helm/latest/
- OpenCompass Rank: https://rank.opencompass.org.cn/
