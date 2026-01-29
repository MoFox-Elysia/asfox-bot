@echo off
echo ========================================
echo 重写依赖配置 - 使用兼容版本
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
git commit -m "Fix: Rewrite dependencies with compatible versions

- Fixed all dependency versions to known compatible versions:
  - kivy==2.1.0 (stable version)
  - pillow==9.5.0 (compatible with Android)
  - fpdf2==2.7.6 (current version)
  - pyjnius==1.6.1 (compatible with Cython 0.29.33)
  - plyer==2.1.0 (stable version)
  - cython==0.29.33 (required for Pyjnius)
  - pyopenssl (for SSL support)

- Fixed buildozer and python-for-android versions:
  - buildozer==1.5.0
  - python-for-android==2024.1.21

- Added 'Clean build environment' step
- This ensures a fresh build with compatible versions
- Should resolve all compilation issues"

echo.
echo ========================================
echo 推送到 GitHub
echo ========================================
echo.

if "%1"=="" (
    echo 用法: rewrite_dependencies.bat ^<仓库URL^>
    echo.
    echo 示例: rewrite_dependencies.bat https://github.com/username/repository.git
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
echo [成功] 依赖配置已重写！
echo ========================================
echo.
echo 重写内容：
echo - 所有依赖都指定了兼容的版本号
echo - 清除了可能的版本冲突
echo - 添加了构建环境清理步骤
echo - 确保每次都是干净的构建
echo.
echo 依赖版本：
echo - Kivy: 2.1.0
echo - Pillow: 9.5.0
echo - fpdf2: 2.7.6
echo - Pyjnius: 1.6.1
echo - Plyer: 2.1.0
echo - Cython: 0.29.33
echo - Buildozer: 1.5.0
echo - python-for-android: 2024.1.21
echo.
echo 下一步：
echo 1. 访问 Actions 页面查看构建进度
echo    %REPO_URL:~0,-4%/actions
echo.
echo 2. 这次应该是全新的干净构建
echo.
echo 3. 查看构建日志，确认所有依赖正确安装
echo.
echo 4. 查看 "Find APK Location" 步骤
echo    应该能看到生成的 APK 文件
echo.
echo 5. 在 Artifacts 部分下载 APK
echo.
pause
