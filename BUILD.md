# 如何使用 GitHub Actions 打包 APK

## 概述
本项目使用 GitHub Actions 自动化构建 Android APK。由于 python-for-android 不支持 Windows，我们使用 GitHub 的云端 Linux 环境进行打包。

## 前置要求
1. GitHub 账号
2. 本项目代码需要推送到 GitHub 仓库

## 使用步骤

### 1. 创建 GitHub 仓库
1. 访问 https://github.com/new
2. 创建一个新的仓库（例如：`errorquestion-app`）
3. 不要初始化 README，因为我们已经有了本地代码

### 2. 初始化本地 Git 仓库
在项目目录执行：
```bash
git init
git add .
git commit -m "Initial commit"
```

### 3. 关联远程仓库并推送
```bash
git remote add origin https://github.com/你的用户名/你的仓库名.git
git branch -M main
git push -u origin main
```

### 4. 触发构建
推送代码后，GitHub Actions 会自动开始构建。你也可以：
- 访问 `https://github.com/你的用户名/你的仓库名/actions` 查看构建进度
- 在 Actions 页面点击 "Build Android APK" -> "Run workflow" 手动触发构建

### 5. 下载 APK
构建完成后（约 10-30 分钟）：
1. 访问 Actions 页面
2. 点击最新的构建任务
3. 在 "Artifacts" 部分下载 `debug-apk`
4. 解压后即可获得 APK 文件

## 构建配置说明

### 自动触发
- 推送代码到 `main` 或 `master` 分支时自动构建
- 创建 Pull Request 时自动构建

### 手动触发
在 Actions 页面手动点击运行

### 构建产物
- Debug 版本的 APK 文件
- 保存 30 天后自动删除
- 如果打 tag 推送，会自动创建 Release

## 常见问题

### Q: 构建失败怎么办？
A: 查看 Actions 的构建日志，通常是因为：
- 依赖包版本冲突
- 代码语法错误
- buildozer.spec 配置问题
- 系统依赖包缺失

### Q: 如何修改构建配置？
A: 编辑 `.github/workflows/build-apk.yml` 文件

### Q: 如何构建正式版（release）？
A: 修改 workflow 文件，将 `buildozer android debug` 改为 `buildozer android release`

### Q: 构建需要多长时间？
A: 首次构建约 20-30 分钟，后续因为有缓存会快一些（10-15 分钟）

## 故障排除

### 构建失败：缺少系统依赖包

如果构建失败并提示缺少系统依赖包，请检查以下几点：

1. **查看构建日志**
   - 在 Actions 页面点击失败的构建任务
   - 查看详细的错误信息
   - 确认是哪个依赖包缺失

2. **已包含的系统依赖**
   当前配置已包含以下依赖包：
   - Java 17 (openjdk-17-jdk)
   - 构建工具 (build-essential, cmake, automake, libtool)
   - 图像库 (libjpeg-dev, libpng-dev, libfreetype6-dev)
   - GUI 库 (libcairo2-dev, libpango1.0-dev, libgtk-3-dev)
   - 数据库库 (libsqlite3-dev)
   - 压缩库 (zlib1g-dev, libbz2-dev)
   - Kivy 相关库 (libsdl2-dev, libsdl2-image-dev, 等)

3. **添加缺少的依赖**
   如果需要添加其他依赖，编辑 `.github/workflows/build-apk.yml`：
   ```yaml
   - name: Install system dependencies
     run: |
       sudo apt-get update
       sudo apt-get install -y \
         # 在这里添加缺少的包名
   ```

4. **常见错误和解决方案**

   **错误：`command 'gcc' failed`**
   - 解决方案：确保已安装 `build-essential`

   **错误：`Python.h: No such file or directory`**
   - 解决方案：确保已安装 `python3-dev`

   **错误：`jpeglib.h: No such file or directory`**
   - 解决方案：确保已安装 `libjpeg-dev`

   **错误：`freetype/freetype.h: No such file or directory`**
   - 解决方案：确保已安装 `libfreetype6-dev`

   **错误：`sqlite3.h: No such file or directory`**
   - 解决方案：确保已安装 `libsqlite3-dev`

   **错误：`Java not found`**
   - 解决方案：确保已安装 `openjdk-17-jdk`

   **错误：`E: Unable to locate package libtinfo5`**
   - 解决方案：将 `libtinfo5` 替换为 `libtinfo-dev`
   ```yaml
   # 错误的配置
   libtinfo5

   # 正确的配置
   libtinfo-dev
   ```

5. **重新构建**
   修复后，提交更改并推送：
   ```bash
   git add .
   git commit -m "Fix: Add missing dependencies"
   git push
   ```

### 构建超时

如果构建超时，可以尝试：
1. 减少构建的架构数量（只构建 arm64-v8a）
2. 使用更简单的依赖包
3. 增加 GitHub Actions 的超时时间

### APK 无法安装

如果生成的 APK 无法安装：
1. 检查 Android 版本是否满足最低要求（API 21+）
2. 确保设备允许安装未知来源的应用
3. 尝试使用 release 版本而非 debug 版本

## 技术细节

- 使用 Ubuntu 最新版本作为构建环境
- Python 3.11
- Buildozer 1.5.0
- Android API 33
- 支持 ARM64 和 ARMv7 架构

## 许可证
与主项目保持一致
