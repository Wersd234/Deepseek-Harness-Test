"""主文档 §11.1 curl 验证脚本的 Python 等价实现。

用法：.venv\\Scripts\\python scripts\\verify_ptv.py
从 .env 读取 PTV_API_BASE / PTV_DEVID / PTV_KEY，请求一次周边搜索接口，
打印返回的 route_type 列表；恰好 5 种即视为凭证有效（M0 验收标准）。

注意：PTV_API_BASE 的确切取值以主文档 §11.1 的 curl 脚本为准，
      拿到主文档后如有出入请同步修改本脚本的路径拼接。
"""
import os
import sys
import urllib.parse
import urllib.request

from dotenv import load_dotenv

load_dotenv()

API_BASE = os.getenv("PTV_API_BASE", "").rstrip("/")
DEVID = os.getenv("PTV_DEVID", "")
KEY = os.getenv("PTV_KEY", "")


def main() -> int:
    if not (API_BASE and DEVID and KEY):
        print("缺少 PTV_API_BASE / PTV_DEVID / PTV_KEY，请先在 .env 中填写（见 .env.example）")
        return 2

    url = f"{API_BASE}/geo/devid/{DEVID}/key/{KEY}/route/1/lat/52.52/lon/13.405/maxdist/2000"
    print(f"GET {url.replace(KEY, '***')}")
    req = urllib.request.Request(url, headers={"User-Agent": "ptvbot-m0-verify/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", "replace")
            print(f"HTTP {resp.status}, {len(body)} bytes")
    except Exception as exc:  # noqa: BLE001
        print(f"请求失败: {exc}")
        return 1

    route_types = sorted({p for p in body.split('"')[1::2] if p.isupper() and p.isalpha()})
    # 兜底：直接在全文里统计已知 5 种 route_type 关键字
    known = [t for t in ("TRAM", "BUS", "U-BAHN", "S-BAHN", "RAIL") if f'"{t}"' in body or t in body]
    print(f"检测到的 route_type: {route_types or known}")
    n = len(set(route_types) | set(known))
    if n == 5:
        print("✅ PTV 凭证有效：返回 5 种 route_type")
        return 0
    print(f"❌ 期望 5 种 route_type，实际 {n} 种——请核对主文档 §11.1 的 URL 与凭证")
    return 1


if __name__ == "__main__":
    sys.exit(main())
