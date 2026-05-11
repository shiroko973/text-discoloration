# Changelog

## [2.7.0] - 2026-05-09

### Added
-  新增 `b64_encode()` Base64 编码（支持字符串/字节自动识别）
-  新增 `b64_decode()` Base64 解码（支持文本/字节模式）
-  新增 `b64_encode_file()` 任意文件转 Base64
-  新增 `b64_decode_to_file()` Base64 还原为文件

### Changed
-  优化代码结构，保持零依赖

## [2.6.1] - 2026-05-08

### Added
-  新增 Base64 编码解码功能（初始版本）

## [2.6.0] - 2026-05-07

### Added
-  新增 `hash_text()` / `hash_file()` 哈希计算
-  新增 `Logger` 日志类
-  新增文件操作函数：`read_file`, `write_file`, `create_file`, `append_file`, `edit_file`

### Fixed
-  修复 `_typewriter_color_factory` 中 `__name__` 缺失的问题

## [2.5.0] - 2026-05-06

### Added
-  新增 `Live` 类和 `live()` 实时刷新
-  新增 `highlight()` 关键词高亮

## [2.4.0] - 2026-05-05

### Added
-  新增 `table()` 表格打印
-  新增 `tree()` 树形结构

## [2.3.5] - 2026-05-05

### Added
-  二进制相关功能：`binary_text`, `text_to_binary`, `binary_exec` 等

## [2.3.0] - 2026-05-04

### Added
-  进度条、标题框、分隔线、加载动画、列表项
-  渐变文字、彩虹文字

## [2.2.0] - 2026-05-04

### Added
-  全局开关 `enable()` / `disable()`
-  强制彩色 `force_color()`
-  自动 TTY 检测

## [2.1.0] - 2026-05-04

### Added
-  渐变文字 `gradient_text()`
-  彩虹文字 `rainbow_text()`
-  二进制输出 `binary_output()`

## [2.0.0] - 2026-05-03

### Added
-  新增状态提示函数
-  Windows ANSI 支持改用 ctypes