from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable


ExperimentRunner = Callable[[str | Path], dict[str, Any]]


def _run_simulated(output_dir: str | Path) -> dict[str, Any]:
    from uav_weather_planning.experiments.midterm_simulated_risk_demo import run_simulated_risk_demo

    return run_simulated_risk_demo(output_dir)


def _run_realdata(output_dir: str | Path) -> dict[str, Any]:
    from uav_weather_planning.experiments.historical_weather_replay import run_historical_weather_replay

    return run_historical_weather_replay(output_dir)


def _run_multi_real(output_dir: str | Path) -> dict[str, Any]:
    from uav_weather_planning.experiments.multi_time_real_weather_replay import run_multi_time_real_weather_replay

    case_dir = Path("data/replay_cases/case_001_wind_precip")
    if list(case_dir.glob("weather_*.npz")):
        return run_multi_time_real_weather_replay(output_dir, case_dir=case_dir, allow_nowcast_fallback=False)
    return run_multi_time_real_weather_replay(output_dir, allow_nowcast_fallback=True)


def _run_multi_case_real(output_dir: str | Path) -> dict[str, Any]:
    from uav_weather_planning.experiments.multi_case_real_weather_replay import run_multi_case_real_weather_replay

    return run_multi_case_real_weather_replay(output_dir)


def _run_benchmark(output_dir: str | Path) -> dict[str, Any]:
    from uav_weather_planning.experiments.benchmark_suite import run_benchmark_suite

    return run_benchmark_suite(output_dir)


def _run_ablation(output_dir: str | Path) -> dict[str, Any]:
    from uav_weather_planning.experiments.ablation_study import run_ablation_study

    return run_ablation_study(output_dir)


def _run_incremental(output_dir: str | Path) -> dict[str, Any]:
    from uav_weather_planning.experiments.incremental_search_validation import run_incremental_search_validation

    return run_incremental_search_validation(output_dir)


def _run_trajectory(output_dir: str | Path) -> dict[str, Any]:
    from uav_weather_planning.experiments.trajectory_control_smoke import run_trajectory_control_smoke

    return run_trajectory_control_smoke(output_dir)


def _run_calibration(output_dir: str | Path) -> dict[str, Any]:
    from uav_weather_planning.experiments.risk_calibration_evidence import run_risk_calibration_evidence

    return run_risk_calibration_evidence(output_dir)


def _run_risk_search(output_dir: str | Path) -> dict[str, Any]:
    from uav_weather_planning.risk_calibration.weight_search import WeightSearchConfig, run_weight_search

    return run_weight_search(output_dir, WeightSearchConfig(sample_count=50, case_count=30))


def _run_sensitivity(output_dir: str | Path) -> dict[str, Any]:
    from uav_weather_planning.experiments.risk_weight_sensitivity import SensitivityConfig, run_risk_weight_sensitivity

    return run_risk_weight_sensitivity(output_dir, SensitivityConfig(case_count=27))


RUNNERS: dict[str, tuple[ExperimentRunner, str]] = {
    "simulated": (_run_simulated, "合成动态气象风险场演示"),
    "realdata": (_run_realdata, "本地真实天气回放闭环验证"),
    "multi-real": (_run_multi_real, "多时刻真实气象序列动态回放"),
    "multi-case-real": (_run_multi_case_real, "多真实历史天气过程批量回放"),
    "benchmark": (_run_benchmark, "参数化统计基准实验"),
    "ablation": (_run_ablation, "风险建模与规划模块消融实验"),
    "incremental": (_run_incremental, "LPA*/D* Lite 同族增量搜索验证"),
    "trajectory": (_run_trajectory, "B-spline 轨迹层与 NMPC 接口 smoke 测试"),
    "calibration": (_run_calibration, "风险校准与证据链实验"),
    "risk-search": (_run_risk_search, "风险融合权重代理标签搜索"),
    "sensitivity": (_run_sensitivity, "风险权重和阈值敏感性实验"),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Unified runner for the UAV weather-aware planning project.")
    parser.add_argument("experiment", choices=sorted(RUNNERS), help="Experiment or validation pipeline to run.")
    parser.add_argument("--output-dir", default=None, help="Output directory. Defaults to results/<experiment>.")
    args = parser.parse_args()

    runner, description = RUNNERS[args.experiment]
    output_dir = Path(args.output_dir or f"results/{args.experiment}")
    print(f"[Project] Running {args.experiment}: {description}")
    print(f"[Project] Output directory: {output_dir}")
    summary = runner(output_dir)
    compact = {
        "experiment": args.experiment,
        "output_dir": str(output_dir),
        "summary_keys": sorted(summary.keys())[:12],
    }
    print(json.dumps(compact, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
