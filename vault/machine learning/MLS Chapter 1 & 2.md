---
date: 2026-06-11
category: Machine Learning
confidence: 1.0
---
# MLS Chapter 1 & 2

> **AI Reasoning for Classification:** The text discusses the foundations of machine learning (ML) systems, their deployment paradigms, and the trade-offs involved in each. It highlights the differences between ML systems and traditional deterministic software, emphasizing the probabilistic nature of ML architectures. The text also touches on the importance of algorithms, data, and computing infrastructure in ML systems, as well as the need for a five-pillar framework to manage complexity. Given these topics and themes, I am confident that this text belongs to the category 'Machine Learning'.

### 🧠 AI Synthesis
The new note further solidifies the notion that ML systems are fundamentally different from traditional software. By highlighting the probabilistic nature of ML and the interdependence of algorithms, data, and computing infrastructure, this chapter underscores the importance of considering the AI Triangle's constraints when designing and deploying ML models. This concept complements earlier notes on silent performance degradation, the bitter lesson learned from AI history, and the five-pillar framework for managing complexity in ML systems engineering.

### 🔗 Related Notes
- [[MLS Chapter 1 & 2.pdf]]
- [[MLS Chapter 1 & 2.pdf]]

---
### Source Content
Part 1: Foundations of ML Systems (Chapter 1) The text establishes that ML systems are fundamentally different from traditional deterministic software.

Instead of following explicit rules, ML systems are probabilistic architectures whose behaviors emerge from patterns in data.

● The AI Triangle: Every ML system relies on the strict interdependence of three components:

Algorithms (the models), Data (the training and inference inputs), and Computing Infrastructure (the hardware).

A limitation in any one component restricts the capabilities of the others.

 ● Silent Performance Degradation: Unlike traditional software that crashes visibly when it fails, ML systems can continue running perfectly on the infrastructure side while their accuracy silently degrades.

This is usually caused by "data drift"—when real-world operational data diverges from the data the model was trained on.

 ● The "Bitter Lesson": Looking at AI history, the most significant breakthroughs haven't come from hard-coding human expertise, but from general algorithms that leverage massive computational scale.

 ● The Five-Pillar Framework: To manage the complexity of moving from the lab to production, ML systems engineering relies on five interconnected disciplines:

Data Engineering, Model Training, Model Deployment, Operation & Maintenance, and Ethics & Governance.

Part 2: Deployment Paradigms (Chapter 2) System deployment is dictated by immutable physical constraints—specifically the speed of light (latency), the "power wall" (energy and thermal limits), and the "memory wall" (bandwidth limitations).

These constraints force engineers to choose between four distinct deployment paradigms:

● Cloud ML: Operates in massive data centers, offering virtually unlimited computational capacity and storage.

 ○ Best for: Training large models and processing massive datasets (e.g., recommendation engines, large language models).

 ○ Trade-offs: Suffers from high network latency (100-500ms), requires constant connectivity, and poses data privacy risks by requiring data transmission.

 ● Edge ML: Moves computation closer to the data source using local servers, industrial controllers, or gateways.

 ○ Best for: Autonomous vehicles, industrial IoT, and smart retail.

 ○ Trade-offs: Drastically reduces latency (10-100ms) and keeps sensitive data on-site, but requires upfront hardware investments and constrains model complexity compared to the cloud.

 ● Mobile ML: Runs models directly on battery-powered personal devices like smartphones and tablets.

 ○ Best for: Computational photography, real-time translation, and personalized voice assistants.

 ○ Trade-offs: Enables complete offline functionality and strong user privacy, but is strictly limited by battery life, memory, and thermal throttling (devices getting too hot).

 ● Tiny ML: Deploys intelligence onto ultra-cheap microcontrollers and embedded sensors.

 ○ Best for: Wake-word detection, wildlife tracking, and predictive maintenance.

 ○ Trade-offs: Operates on milliwatts of power, allowing for "deploy-and-forget" sensors that run on coin-cell batteries for years.

However, severe memory limits (often kilobytes) force massive model compression and reduced accuracy.

The Reality: Hybrid Architectures In practice, modern ML systems rarely rely on just one paradigm. Hybrid ML combines these tiers to balance their trade-offs.

A common example is the Train-Serve Split , where a massive model is trained on the cloud, but a compressed, optimized version is deployed to an edge or mobile device for fast, private inference.
