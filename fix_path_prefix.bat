@echo off
echo ========================================
echo 修复路径前缀问题
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
git commit -m "Fix: Add ./ prefix to all artifact upload paths

- Added ./ prefix to all paths in upload-artifact step
- Paths now use relative paths from project root
- Fixed: ./bin/*.apk
- Fixed: ./.buildozer/android/platform/build-*/build/outputs/apk/debug/*.apk
- Fixed: ./.buildozer/android/platform/build-*/build/outputs/apk/release/*.apk
- Without ./ prefix, paths were interpreted incorrectly"

echo.
echo ========================================
echo 推送到 GitHub
echo ========================================
echo.

if "%1"=="" (
    echo 用法: fix_path_prefix.bat ^<仓库URL^>
    echo.
    echo 示例: fix_path_prefix.bat https://github.com/username/repository.git
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
echo - 所有上传路径都添加了 ./ 前缀
echo - 确保路径被正确解释为相对路径
echo - 修复了 GitHub Actions 路径解析问题
echo.
echo 下一步：
echo 1. 访问 Actions 页面查看构建进度
echo    %REPO_URL:~0,-4%/actions
echo.
echo 2. 这次应该能够成功上传 APK 文件
echo.
echo 3. 在 Artifacts 部分下载 APK
echo.
pause
