# 模型能力榜单（自动生成）

- 生成时间（UTC）：2026-09-21T08:41:26+00:00
- 说明：按 5 个榜单（代码优先）做分位数标准化后加权平均；缺失榜单不计入分母。
- 权重：SWE-bench 0.30、LiveCodeBench 0.30、Arena 0.15、HELM 0.15、OpenCompass 0.10。
- 过滤规则（Top3 输出用）：排除 distill/quant/int4/int8/gguf/awq/gptq 以及 mini/small/lite/tiny 等小模型。

## 全局排名
| Rank | Provider    | Model                               | Score(0..1) | SWE   | LCB   | Arena | HELM | OC    |
| ---- | ----------- | ----------------------------------- | ----------- | ----- | ----- | ----- | ---- | ----- |
| 1    | Google      | Gemini-2.5-Pro-06-05                | 1.0000      |       | 1.000 |       |      |       |
| 2    | Anthropic   | claude-opus-4-5-20251101            | 1.0000      | 1.000 |       |       |      |       |
| 3    | Anthropic   | claude-opus-4-5                     | 0.9873      | 0.987 |       |       |      |       |
| 4    | ByteDance   | Doubao-Seed-1.6                     | 0.9747      | 0.975 |       |       |      |       |
| 5    | Google      | Gemini-3-Pro-Preview                | 0.9715      | 0.962 |       |       |      | 1.000 |
| 6    | OpenAI      | gpt-5                               | 0.9494      | 0.949 |       |       |      |       |
| 7    | Google      | Gemini-2.5-Flash-04-17              | 0.9375      |       | 0.938 |       |      |       |
| 8    | Anthropic   | claude-4-5-opus                     | 0.9241      | 0.924 |       |       |      |       |
| 9    | Google      | gemini-2.5-pro-06-17                | 0.9114      | 0.911 |       |       |      |       |
| 10   | Google      | gemini-3-flash-preview              | 0.8987      | 0.899 |       |       |      |       |
| 11   | DeepSeek    | DeepSeek-R1-0528                    | 0.8750      |       | 0.875 |       |      |       |
| 12   | Anthropic   | claude-opus-4-6                     | 0.8734      | 0.873 |       |       |      |       |
| 13   | Google      | gemini-2.5-pro-preview-06-05        | 0.8608      | 0.861 |       |       |      |       |
| 14   | Anthropic   | claude-sonnet-4-5                   | 0.8481      | 0.848 |       |       |      |       |
| 15   | Zhipu AI    | GLM-5                               | 0.8481      | 0.785 |       | 0.947 |      | 0.889 |
| 16   | Anthropic   | claude-4-sonnet-20250514            | 0.8354      | 0.835 |       |       |      |       |
| 17   | Google      | gemini-3-flash                      | 0.8312      | 0.747 |       | 1.000 |      |       |
| 18   | OpenAI      | gpt-4.1                             | 0.8228      | 0.823 |       |       |      |       |
| 19   | OpenAI      | gpt-5-2025-08-07                    | 0.8101      | 0.810 |       |       |      |       |
| 20   | Anthropic   | claude-4-opus-20250514              | 0.7975      | 0.797 |       |       |      |       |
| 21   | OpenAI      | GPT-5-2025-08-07 (high)             | 0.7778      |       |       |       |      | 0.778 |
| 22   | Anthropic   | claude-sonnet-4-5-20250929          | 0.7708      | 0.709 |       | 0.895 |      |       |
| 23   | OpenAI      | gpt-5-2                             | 0.7519      | 0.759 |       | 0.737 |      |       |
| 24   | OpenAI      | GPT-4-Turbo-2024-04-09              | 0.7500      |       | 0.750 |       |      |       |
| 25   | OpenAI      | gpt-5.2-2025-12-11                  | 0.7342      | 0.734 |       |       |      |       |
| 26   | OpenAI      | gpt-5-2-codex                       | 0.7253      | 0.772 |       | 0.632 |      |       |
| 27   | OpenAI      | openai/gpt-5-2025-08-07             | 0.7215      | 0.722 |       |       |      |       |
| 28   | Anthropic   | claude-sonnet-4-20250514            | 0.7122      | 0.937 |       | 0.263 |      |       |
| 29   | Google      | gemini-2.5-pro                      | 0.7111      | 0.646 |       | 0.842 |      |       |
| 30   | OpenAI      | gpt-4o                              | 0.6962      | 0.696 |       |       |      |       |
| 31   | Alibaba     | Qwen3.5-397B-A17B                   | 0.6667      |       |       |       |      | 0.667 |
| 32   | MiniMax     | minimax-m2.5                        | 0.6609      | 0.886 |       | 0.211 |      |       |
| 33   | Moonshot AI | Kimi-K2.5                           | 0.6326      | 0.658 |       |       |      | 0.556 |
| 34   | Moonshot AI | kimi-k2-0905-preview                | 0.6311      | 0.684 |       | 0.526 |      |       |
| 35   | OpenAI      | O3 (High)                           | 0.6250      |       | 0.625 |       |      |       |
| 36   | Alibaba     | Qwen/Qwen3-Coder-480B-A35B-Instruct | 0.6203      | 0.620 |       |       |      |       |
| 37   | Google      | gemini-3-pro                        | 0.6076      | 0.608 |       |       |      |       |
| 38   | Zhipu AI    | GLM-4.7                             | 0.6070      |       |       | 0.789 |      | 0.333 |
| 39   | MiniMax     | minimax-2.5                         | 0.5949      | 0.595 |       |       |      |       |
| 40   | OpenAI      | gpt-4.1-2025-04-14                  | 0.5876      | 0.671 |       | 0.421 |      |       |
| 41   | Meta        | meta-llama/Llama-3.3-70B-Instruct   | 0.5823      | 0.582 |       |       |      |       |
| 42   | Zhipu AI    | zai-org/GLM-4.6                     | 0.5696      | 0.570 |       |       |      |       |
| 43   | Anthropic   | claude-3-7-sonnet-20250219          | 0.5443      | 0.544 |       |       |      |       |
| 44   | OpenAI      | GPT-4O-2024-08-06                   | 0.5400      | 0.392 | 0.688 |       |      |       |
| 45   | OpenAI      | gpt-5.1-codex                       | 0.5390      | 0.519 |       | 0.579 |      |       |
| 46   | OpenAI      | gpt-5.1-2025-11-13                  | 0.5316      | 0.532 |       |       |      |       |
| 47   | Anthropic   | claude-haiku-4-5-20251001           | 0.5292      | 0.557 |       | 0.474 |      |       |
| 48   | Anthropic   | Claude-3.5-Sonnet-20241022          | 0.5154      | 0.468 | 0.562 |       |      |       |
| 49   | Moonshot AI | moonshot/kimi-k2-0711-preview       | 0.5063      | 0.506 |       |       |      |       |
| 50   | DeepSeek    | DeepSeek-V3.2                       | 0.5025      | 0.633 |       |       |      | 0.111 |
| 51   | DeepSeek    | DeepSeek-V3                         | 0.5012      | 0.190 | 0.812 |       |      |       |
| 52   | Anthropic   | Claude-3-Haiku                      | 0.5000      |       | 0.500 |       |      |       |
| 53   | OpenAI      | o3-2025-04-16                       | 0.4981      | 0.405 |       | 0.684 |      |       |
| 54   | OpenAI      | o1-preview                          | 0.4937      | 0.494 |       |       |      |       |
| 55   | Zhipu AI    | zai-org/GLM-4.5                     | 0.4810      | 0.481 |       |       |      |       |
| 56   | DeepSeek    | DeepSeek-V3.2-Speciale              | 0.4444      |       |       |       |      | 0.444 |
| 57   | Anthropic   | Claude-Sonnet-4 (Thinking)          | 0.4375      |       | 0.438 |       |      |       |
| 58   | DeepSeek    | deepseek-v3.2-reasoner              | 0.4304      | 0.430 |       |       |      |       |
| 59   | Unknown     | agentica-org/DeepSWE-Preview        | 0.4177      | 0.418 |       |       |      |       |
| 60   | Anthropic   | Claude-Opus-4 (Thinking)            | 0.3750      |       | 0.375 |       |      |       |
| 61   | Zhipu AI    | glm-4.6                             | 0.3671      | 0.367 |       |       |      |       |
| 62   | Zhipu AI    | GLM-4.5                             | 0.3544      | 0.354 |       |       |      |       |
| 63   | Mistral     | devstral-2512                       | 0.3418      | 0.342 |       |       |      |       |
| 64   | Moonshot AI | Kimi-K2-Thinking                    | 0.3418      | 0.456 |       |       |      | 0.000 |
| 65   | Moonshot AI | Kimi-K2-Instruct                    | 0.3291      | 0.329 |       |       |      |       |
| 66   | Google      | gemini-2.5-pro-preview-05-06        | 0.3165      | 0.316 |       |       |      |       |
| 67   | Anthropic   | Claude-Opus-4                       | 0.3125      |       | 0.312 |       |      |       |
| 68   | Alibaba     | Qwen3-Coder-480B-A35B-Instruct      | 0.3058      | 0.380 |       | 0.158 |      |       |
| 69   | DeepSeek    | deepseek-reasoner                   | 0.3038      | 0.304 |       |       |      |       |
| 70   | MiniMax     | minimax-m2                          | 0.2954      | 0.443 |       | 0.000 |      |       |
| 71   | Google      | gemini-2.0-flash-exp                | 0.2911      | 0.291 |       |       |      |       |
| 72   | Amazon      | amazon.nova-premier-v1:0            | 0.2785      | 0.278 |       |       |      |       |
| 73   | StepFun     | Step-3.5-Flash                      | 0.2784      |       |       | 0.316 |      | 0.222 |
| 74   | DeepSeek    | DeepSeek-V3-0324                    | 0.2658      | 0.266 |       |       |      |       |
| 75   | Anthropic   | claude-3.5-sonnet-latest            | 0.2532      | 0.253 |       |       |      |       |
| 76   | Anthropic   | Claude-Sonnet-4                     | 0.2500      |       | 0.250 |       |      |       |
| 77   | Meta        | Llama3-SWE-RL-70B                   | 0.2405      | 0.241 |       |       |      |       |
| 78   | Anthropic   | claude-3-haiku-20240307             | 0.2278      | 0.228 |       |       |      |       |
| 79   | Google      | gemini-2.5-flash                    | 0.2156      | 0.139 |       | 0.368 |      |       |
| 80   | Alibaba     | Qwen 2.5                            | 0.2152      | 0.215 |       |       |      |       |
| 81   | OpenAI      | gpt-4o-2024-05-13                   | 0.2025      | 0.203 |       |       |      |       |
| 82   | Google      | Gemini-2.5-Pro-05-06                | 0.1875      |       | 0.188 |       |      |       |
| 83   | Anthropic   | claude-4-sonnet                     | 0.1772      | 0.177 |       |       |      |       |
| 84   | OpenAI      | gpt-5-nano-2025-08-07               | 0.1646      | 0.165 |       |       |      |       |
| 85   | DeepSeek    | deepseek-chat                       | 0.1519      | 0.152 |       |       |      |       |
| 86   | OpenAI      | gpt-4-1106-preview                  | 0.1266      | 0.127 |       |       |      |       |
| 87   | Google      | Gemini-2.5-Flash-05-20              | 0.1250      |       | 0.125 |       |      |       |
| 88   | OpenAI      | gpt-4-0613                          | 0.1013      | 0.101 |       |       |      |       |
| 89   | OpenAI      | gpt-oss-120b                        | 0.0935      | 0.114 |       | 0.053 |      |       |
| 90   | OpenAI      | gpt-4o-20241120                     | 0.0886      | 0.089 |       |       |      |       |
| 91   | Alibaba     | Qwen3-235B-A22B                     | 0.0768      |       | 0.062 | 0.105 |      |       |
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
