@echo off
echo ========================================
echo 修复构建配置并推送
echo ========================================
echo.

echo 正在初始化 Git 仓库...
if not exist .git (
    git init
)

echo.
echo 添加所有修复的文件...
git add .

echo.
echo 创建提交...
git commit -m "Fix: Add missing system dependencies and optimize build configuration

- Added comprehensive system dependencies including Java 17, image libraries, and GUI libraries
- Optimized buildozer.spec by removing problematic asset copy configuration
- Added Buildozer cache to speed up subsequent builds
- Added Java 17 setup step for Android SDK compatibility
- Improved error handling and build logging"

echo.
echo ========================================
echo 推送到 GitHub
echo ========================================
echo.

if "%1"=="" (
    echo 用法: fix_build.bat ^<仓库URL^>
    echo.
    echo 示例: fix_build.bat https://github.com/username/repository.git
    echo.
    pause
    exit /b 1
)

set REPO_URL=%1

echo 设置远程仓库...
git remote add origin %REPO_URL% 2>nul
if errorlevel 1 (
    echo 远程仓库已存在，更新 URL...
    git remote set-url origin %REPO_URL%
)

echo.
echo 推送代码到 GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo [错误] 推送失败！
    echo ========================================
    echo.
    echo 如果遇到身份验证问题，请：
    echo 1. 创建 GitHub Personal Access Token
    echo    访问: https://github.com/settings/tokens
    echo 2. 使用以下命令手动推送：
    echo    git push -u origin main
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo [成功] 修复已推送！
echo ========================================
echo.
echo 下一步：
echo 1. 访问 Actions 页面查看构建进度
echo    %REPO_URL:~0,-4%/actions
echo.
echo 2. 如果构建仍然失败，请查看构建日志中的具体错误信息
echo.
echo 3. 构建成功后，在 Artifacts 部分下载 APK
echo.
pause
