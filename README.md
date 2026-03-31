> **IPFS-Meta-Portfolio**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build: BuidlGuidl Batch 23](https://img.shields.io/badge/BuidlGuidl-Batch%2023-blue)](https://buidlguidl.com/)
[![Network: Optimism](https://img.shields.io/badge/Network-Optimism-red)](https://optimistic.etherscan.io/)

## Overview

Meta-Portfolio is a decentralized technical aggregator designed to centralize and showcase multi-disciplinary engineering work. It allows developers to index their articles and projects metadata into a single searchable interface, with a permanent record anchored on the blockchain.

The project demonstrates a full-stack integration of high-performance **Rust/WebAssembly** rendering, **RAG-based (Retrieval-Augmented Generation)** search capabilities, and **Ethereum Layer 2** infrastructure for data provenance.

---

## Technical Architecture

The system is composed of three core layers, ensuring scalability, speed, and decentralization:

### 1. Intelligence Layer (Python & RAG)
* **Engine**: Powered by `FastAPI` and `LangChain`.
* **RAG Implementation**: Utilizes **Chroma DB** for vector indexing of project metadata and technical articles (e.g., Prompt Injection research).
* **LLM**: Integrated with **Groq (Llama 3.1)** for near-instantaneous agentic reasoning over the developer's skill set.

### 2. Rendering & UI Layer (Rust/Wasm & React)
* **High Performance**: The core UI components and data processing are handled by **Rust (`render.rs`)**, compiled to **WebAssembly (Wasm)** for near-native browser performance.
* **Frontend**: A modern React/TypeScript dashboard that interacts with the Wasm engine to visualize complex portfolio data.

### 3. Trust Layer (Solidity & IPFS)
* **On-chain Anchor**: Portfolio snapshots are minted as ERC-721 tokens on **Optimism Mainnet**.
* **Decentralized Storage**: All metadata and source-code hashes are persisted via **IPFS**, ensuring the portfolio remains tamper-proof and permanent.

---

## 🔗 Verifiable Links

* **Live Demo**: [https://meta-portfolio-frontend.vercel.app/](https://meta-portfolio-frontend.vercel.app/)
* **NFT Contract (Optimism)**: `0x832F4120a1A745D8DA4D8A6A8C53C598284ad3aD`
* **Mint Transaction**: [View on Optimistic Etherscan](https://optimistic.etherscan.io/tx/0x31951c7c638f1f189685dcae2acf8d00e3a1447db306ca37a348d6cfce2b3d80)

---

## Repository Structure

```bash
├── app/
│   ├── engine/       # Python RAG Server & Router logic
│   └── ui/           # Rust/Wasm rendering engine (render.rs)
├── mint/             # Solidity smart contracts (mintMETAP.sol) & NFT metadata
├── web/              # React/Vite Frontend
└── data/             # Vector database source & Metadata snapshots
```

## Author: stardustclub.eth

* BuidlGuidl Batch 23 Member

* Focused on AI-Agentic Workflows and EVM Infrastructure.
