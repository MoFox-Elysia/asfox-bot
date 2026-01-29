@echo off
echo ========================================
echo 添加 lld 链接器并优化构建
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
git commit -m "Fix: Add lld linker and optimize build configuration

- Added lld (LLVM linker) to system dependencies
- Added clang compiler for better compatibility
- Added libc++-dev and libc++abi-dev for C++ standard library
- Changed android.archs to arm64-v8a only (faster build)
- This should fix:
  - lld not found warnings
  - libffi linking issues
  - hostpython3 build failures
- Building only arm64-v8a reduces build time and complexity
- arm64-v8a covers most modern Android devices"

echo.
echo ========================================
echo 推送到 GitHub
echo ========================================
echo.

if "%1"=="" (
    echo 用法: add_lld_optimize.bat ^<仓库URL^>
    echo.
    echo 示例: add_lld_optimize.bat https://github.com/username/repository.git
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
echo [成功] lld 链接器已添加！
echo ========================================
echo.
echo 修复内容：
echo - 添加了 lld 链接器，加快链接速度
echo - 添加了 clang 编译器，提高兼容性
echo - 添加了 C++ 标准库支持
echo - 只构建 arm64-v8a 架构，加快构建速度
echo - 应该解决 hostpython3 构建失败问题
echo.
echo 新增依赖：
echo - lld: LLVM 链接器
echo - clang: LLVM 编译器
echo - libc++-dev: C++ 标准库
echo - libc++abi-dev: C++ ABI 库
echo.
echo 架构优化：
echo - 只构建 arm64-v8a（减少 50% 构建时间）
echo - 覆盖大多数现代 Android 设备
echo.
echo 下一步：
echo 1. 访问 Actions 页面查看构建进度
echo    %REPO_URL:~0,-4%/actions
echo.
echo 2. 查看 "Build APK with Buildozer" 步骤
echo    应该不再有 lld 警告
echo.
echo 3. 查看 "Find APK Location" 步骤
echo    应该能看到生成的 APK 文件
echo.
echo 4. 在 Artifacts 部分下载 APK
echo.
pause
