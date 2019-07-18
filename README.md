# 选课一时爽 （courses）

## 问题背景

众所周知，芃芃现在有了一个物理系的女朋友。新学期马上就要开始了，又到了选课的时候。物理系的培养方案中有好多课程，它们之间有纷繁复杂的依赖关系；如果没有学完前置课程就贸然去上，很容易选课一时爽，期末火葬场。为了不让她的女朋友面临这种尴尬的境地，芃芃决定用他最近学的知识，来安排出正确的上课顺序。

## 问题描述

你需要编写一个 `Makefile`，其中表达了附录中各个课程的依赖关系，最终目标应该是 `thesis`（毕业论文）。每当处理到一门课，你就应该在当前目录下进行以下操作：

* 使用 `touch` 命令创建一个空文件，文件名为课程的名称（以附录中给出的为准） + 一个后缀（环境变量 `SUFFIX` 指定）
* 把该课程的所有前置课程输出到该文件中，课程名字以空格分隔（不需要上述的后缀，没有前置课程则不需要）

我们保证 `SUFFIX` 总是 `.xxx` 的形式（即形成一个文件扩展名）。

为了方便你开始编写，我们提供了一个简单的 `Makefile` 示例。

## 评分

我们的 `grader` 会进行以下两个检查：

1. 使用 `make -n` 命令来检查你的 `Makefile` 真正执行命令的过程。这一步中，我们只关注那些以 `touch` 开头的命令，其他命令都会被忽略。可行的方案可能不止一种，任何一种满足依赖关系的方案都会通过测试。
2. 运行 `make`，检查你是否正确在每个课程对应的文件中写入了课程的依赖

举一个简单的例子，如果有 `A, B, C` 三门顺序依赖的课程，并且 `SUFFIX` 变量指定的后缀为 `.done`，那么你的 `Makefile` 应该执行以下的命令：

```bash
touch A.done
touch B.done
echo A > B.done
touch C
echo A B > C.done
```

上面两个检查各占 40 分。除此之外，`Makefile` 编写（正确用法、合理注释等）与 Git 使用各占 10 分。

## 提示

1. 你应该合理使用 `GNU Make` 的 automatic variables 来减少硬编码，如 `$^`, `$@`, `$<` 等。
2. 你应该合理地书写规则，以使其能够适应环境变量 `SUFFIX` 的变化。
3. `Makefile` 中的 `basename` 函数或许对你完成任务有帮助。

## 附录：课程依赖关系

为了简化起见，我们只选取了一部分课程，它们也未必与真实的课程有对应关系。

* `thesis`（毕业论文）: `analytical_mechanics`, `quantum_mechanics`, `statistical_mechanics`, `electrodynamics`
* `general_physics` （普通物理学）: 无依赖
* `analytical_mechanics` （分析力学）: `multivariate_calculus`, `general_physics`, `mathematical_physics`
* `thermodynamics` （热力学）: `multivariate_calculus`, `general_physics`
* `statistical_mechanics` （统计力学）: `thermodynamics`, `probability_theory`
* `quantum_mechanics` （量子力学）: `linear_algebra`, `general_physics`, `analytical_mechanics`
* `linear_algebra` （线性代数）: 无依赖
* `univariate_calculus` （单变量微积分）: 无依赖
* `multivariate_calculus` （多变量微积分）: `univariate_calculus`
* `mathematical_physics` （数学物理方法）: `multivariate_calculus`, `linear_algebra`
* `electrodynamics` （电动力学）: `multivariate_calculus`, `general_physics`, `mathematical_physics`
* `probability_theory` （概率论）: `multivariate_calculus`

其中每一行冒号前为课程名称，冒号后为该课程所需的前置课程。
