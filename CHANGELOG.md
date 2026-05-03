# Changelog

## [1.1.0] - 2026-05-03

### Added
- 新增状态提示函数：`info()`, `success()`, `error()`, `warn()`
- 新增单色直接打印系列：`color_print_red()`, `color_print_green()`, ... 共8个
- 新增黑色文字支持（`BLACK` / `color_print_black` / `typewriter_black`）
- 补回随机彩色打字机 `random_typewriter()`

### Changed
- Windows ANSI 颜色支持改用 `ctypes.SetConsoleMode()`，不再修改注册表
- 颜色代码改为全局常量（`RED`, `GREEN`, ...），提升性能
- `color_typewriter()` 改用 `globals().get()` 动态获取颜色

### Fixed
- 移除注册表写入操作，避免永久修改用户系统设置

## [1.0.1] - 2026-05-02

### Added
- 初始发布
- 打字机效果 `typewriter()`
- 彩色打字机 `color_typewriter()`
- 分颜色打字机函数（red/green/yellow/blue/purple/cyan/white）
- 单色打印函数
- 慢速打印 `slow_print()`
- Windows ANSI 颜色支持（第一版，使用注册表方式）