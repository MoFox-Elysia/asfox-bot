@echo off
echo ========================================
echo 本地构建 APK 脚本
echo ========================================
echo.
echo 这个脚本帮助你在本地构建 APK，用于测试和调试。
echo.

echo 步骤 1: 检查 Python 环境
python --version
if errorlevel 1 (
    echo 错误: Python 未安装
    echo 请从 https://www.python.org/downloads/ 安装 Python 3.10+
    pause
    exit /b 1
)

echo.
echo 步骤 2: 安装必要的 Python 包
pip install --upgrade pip
pip install Cython==0.29.33 buildozer==1.5.0

echo.
echo 步骤 3: 检查 Buildozer 配置
if not exist buildozer.spec (
    echo 错误: buildozer.spec 文件不存在
    echo 请确保在项目根目录运行此脚本
    pause
    exit /b 1
)

echo.
echo 步骤 4: 开始构建 APK
echo 注意: 首次构建可能需要 30-60 分钟，需要下载大量依赖
echo.
set /p CONTINUE="是否继续？(y/n): "
if /i not "%CONTINUE%"=="y" (
    echo 构建已取消
    pause
    exit /b 0
)

echo.
echo 开始构建...
echo 构建日志将保存到 build.log
echo.

buildozer android debug 2>&1 | tee build.log

echo.
echo ========================================
echo 构建完成
echo ========================================
echo.

if exist bin\*.apk (
    echo ✅ APK 构建成功！
    echo.
    echo 生成的 APK 文件：
    dir /b bin\*.apk
    echo.
    echo 文件位置：%CD%\bin\
    echo.
    echo 下一步：
    echo 1. 将 APK 文件复制到 Android 设备
    echo 2. 在设备上允许安装未知来源的应用
    echo 3. 安装并测试应用
) else (
    echo ❌ APK 构建失败
    echo.
    echo 请检查 build.log 文件中的错误信息
    echo.
    echo 常见问题：
    echo 1. 网络问题 - 确保可以访问 Google 和 GitHub
    echo 2. 内存不足 - 关闭其他程序释放内存
    echo 3. 磁盘空间不足 - 确保有至少 10GB 可用空间
)

echo.
pause
