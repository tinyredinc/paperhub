# Case Study: Solving a Real-Life Poisson–Binomial CDF Problem Using Monte Carlo Approach

**Author:** Samuel Zhang  
**Date:** 2025-08-16 

## Abstract

## Background

## Problem Identification

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