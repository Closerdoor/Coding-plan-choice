# rankings

本目录实现“模型能力榜单”支线模块：从多个第三方榜单抓取数据，聚合生成全局模型能力榜单，并为每个模型原厂（Provider）生成 Top3 清单。

## 产物

产物固定生成到 `rankings/output/`：
- `MODEL_RANKING.md`：全局榜单（markdown）
- `MODEL_SCORES.json`：结构化分数明细（供其它模块读取）
- `MODEL_TOP3.md`：按 Provider 分组的 Top3（markdown）

## 运行方式

- 一键更新（会触网抓取榜单）：`python -m rankings.update`
- 单元测试（不触网）：`python -m unittest rankings.UTtest.test_rankings`

## 数据源

实现位于 `rankings/sources/`，每个榜单一个模块，统一暴露 `fetch()`：
- `livecodebench.py`
- `swebench.py`
- `arena.py`
- `opencompass.py`
- `helm.py`（占位，当前返回空）

数据源注册表：`rankings/sources/__init__.py` 的 `SOURCES = [...]`。

## 聚合口径（简述）

- 各源内部按名次映射为 `0..1` 的 unit score，再按权重加权平均。
- 缺失源不计入分母。
- 过滤规则对所有源与所有输出统一生效：剔除蒸馏/量化/小号模型，以及可解析参数量 `<70B` 的模型。
- Arena 噪声门控：只保留同时在至少一个非 Arena 源出现过的 Arena 模型。
- Provider 归属：优先从模型名推断；源提供的 org/provider 字段仅在白名单内才作为兜底，避免把提交团队/聚合商当作 Provider。

细节见 `rankings/大模型能力榜单需求文档.md` 与 `rankings/core.py`。

## 在项目中的作用（给主线使用）

主线 catalog 在渲染“支持模型”时，可读取 `rankings/output/MODEL_SCORES.json`：
- 生成 `provider -> Top3` 映射
- 将“官方解析到的可用模型列表”与 Top3 做交集过滤
- 若交集为空则退化为展示官方列表

## 自动化

GitHub Actions：`.github/workflows/update-model-rankings.yml`
- 定时运行 + 支持手动触发
- 产物变更自动创建 PR（仅包含 `rankings/output/` 三件套）
