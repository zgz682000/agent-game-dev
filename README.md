# Agent Game Dev

**English** | [中文](#中文)

---

## English

### Overview

**Agent Game Dev** is a framework designed to help game developers build a one-person multi-agent game development studio. This framework is built on top of Microsoft's [agent-framework](https://github.com/microsoft/agent-framework), providing a powerful and flexible foundation for creating AI-powered game development workflows.

### Features

- 🤖 **Multi-Agent Architecture**: Leverage multiple AI agents working together to handle different aspects of game development
- 🎮 **Game Development Focus**: Specifically designed for game development workflows and pipelines
- 🏗️ **Modular Design**: Core framework with extensible architecture for customization
- 📦 **Workspace Support**: Built-in support for managing multiple projects and samples
- 🔧 **Type Safety**: Full type checking with Pyright and MyPy for robust development

### Requirements

- Python >= 3.13
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Install using uv
uv sync
```

### Project Structure

```
agent-game-dev/
├── core/              # Core framework module
├── samples/           # Example projects and samples
│   └── base-sample/   # Base sample project
└── pyproject.toml     # Root project configuration
```

### Getting Started

1. Clone the repository
2. Install dependencies: `uv sync`
3. Explore the samples in `samples/base-sample/` to see how to use the framework
4. Start building your own multi-agent game development workflow!

### Development

This project uses strict type checking and follows best practices:

- **Type Checking**: Pyright (strict mode) and MyPy
- **Package Manager**: uv with workspace support
- **Code Quality**: Full type annotations and strict linting

### License

See [LICENSE](LICENSE) file for details.

---

## 中文

### 概述

**Agent Game Dev** 是一个旨在帮助游戏开发者组建单人+多智能体游戏开发工作室的框架。该框架基于微软的 [agent-framework](https://github.com/microsoft/agent-framework)，为创建 AI 驱动的游戏开发工作流提供了强大而灵活的基础。

### 特性

- 🤖 **多智能体架构**：利用多个 AI 智能体协同工作，处理游戏开发的不同方面
- 🎮 **游戏开发导向**：专为游戏开发工作流和流程设计
- 🏗️ **模块化设计**：核心框架具有可扩展架构，支持自定义
- 📦 **工作区支持**：内置支持管理多个项目和示例
- 🔧 **类型安全**：使用 Pyright 和 MyPy 进行完整的类型检查，确保开发稳健性

### 要求

- Python >= 3.13
- [uv](https://github.com/astral-sh/uv) 包管理器

### 安装

```bash
# 使用 uv 安装
uv sync
```

### 项目结构

```
agent-game-dev/
├── core/              # 核心框架模块
├── samples/           # 示例项目和样例
│   └── base-sample/   # 基础示例项目
└── pyproject.toml     # 根项目配置
```

### 快速开始

1. 克隆仓库
2. 安装依赖：`uv sync`
3. 查看 `samples/base-sample/` 中的示例，了解如何使用框架
4. 开始构建您自己的多智能体游戏开发工作流！

### 开发

本项目使用严格的类型检查并遵循最佳实践：

- **类型检查**：Pyright（严格模式）和 MyPy
- **包管理器**：支持工作区的 uv
- **代码质量**：完整的类型注解和严格的代码检查

### 许可证

详情请参阅 [LICENSE](LICENSE) 文件。

