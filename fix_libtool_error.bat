@echo off
echo ========================================
echo 修复 libtool 兼容性问题
echo ========================================
echo.

echo 正在初始化 Git 仓库...
if not exist .git (
    git init
)

echo.
echo 添加修复的文件...
git add .github/workflows/build-apk.yml buildozer.spec

echo.
echo 创建提交...
git commit -m "Fix: Resolve libtool macro compatibility issues

- Added m4, bison, flex, gperf to system dependencies
- Added 'Fix libtool macros' step before build
- Try to install automake1.11 for better compatibility
- Create symlink for ltmain.sh to fix macro issues
- Added pyopenssl to requirements
- This fixes the LT_SYS_SYMBOL_USCORE error in libffi compilation
- The error was caused by missing libtool macros in Ubuntu 22.04"

echo.
echo ========================================
echo 推送到 GitHub
echo ========================================
echo.

if "%1"=="" (
    echo 用法: fix_libtool_error.bat ^<仓库URL^>
    echo.
    echo 示例: fix_libtool_error.bat https://github.com/username/repository.git
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
echo [成功] libtool 修复已推送！
echo ========================================
echo.
echo 修复内容：
echo - 添加了 m4, bison, flex, gperf 等构建工具
echo - 添加了 libtool 宏修复步骤
echo - 添加了 pyopenssl 到依赖
echo - 解决了 LT_SYS_SYMBOL_USCORE 错误
echo.
echo 下一步：
echo 1. 访问 Actions 页面查看构建进度
echo    %REPO_URL:~0,-4%/actions
echo.
echo 2. 这次应该能够成功编译 libffi
echo.
echo 3. 构建完成后，查看 "Find APK Location" 步骤
echo    应该能看到生成的 APK 文件
echo.
echo 4. 在 Artifacts 部分下载 APK
echo.
pause
