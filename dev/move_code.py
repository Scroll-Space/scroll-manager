#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import shutil
from pathlib import Path
from typing import Set, List

# Список папок и файлов для игнорирования при копировании
EXCLUDE_PATTERNS: Set[str] = {
    ".git",
    ".gitmodules",
    ".idea",
    ".vscode",
    "/docs",
    "/dev",
    "__pycache__",    
    ".DS_Store",
    "*.pyc",
    "*.free"
}

def should_exclude(rel_path: Path) -> bool:
    """
    Проверяет, нужно ли пропустить элемент.
    
    - Если паттерн начинается с '/', проверяем относительный путь с ведущим слешем (только от корня).
    - В противном случае проверяем соответствие на любой глубине.
    """
    # Приводим путь к POSIX-формату (например, "src/main.py")
    posix_path: str = rel_path.as_posix()
    
    # Путь с ведущим слешем для точной проверки корня (например, "/automation")
    root_posix_path: str = f"/{posix_path}"

    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith("/"):
            # Проверка от КОРНЯ: совпадает ли путь целиком или с папкой в корне (напр. /automation/...)
            if root_posix_path == pattern or root_posix_path.startswith(f"{pattern}/"):
                return True
        else:
            # Проверка на ЛЮБОЙ глубине (для __pycache__, *.pyc и т.д.)
            if rel_path.match(pattern):
                return True

    return False

def main():
    parser = argparse.ArgumentParser(
        description="Копирование файлов плагина в репозиторий ONLYOFFICE."
    )
    parser.add_argument(
        "dest_repo",
        type=str,
        help="Путь к корню репозитория onlyoffice.github.io",
    )

    args: argparse.Namespace = parser.parse_args()

    # 1. Определяем корень текущего проекта через рабочую директорию (CWD)
    source_dir: Path = Path.cwd().resolve()

    # Имя текущей директории плагина
    plugin_name: str = source_dir.name

    # 2. Преобразуем входящую строку в объект Path и проверяем его
    target_repo: Path = Path(args.dest_repo).resolve()
    if not target_repo.exists() or not target_repo.is_dir():
        print(f"Ошибка: Директория назначения '{target_repo}' не существует.")
        sys.exit(1)

    # Целевая папка плагина в репозитории ONLYOFFICE
    target_plugin_dir: Path = (target_repo /
                               "sdkjs-plugins" /
                               "content" /
                               plugin_name)

    print(f"Источник (рабочая директория): {source_dir}")
    print(f"Название плагина:             {plugin_name}")
    print(f"Назначение:                   {target_plugin_dir}\n")

    # 3. Очищаем целевую папку перед копированием, если она уже существует
    if target_plugin_dir.exists():
        shutil.rmtree(target_plugin_dir)

    target_plugin_dir.mkdir(parents=True, exist_ok=True)

    copied_count: int = 0

    # 3. Обход через os.walk
    root: str
    dirs: List[str]
    files: List[str]
    for root, dirs, files in os.walk(source_dir):
        current_dir: Path = Path(root)

        # Модифицируем dirs in-place (dirs[:]): os.walk сразу пропустит исключенные папки
        dirs[:] = [
            d
            for d in dirs
            if not should_exclude((current_dir / d).relative_to(source_dir))
        ]

        # Обрабатываем файлы в текущей разрешённой директории
        for file_name in files:
            src_file: Path = current_dir / file_name
            rel_file: Path = src_file.relative_to(source_dir)

            if should_exclude(rel_file):
                continue

            dest_file: Path = target_plugin_dir / rel_file

            # Создаем структуру подпапок и копируем файл
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dest_file)

            copied_count += 1

    print(f"\nУспешно скопировано файлов: {copied_count}")


if __name__ == "__main__":
    main()
