#!/usr/bin/env python3
"""使用本机 IntelliJ IDEA SDK 离线编译和打包插件。"""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--idea-home", required=True, type=Path,
                        help="IDEA Contents 目录，或包含 lib 目录的 IDEA 安装目录")
    parser.add_argument("--jdk-home", type=Path,
                        help="包含 bin/javac 的 JDK 21 或更高版本目录")
    parser.add_argument("--output", type=Path,
                        default=root / "dist" / "idea-code-location-copy-1.0.5.zip")
    parser.add_argument("--build-dir", type=Path, default=root / "build")
    args = parser.parse_args()

    idea_home = args.idea_home.expanduser().resolve()
    if (idea_home / "Contents" / "lib").is_dir():
        idea_home = idea_home / "Contents"
    if not (idea_home / "lib" / "annotations.jar").is_file():
        parser.error("IDEA 安装目录无效：缺少 lib/annotations.jar")
    product_files = [idea_home / "Resources" / "product-info.json", idea_home / "product-info.json"]
    product_file = next((path for path in product_files if path.is_file()), None)
    if product_file:
        info = json.loads(product_file.read_text(encoding="utf-8"))
        if int(info["buildNumber"].split(".")[0]) < 261:
            parser.error("此工程需要 IntelliJ Platform 261（IDEA 2026.1）或更高版本的 SDK")

    executable = "javac.exe" if os.name == "nt" else "javac"
    if args.jdk_home:
        javac = args.jdk_home.expanduser().resolve() / "bin" / executable
    else:
        bundled = [idea_home / "jbr" / "Contents" / "Home", idea_home / "jbr"]
        javac = next((home / "bin" / executable for home in bundled
                      if (home / "bin" / executable).is_file()), None)
        if javac is None:
            javac = shutil.which(executable)
    if javac is None or not Path(javac).is_file():
        parser.error("找不到 javac，请用 --jdk-home 指定 JDK 21 或更高版本")

    build_dir = args.build_dir.expanduser().resolve()
    build_dir.mkdir(parents=True, exist_ok=True)
    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    sources = sorted((root / "src" / "main" / "java").rglob("*.java"))
    with tempfile.TemporaryDirectory(prefix="compile-", dir=build_dir) as scratch:
        classes = Path(scratch) / "classes"
        classes.mkdir()
        subprocess.run([
            str(javac), "--release", "21", "-encoding", "UTF-8", "-proc:none",
            "-classpath", str(idea_home / "lib" / "*"), "-d", str(classes),
            *map(str, sources),
        ], check=True)
        jar_path = Path(scratch) / "idea-code-location-copy.jar"
        with zipfile.ZipFile(jar_path, "w", zipfile.ZIP_DEFLATED) as jar:
            for path in sorted(classes.rglob("*.class")):
                jar.write(path, path.relative_to(classes).as_posix())
            resources = root / "src" / "main" / "resources"
            for path in sorted(resources.rglob("*")):
                if path.is_file():
                    jar.write(path, path.relative_to(resources).as_posix())
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as plugin:
            plugin.write(jar_path, "idea-code-location-copy/lib/idea-code-location-copy.jar")
    print("编译完成，安装包：" + str(output))


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        sys.exit(error.returncode)
