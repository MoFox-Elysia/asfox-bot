@echo off
echo ========================================
echo 修复 APK 路径查找
echo ========================================
echo.

echo 正在初始化 Git 仓库...
if not exist .git (
    git init
)

echo.
echo 添加修复的文件...
git add .github/workflows/build-apk.yml

echo.
echo 创建提交...
git commit -m "Fix: Add correct Buildozer APK paths

- Added search in .buildozer/android/platform/ directory
- Added search in build outputs directory
- Added automatic copy of APK to bin/ directory
- Updated upload paths to include Buildozer's actual output locations
- APK is generated in deep directories like:
  .buildozer/android/platform/build-arm64-v8a_docker/build/outputs/apk/debug/"

echo.
echo ========================================
echo 推送到 GitHub
echo ========================================
echo.

if "%1"=="" (
    echo 用法: fix_apk_path.bat ^<仓库URL^>
    echo.
    echo 示例: fix_apk_path.bat https://github.com/username/repository.git
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
echo 修复内容：
echo - 添加了 Buildozer 实际使用的 APK 路径
echo - 自动将 APK 复制到 bin/ 目录
echo - 更新了上传路径以包含深层目录
echo.
echo 下一步：
echo 1. 访问 Actions 页面查看构建进度
echo    %REPO_URL:~0,-4%/actions
echo.
echo 2. 查看构建日志中的 "Find and display APK files" 步骤
echo    这会显示 APK 文件的实际位置和复制操作
echo.
echo 3. 在 Artifacts 部分下载 APK 文件
echo.
pause
