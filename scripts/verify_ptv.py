"""主文档 §11.1：手动验证 PTV Timetable API 凭证（curl 的等价 Python 版）。

拿到 devid / key 后第一件事先跑这个，确认凭证可用再写代码。
用法：确保 .env 里填了 PTV_DEVID / PTV_KEY（PTV_API_BASE 默认官方地址），然后：
    .venv\\Scripts\\python.exe scripts\\verify_ptv.py
退出码 0 = 凭证有效（返回 5 种 route_type）。

签名方式（§11.1）：HMAC-SHA1(key, path含query、不含host)，十六进制，&signature= 附加在 URL 尾部。
"""
import hashlib
import hmac
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# 控制台可能是 GBK，强制 UTF-8 输出避免 UnicodeEncodeError
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DEVID = os.getenv("PTV_DEVID", "")
KEY = os.getenv("PTV_KEY", "")
API_BASE = (os.getenv("PTV_API_BASE") or "https://timetableapi.ptv.vic.gov.au").rstrip("/")


def sign(path_and_query: str) -> str:
    """§11.1: HMAC-SHA1(key, "/v3/...?devid=...") —— 只签 path+query，不含 host。"""
    return hmac.new(KEY.encode(), path_and_query.encode(), hashlib.sha1).hexdigest()


def main() -> int:
    if not DEVID or not KEY:
        print("❌ 未配置 PTV_DEVID / PTV_KEY —— 请在 .env 填入后重试")
        return 2
    pathq = f"/v3/route_types?devid={DEVID}"
    url = f"{API_BASE}{pathq}&signature={sign(pathq)}"
    print(f"GET {url.rsplit('signature=', 1)[0]}signature=***")
    req = urllib.request.Request(url, headers={"User-Agent": "ptvbot-m0/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            raw = resp.read().decode("utf-8", "errors=replace")
    except urllib.error.HTTPError as exc:
        # §11.1: 403 多半是签名串拼错（比如把 host 也签进去了）
        print(f"HTTP {exc.status}: {exc.read().decode('utf-8', errors='replace')[:500]}")
        print("❌ 凭证验证失败" + ("（403：检查签名串是否多签了 host）" if exc.status == 403 else ""))
        return 1

    data = json.loads(raw)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    route_types = data.get("route_types", [])
    names = [rt.get("route_type_name") for rt in route_types]
    if len(route_types) == 5:
        print(f"✅ 凭证有效：返回 5 种 route_type {names}")
        return 0
    print(f"❌ 预期 5 种 route_type，实际 {len(route_types)} 种")
    return 1


if __name__ == "__main__":
    sys.exit(main())
