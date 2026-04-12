# Catalog 执行与诊断说明

## 新增输出文件

- `catalog/output/CATALOG_DATA.json`
  - 最终结构化产物
- `catalog/output/CATALOG_PREFLIGHT.json`
  - 预检测结果
  - 用于确认各厂商官方页面和 source URL 在当前运行环境下是否网络可达
- `catalog/output/CATALOG_RUN.log`
  - 完整执行日志
  - 记录预检测、逐厂商抓取、失败堆栈、单厂商耗时、总耗时、产物写出等信息

## 预检测逻辑

- 在正式抓取前，对当前运行范围内厂商的 `official_url` 和 `source_urls` 执行可达性探测
- 若预检测失败，会在日志和 `CATALOG_PREFLIGHT.json` 中记录具体 URL 和错误原因
- 当前预检测结果不会直接进入 `CATALOG_DATA.json` 的 `warnings`
- `CATALOG_DATA.json` 的 `warnings` 仅表示真实抓取失败

## GitHub Actions 调试方式

每次执行后，可在 workflow 的 artifacts 中下载：

- `catalog-auto-diagnostics`
- `catalog-xfyun-manual-diagnostics`

重点查看：

1. `CATALOG_PREFLIGHT.json`
2. `CATALOG_RUN.log`

同时，这两个文件也会跟随 catalog 更新 PR 一起提交到仓库，便于直接在主分支回溯当次执行问题。

## PR 分支策略

- 自动更新 workflow 每次都会基于当前 `main` 创建新的唯一分支。
- 手动讯飞 workflow 也会基于当前 `main` 创建新的唯一分支。
- 这样可以避免复用旧的 automation 分支，导致历史失败产物再次进入新的 PR。

## 本地运行

```powershell
python -m catalog.preflight
python -m catalog.update
python -m unittest catalog.UTtest.selftest
```

执行完成后，到 `catalog/output/` 查看诊断文件。

说明：

- 每次新执行都会覆盖旧的 `CATALOG_PREFLIGHT.json` 和 `CATALOG_RUN.log`
- 当前只保留最近一次执行的诊断结果
