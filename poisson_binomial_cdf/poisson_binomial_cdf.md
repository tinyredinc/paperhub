# Case Study: Solving a Real-Life Poisson–Binomial CDF Problem Using Monte Carlo Approach

**Author:** Samuel Zhang  
**Date:** 2025-08-16 

## Abstract
This case study addresses a real-world probability problem derived from a weekly badminton signup system.  
We demonstrate two approaches:  
1. **Monte Carlo simulation** for approximate probability estimation.  
2. **Analytical solution** using the **Poisson–Binomial distribution** and its cumulative distribution function (CDF).  

## Background
In the badminton signup chatroom, there is a participant limit of 14. Anyone signing up after that limit enters a waiting list. If earlier participants drop out, waiting list members may move into the valid list. However, each participant has a personal dropout probability based on historical data.  

Thus, the **admission probability** of a waiting-list participant depends on the distribution of how many earlier players drop out.

### Real-Life Example
```
#接龙
Aug 15 周五 8-11 p.m 
✨打球地址: 170 Shields Court (Markham Badminton)
✨场地：4 5号
✨限制人数14位，从第15位开始进入waitlist！
✨周四晚上8⃣️点之后不可退接龙 如果有事🐦🐦 仍需付钱或转给别人 谢谢

☀️请大家自觉按照报名人数和时间
☀️非会员要额外支付$3(直接支付给su前台)

‼️开车的朋友们请大家切记把车停在unit 1指定停车位,停在unit 2 车位有可能会被拖车

1. Helen
2. June
3. Huiyi
4. Leah
5. Cheng
6. Victor
7. 小晨
8. 小新
9. 菲菲
10. Jason
11. Kevin
12. Kevin +1
13. Jassoonk
14. Carrie 雙
15. Anson
16. 0.0🦋
17. Henry Wang
18. RED
```

In this example, the author is **ranked #18** (i.e., **4th on the waiting list**, since only the first 14 are guaranteed). For the author to play, at least **4 earlier participants** must drop out.  

---

## Problem Identification

We model the number of dropouts as a **Poisson–Binomial random variable**:

- Each player $i$ has a dropout probability $p_i$.  
- Define independent Bernoulli random variables:

$$
X_i \sim \text{Bernoulli}(p_i), \quad i = 1, 2, \dots, n
$$

where $X_i = 1$ if player $i$ drops out, $0$ otherwise.  

- The total number of dropouts is:

$$
S = \sum_{i=1}^{n} X_i
$$

- $S$ follows a **Poisson–Binomial distribution** with parameters $(p_1, p_2, \dots, p_n)$.  

A waiting-list participant at position $r$ (i.e. the $(14+r)$-th signup) gets admitted if at least $r$ people drop out:

$$
P(\text{admission for position } r) = P(S \geq r)
$$

This is equivalent to:

$$
P(\text{admission}) = 1 - F(r-1)
$$

where $F(k)$ is the CDF of the Poisson–Binomial distribution:

$$
F(k) = P(S \leq k)
$$

---

## Data Preparation

### WeChat Message Synchronization

To obtain a complete copy of chat logs spanning multiple years, you need to synchronize messages from your phone to the PC client:

- [Settings] => [General] => [Manage Chat History] => [Inport and Export Chat History]
- [Export to computer] => [Export only selected chat history] => choose chatroom (20644756264@chatroom)

By doing this, the PC client will have the full chat history for the selected chatroom. In this specific case, the history covers the period from 2023-04-06 to 2025-08-13.


### WeChat Database Decryption

WeChat PC Client uses a local SQLite database to store data such as chat logs; however, these files are encrypted. There are several open-source tools available for decryption. The one used in this project is [chatlog](https://github.com/sjzar/chatlog) by sjzar, originally developed for the MCP service to allow LLM-based AI assistants to access personal chat histories.

After automatic decryption, the decrypted SQLite database can be found at:

- \Users\[:username]\Documents\chatlog\[:wechatid]

For privacy reasons, I will not be releasing the original decrypted SQLite database files, as they contain my complete chat history with individuals and chatrooms.

### Data Preprocessing

- Import SQLite databases into MySQL

The import script used is [sqlite3-to-mysql
](https://github.com/techouse/sqlite3-to-mysql) by techouse. This step is not mandatory; the main reason for performing it is to merge multiple SQLite databases into one and to work within a more robust RDBMS environment for data cleanup.

## Monte Carlo Simulation

## Analytical Solution

An exact solution can be computed using the **Poisson–binomial distribution CDF**.  
This is done via dynamic programming:
\[
f^{(i)}(k) = (1 - q_i) f^{(i-1)}(k) + q_i f^{(i-1)}(k-1),
\]
where \(f^{(i)}(k)\) is the probability of exactly \(k\) dropouts after considering the first \(i\) players.  
After processing all players, the CDF is:
\[
F(k) = \Pr(S \leq k) = \sum_{j=0}^k f^{(n)}(j).
\]
The target probability for player \(r\) is then:
\[
\Pr(S \geq r-14) = 1 - F(r-15).
\]

This method yields exact probabilities but requires more computation than the Monte Carlo approach when \(n\) and iterations are large.

## Conclusion