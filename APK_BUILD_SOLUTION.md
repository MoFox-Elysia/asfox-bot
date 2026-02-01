# APK 构建问题解决方案

## 问题分析

从 GitHub Actions 构建日志可以看出，主要问题有：

### 1. 构建过程未完成
```
# sdkmanager path "/home/runner/.buildozer/android/platform/android-sdk/tools/bin/sdkmanager" does not exist
```
构建在 Android SDK 安装阶段就停止了，没有完成 APK 的生成。

### 2. SDK 路径配置错误
原始工作流将 Android SDK 下载到错误的位置，导致 Buildozer 找不到 sdkmanager。

### 3. 缺少 APK 文件
由于构建未完成，没有生成 `./bin/*.apk` 文件，导致上传失败。

## 已实施的修复方案

### 修复 1：简化版工作流 (`build-apk-simple.yml`)
- **减少系统依赖**：只安装必要的包
- **增加超时时间**：30分钟构建时间
- **改进错误处理**：更好的日志和错误检查
- **自动上传日志**：无论构建成功与否都上传日志

### 修复 2：更新主工作流 (`build-apk.yml`)
- **修复 SDK 路径**：正确设置 Android SDK 和 NDK 路径
- **添加环境变量**：设置 `ANDROID_SDK_ROOT` 和 `ANDROID_NDK_HOME`
- **改进许可证接受**：正确放置许可证文件
- **添加构建检查**：构建后检查 APK 文件是否存在

### 修复 3：创建修复脚本 (`fix_github_actions.bat`)
- **一键修复**：自动备份、替换、提交和推送
- **详细说明**：提供清晰的步骤说明
- **错误处理**：包含完整的错误处理逻辑

## 使用说明

### 方法 1：使用修复脚本（推荐）
```bash
fix_github_actions.bat https://github.com/你的用户名/你的仓库名.git
```

### 方法 2：手动操作
1. **触发构建**：
   - 访问 GitHub Actions 页面：`https://github.com/你的用户名/你的仓库名/actions`
   - 点击 "Build Android APK (Simple and Fast)"
   - 点击 "Run workflow"

2. **监控构建**：
   - 构建过程约需 15-20 分钟
   - 查看实时日志输出
   - 如果失败，下载 `build-log` 分析问题

3. **下载 APK**：
   - 构建成功后，在 "Artifacts" 部分下载 `debug-apk`
   - 解压获得 APK 文件

## 故障排除

### 如果构建仍然失败：

#### 1. 检查构建日志
```bash
# 下载 build-log 文件
# 查看最后 100 行
tail -100 build.log

# 搜索错误关键词
grep -i "error\|fail\|missing\|not found" build.log
```

#### 2. 常见问题及解决方案

**问题：内存不足**
```
解决方案：增加虚拟内存或使用更高配置的 runner
```

**问题：网络超时**
```
解决方案：重试构建，GitHub Actions 会自动重试下载
```

**问题：依赖包冲突**
```
解决方案：检查 requirements.txt 中的版本兼容性
```

#### 3. 进一步优化建议

如果简化版工作流仍然失败，可以尝试：

1. **使用缓存**：
```yaml
- name: Cache Buildozer dependencies
  uses: actions/cache@v3
  with:
    path: ~/.buildozer
    key: ${{ runner.os }}-buildozer-${{ hashFiles('buildozer.spec') }}
```

2. **分阶段构建**：
   - 第一阶段：下载所有依赖
   - 第二阶段：构建 APK

3. **使用预构建镜像**：
```yaml
runs-on: ubuntu-22.04  # 使用更稳定的版本
```

## 技术细节

### 构建环境
- **操作系统**：Ubuntu latest
- **Python 版本**：3.10（更稳定）
- **Java 版本**：17
- **Buildozer 版本**：1.5.0
- **Android API**：33
- **NDK 版本**：25b

### 依赖包
```python
# requirements.txt
kivy==2.3.0
Pillow==10.3.0
fpdf2==2.7.6
pyjnius==1.6.1
plyer==2.1.0
Cython==0.29.33
pyopenssl==23.2.0
```

### 应用配置
- **包名**：org.errorquestion
- **应用名**：错题整理软件
- **最低 Android 版本**：API 21 (Android 5.0)
- **目标 Android 版本**：API 33 (Android 13)
- **权限**：相机、存储读写

## 联系支持

如果问题仍然存在，请提供：
1. GitHub Actions 构建日志
2. `buildozer.spec` 文件内容
3. 错误截图或描述

可以通过以下方式获取帮助：
- GitHub Issues：报告构建问题
- 项目 README：查看最新文档
- 社区支持：相关技术论坛

## 更新历史

### 2024-02-01
- 修复 Android SDK 路径问题
- 创建简化版构建工作流
- 添加修复脚本
- 改进错误处理和日志

### 2024-01-31
- 初始构建配置
- 基础 GitHub Actions 工作流
- 文档创建
