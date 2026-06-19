# UAV Weather-Aware 4D Risk Planning

本工程用于低空气象约束下多旋翼无人机四维概率风险场建模、动态全局路径规划与中期/论文实验验证。

## 目录结构

- `uav_weather_planning/`：正式 Python 源码包。
- `configs/`：风险阈值、融合权重、多尺度网格等配置。
- `data/`：真实天气回放案例、缓存索引和可复现实验数据。
- `results/`：精选展示结果和后续默认实验输出。
- `outputs/`：历史实验输出，保留用于追溯，不再作为默认输出目录。
- `docs/`：研究说明、阶段笔记和源方案文档。
- `scripts/`：辅助脚本；旧脚本位于 `scripts/legacy/`。
- `archive/`：本次整理归档的旧输出、旧数据、临时结果和清理清单。

## 常用入口

统一入口：

```powershell
python run_project.py simulated
python run_project.py multi-real
python run_project.py benchmark
python run_project.py incremental
```

旧模块入口仍然兼容，例如：

```powershell
python -m uav_weather_planning.experiments.paper_10km_weather_risk_demo --help
python -m uav_weather_planning.experiments.benchmark_suite --help
```

## 实验模块分组

`uav_weather_planning/experiments/` 已按用途分组：

- `midterm/`：中期演示。
- `real_replay/`：真实天气回放和案例构建。
- `benchmarks/`：基准、消融、校准和敏感性实验。
- `paper_10km/`：10 km 论文级 4D 风险场与 D* Lite 实验。
- `smoke/`：快速 smoke 验证。
- `utils/`：实验共享工具。

根层旧实验模块文件是兼容 wrapper，不再承载真实实现。

## 清理记录

本次目录整理的移动清单位于：

```text
archive/cleanup_manifest.json
```

如需回滚，可根据该清单将归档文件移动回原路径。

