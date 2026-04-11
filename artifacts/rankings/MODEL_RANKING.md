# 模型能力榜单（自动生成）

- 生成时间（UTC）：2026-04-11T12:45:54+00:00
- 说明：按 5 个榜单（代码优先）做分位数标准化后加权平均；缺失榜单不计入分母。
- 权重：SWE-bench 0.30、LiveCodeBench 0.30、Arena 0.15、HELM 0.15、OpenCompass 0.10。
- 过滤规则（Top3 输出用）：排除 distill/quant/int4/int8/gguf/awq/gptq 以及 mini/small/lite/tiny 等小模型。

## 全局排名
| Rank | Provider    | Model                               | Score(0..1) | SWE   | LCB | Arena | HELM | OC    |
| ---- | ----------- | ----------------------------------- | ----------- | ----- | --- | ----- | ---- | ----- |
| 1    | Anthropic   | claude-opus-4-5                     | 0.9873      | 0.987 |     |       |      |       |
| 2    | ByteDance   | Doubao-Seed-1.6                     | 0.9747      | 0.975 |     |       |      |       |
| 3    | Google      | Gemini-3-Pro-Preview                | 0.9715      | 0.962 |     |       |      | 1.000 |
| 4    | Anthropic   | claude-4-5-opus                     | 0.9494      | 0.949 |     |       |      |       |
| 5    | Anthropic   | claude-opus-4-5-20251101            | 0.9444      | 1.000 |     | 0.833 |      |       |
| 6    | OpenAI      | gpt-5                               | 0.9367      | 0.937 |     |       |      |       |
| 7    | Anthropic   | claude-opus-4-6                     | 0.9156      | 0.873 |     | 1.000 |      |       |
| 8    | Google      | gemini-2.5-pro-06-17                | 0.9114      | 0.911 |     |       |      |       |
| 9    | Google      | gemini-3-flash-preview              | 0.8987      | 0.899 |     |       |      |       |
| 10   | Google      | gemini-2.5-pro-preview-06-05        | 0.8608      | 0.861 |     |       |      |       |
| 11   | Anthropic   | claude-sonnet-4-5                   | 0.8481      | 0.848 |     |       |      |       |
| 12   | Anthropic   | claude-4-sonnet-20250514            | 0.8354      | 0.835 |     |       |      |       |
| 13   | OpenAI      | gpt-4.1                             | 0.8228      | 0.823 |     |       |      |       |
| 14   | OpenAI      | gpt-5-2025-08-07                    | 0.8101      | 0.810 |     |       |      |       |
| 15   | Zhipu AI    | GLM-5                               | 0.7987      | 0.772 |     | 0.792 |      | 0.889 |
| 16   | Anthropic   | claude-4-opus-20250514              | 0.7975      | 0.797 |     |       |      |       |
| 17   | Google      | gemini-3-flash                      | 0.7896      | 0.747 |     | 0.875 |      |       |
| 18   | OpenAI      | GPT-5-2025-08-07 (high)             | 0.7778      |       |     |       |      | 0.778 |
| 19   | OpenAI      | gpt-5-2-codex                       | 0.7454      | 0.785 |     | 0.667 |      |       |
| 20   | OpenAI      | gpt-5.2-2025-12-11                  | 0.7342      | 0.734 |     |       |      |       |
| 21   | Google      | gemini-3-pro                        | 0.7245      | 0.608 |     | 0.958 |      |       |
| 22   | Anthropic   | claude-sonnet-4-5-20250929          | 0.7226      | 0.709 |     | 0.750 |      |       |
| 23   | OpenAI      | openai/gpt-5-2025-08-07             | 0.7215      | 0.722 |     |       |      |       |
| 24   | OpenAI      | gpt-5-2                             | 0.7008      | 0.759 |     | 0.583 |      |       |
| 25   | OpenAI      | gpt-4o                              | 0.6962      | 0.696 |     |       |      |       |
| 26   | MiniMax     | minimax-m2.5                        | 0.6879      | 0.886 |     | 0.292 |      |       |
| 27   | Anthropic   | claude-sonnet-4-20250514            | 0.6855      | 0.924 |     | 0.208 |      |       |
| 28   | Zhipu AI    | GLM-4.7                             | 0.6833      |       |     | 0.917 |      | 0.333 |
| 29   | Alibaba     | Qwen3.5-397B-A17B                   | 0.6667      |       |     |       |      | 0.667 |
| 30   | Google      | gemini-2.5-pro                      | 0.6665      | 0.646 |     | 0.708 |      |       |
| 31   | Moonshot AI | Kimi-K2.5                           | 0.6326      | 0.658 |     |       |      | 0.556 |
| 32   | Alibaba     | Qwen/Qwen3-Coder-480B-A35B-Instruct | 0.6203      | 0.620 |     |       |      |       |
| 33   | Moonshot AI | kimi-k2-0905-preview                | 0.6085      | 0.684 |     | 0.458 |      |       |
| 34   | MiniMax     | minimax-2.5                         | 0.5949      | 0.595 |     |       |      |       |
| 35   | OpenAI      | gpt-4.1-2025-04-14                  | 0.5861      | 0.671 |     | 0.417 |      |       |
| 36   | Meta        | meta-llama/Llama-3.3-70B-Instruct   | 0.5823      | 0.582 |     |       |      |       |
| 37   | Zhipu AI    | zai-org/GLM-4.6                     | 0.5696      | 0.570 |     |       |      |       |
| 38   | OpenAI      | gpt-5.1-codex                       | 0.5628      | 0.532 |     | 0.625 |      |       |
| 39   | OpenAI      | gpt-5.1-2025-11-13                  | 0.5190      | 0.519 |     |       |      |       |
| 40   | Moonshot AI | moonshot/kimi-k2-0711-preview       | 0.5063      | 0.506 |     |       |      |       |
| 41   | DeepSeek    | DeepSeek-V3.2                       | 0.5018      | 0.633 |     | 0.500 |      | 0.111 |
| 42   | OpenAI      | o1-preview                          | 0.4937      | 0.494 |     |       |      |       |
| 43   | Anthropic   | claude-haiku-4-5-20251001           | 0.4824      | 0.557 |     | 0.333 |      |       |
| 44   | Zhipu AI    | zai-org/GLM-4.5                     | 0.4810      | 0.481 |     |       |      |       |
| 45   | OpenAI      | o3-2025-04-16                       | 0.4506      | 0.405 |     | 0.542 |      |       |
| 46   | DeepSeek    | DeepSeek-V3.2-Speciale              | 0.4444      |       |     |       |      | 0.444 |
| 47   | DeepSeek    | deepseek-v3.2-reasoner              | 0.4304      | 0.430 |     |       |      |       |
| 48   | Unknown     | agentica-org/DeepSWE-Preview        | 0.4177      | 0.418 |     |       |      |       |
| 49   | OpenAI      | gpt-4o-2024-08-06                   | 0.3924      | 0.392 |     |       |      |       |
| 50   | Anthropic   | claude-3-7-sonnet-20250219          | 0.3906      | 0.544 |     | 0.083 |      |       |
| 51   | Zhipu AI    | glm-4.6                             | 0.3671      | 0.367 |     |       |      |       |
| 52   | Zhipu AI    | GLM-4.5                             | 0.3544      | 0.354 |     |       |      |       |
| 53   | Moonshot AI | Kimi-K2-Thinking                    | 0.3513      | 0.468 |     |       |      | 0.000 |
| 54   | Anthropic   | claude-3-5-sonnet-20241022          | 0.3455      | 0.456 |     | 0.125 |      |       |
| 55   | Mistral     | devstral-2512                       | 0.3418      | 0.342 |     |       |      |       |
| 56   | Moonshot AI | Kimi-K2-Instruct                    | 0.3291      | 0.329 |     |       |      |       |
| 57   | Google      | gemini-2.5-pro-preview-05-06        | 0.3165      | 0.316 |     |       |      |       |
| 58   | Alibaba     | Qwen3-Coder-480B-A35B-Instruct      | 0.3087      | 0.380 |     | 0.167 |      |       |
| 59   | DeepSeek    | deepseek-reasoner                   | 0.3038      | 0.304 |     |       |      |       |
| 60   | MiniMax     | minimax-m2                          | 0.2954      | 0.443 |     | 0.000 |      |       |
| 61   | Google      | gemini-2.0-flash-exp                | 0.2911      | 0.291 |     |       |      |       |
| 62   | Amazon      | amazon.nova-premier-v1:0            | 0.2785      | 0.278 |     |       |      |       |
| 63   | DeepSeek    | DeepSeek-V3-0324                    | 0.2658      | 0.266 |     |       |      |       |
| 64   | Anthropic   | claude-3.5-sonnet-latest            | 0.2532      | 0.253 |     |       |      |       |
| 65   | Meta        | Llama3-SWE-RL-70B                   | 0.2405      | 0.241 |     |       |      |       |
| 66   | StepFun     | Step-3.5-Flash                      | 0.2389      |       |     | 0.250 |      | 0.222 |
| 67   | Alibaba     | Qwen 2.5                            | 0.2278      | 0.228 |     |       |      |       |
| 68   | Google      | gemini-2.5-flash                    | 0.2178      | 0.139 |     | 0.375 |      |       |
| 69   | Anthropic   | claude-3-haiku-20240307             | 0.2152      | 0.215 |     |       |      |       |
| 70   | OpenAI      | gpt-4o-2024-05-13                   | 0.2025      | 0.203 |     |       |      |       |
| 71   | DeepSeek    | deepseek-v3                         | 0.1899      | 0.190 |     |       |      |       |
| 72   | Anthropic   | claude-4-sonnet                     | 0.1772      | 0.177 |     |       |      |       |
| 73   | OpenAI      | gpt-5-nano-2025-08-07               | 0.1646      | 0.165 |     |       |      |       |
| 74   | DeepSeek    | deepseek-chat                       | 0.1519      | 0.152 |     |       |      |       |
| 75   | OpenAI      | gpt-4-1106-preview                  | 0.1266      | 0.127 |     |       |      |       |
| 76   | OpenAI      | gpt-4-0613                          | 0.1013      | 0.101 |     |       |      |       |
| 77   | OpenAI      | gpt-oss-120b                        | 0.0898      | 0.114 |     | 0.042 |      |       |
| 78   | OpenAI      | gpt-4o-20241120                     | 0.0886      | 0.089 |     |       |      |       |
| 79   | Meta        | llama-4-maverick-instruct           | 0.0759      | 0.076 |     |       |      |       |
| 80   | OpenAI      | gpt-4-0125-preview                  | 0.0633      | 0.063 |     |       |      |       |
| 81   | Anthropic   | claude-3-opus-20240229              | 0.0506      | 0.051 |     |       |      |       |
| 82   | Google      | gemini-2.0-flash                    | 0.0380      | 0.038 |     |       |      |       |
| 83   | Meta        | llama-4-scout-instruct              | 0.0253      | 0.025 |     |       |      |       |
| 84   | Anthropic   | claude-2                            | 0.0127      | 0.013 |     |       |      |       |
| 85   | Unknown     | SWE-Llama                           | 0.0000      | 0.000 |     |       |      |       |

## 抓取/解析告警

- source livecodebench: failed: URLError: <urlopen error [Errno 2] No such file or directory>

## 数据源

- LiveCodeBench: https://livecodebench.github.io/
- SWE-bench: https://www.swebench.com/
- Arena: https://lmarena.ai/leaderboard
- HELM: https://crfm.stanford.edu/helm/latest/
- OpenCompass Rank: https://rank.opencompass.org.cn/
