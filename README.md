# memory-bridge
![image](https://github.com/user-attachments/assets/fe4f75ef-d8ca-4456-8202-6167dd3ae9e1)

# 🚀 Memory Bridge AI

## **🧠 Project Overview**  
Memory Bridge AI is an **AI-powered memory reinforcement system** designed to help individuals in **memory care facilities** strengthen recall and rediscover past memories. Unlike traditional chatbots, it **builds an evolving memory graph**, tracking relationships between **people, places, and events**, reinforcing **weaker memories**, and integrating **family-uploaded images for rediscovery**.

## **🎯 Key Features**
✅ **Graph-Based Memory Storage** – AI creates a **network of linked memories**  
✅ **Conversational Memory Recall** – AI **remembers past interactions** and revisits memories for **reinforcement**  
✅ **Recall Strengthening & Testing** – AI uses **adaptive recall difficulty** (Recognition → Cued Recall → Free Recall)  
✅ **Image Upload & Rediscoverable Memories** – Family members upload photos, and AI **uses them as recall prompts**  
✅ **Memory Graph Visualization** – The graph **dynamically updates in real-time** to show how memories connect  

---

## **🛠 Tech Stack**
| **Component** | **Technology** |
|--------------|--------------|
| **Backend (Memory Storage & Retrieval)** | JSON (for MVP), NetworkX (graph model), Flask |
| **Conversational AI** | OpenAI GPT-4 API (or Mistral-7B), LangChain |
| **Recall Reinforcement** | AI uses **adaptive recall logic** based on user responses |
| **Frontend (UI & Graph Visualization)** | Flask (chat UI), Plotly Dash (interactive graph) |
| **Image Upload & Retrieval** | Flask file handling, stored image metadata in JSON |

---

## **👥 Team Roles & Responsibilities**
| **Team Member** | **Role** | **Tasks** |
|--------------|--------------|--------------|
| **AI Developer** | **Conversational AI & Memory Recall** | Implements chatbot logic, adaptive recall, connects AI with memory graph |
| **Data Scientist** | **Memory Graph & Visualization** | Creates and updates NetworkX-based memory graph, builds interactive visualization |
| **Frontend Developer** | **Chat UI & Image Upload** | Develops chatbot interface, image upload portal, integrates visualization |

---

## **⏳ 8-Hour Plan: Get a Working MVP**
This plan ensures a **basic working prototype** that can **store and retrieve memories, reinforce recall, and display a simple graph.**

| **Time Block** | **Task** | **Who Works on It?** |
|--------------|----------------------------|----------------|
| **Hour 1-2** | Set up project structure (Flask backend, chatbot API, JSON storage) | **All team members** |
| **Hour 3-4** | Implement **basic memory graph storage (JSON/NetworkX)** | **Data Scientist** |
| **Hour 3-4** | Develop **basic chatbot API** that references stored memories | **AI Developer** |
| **Hour 5-6** | Create **Flask-based chat UI** for interacting with AI | **Frontend Developer** |
| **Hour 6-7** | Implement **static memory visualization (Plotly/Matplotlib)** | **Data Scientist** |
| **Hour 7-8** | **End-to-end testing & debugging** | **All team members** |

✅ **By Hour 8, We Can Demo:**  
1️⃣ User **enters a memory** in the chat UI.  
2️⃣ AI **remembers & references it later**.  
3️⃣ The **memory graph updates & displays connections**.  

---

## **🚀 24-Hour Plan: Full Scientific Version**
After the **MVP is working**, we **enhance the project** with features backed by **modern Alzheimer's therapy research**.

| **Time Block** | **Feature** | **Why It’s Important?** | **Who Works on It?** |
|--------------|--------------------|------------------|----------------|
| **Hour 9-12** | 🔹 **Dynamic Recall Testing** (Recognition → Cued Recall → Free Recall) | **Better memory reinforcement based on cognitive therapy** | **AI Developer** |
| **Hour 9-12** | 🔹 **Image Upload for Rediscovery** | **Adds personal touch, aligns with reminiscence therapy** | **Frontend Dev + Data Scientist** |
| **Hour 13-16** | 🔹 **Confidence Tracking for Memory Integrity** | **Prevents AI from reinforcing false memories** | **AI Developer** |
| **Hour 13-16** | 🔹 **Graph Enhancements (Live Updates & Clickable Nodes)** | **More interactive & visually compelling** | **Data Scientist** |
| **Hour 17-20** | 🔹 **Cognitive Stimulation Therapy (CST) Features** | **Aligns with Alzheimer’s research, makes AI-backed exercises more engaging** | **AI Developer** |
| **Hour 17-20** | 🔹 **Music-Based Memory Recall (Music Therapy)** | **Evidence-backed approach to memory retrieval** | **Frontend + AI Developer** |
| **Hour 21-24** | 🔹 **Final Testing, Bug Fixes, and UI Polish** | **Ensures smooth demo experience** | **All team members** |

---

## **🔬 Scientific Enhancements in the 24-Hour Plan**
Claude’s suggestions helped us **align with existing Alzheimer’s research** while keeping our innovation intact. Here’s how we integrate **proven therapy techniques** into our project:

### **🔹 1. Cognitive Stimulation Therapy (CST) Features**
- AI **introduces theme-based memory exercises** (e.g., "Tell me about a childhood holiday").  
- **Why It’s Important:** **Gives our project clinical credibility**.

### **🔹 2. Music-Based Memory Recall (Music Therapy)**
- **How We Implement It:** Allow family members to **tag memories with music**.  
- **Why It’s Important:** **Scientifically backed as a powerful memory trigger**.  

### **🔹 3. Confidence Tracking for Memory Integrity**
- **Prevents AI from reinforcing false memories** by **tracking recall confidence & flagging inconsistencies**.  

---

## **🎤 Hackathon Demo Plan**
🔥 **Live Walkthrough:**  
1️⃣ User **shares a memory** (*"I went to Paris with Lisa in 1998."*).  
2️⃣ **Memory Graph updates** with nodes for **Lisa, Paris, and 1998**.  
3️⃣ AI later **tests recall** → *"Who was with you on that trip?"*  
4️⃣ **Family uploads a photo** → AI uses it for rediscovery.  
5️⃣ **Graph visualization updates dynamically**, showing **stronger recall links**.  

---

## **🏆 Why This Hackathon Plan Wins**
✅ **MVP in 8 Hours:** Guarantees **a working demo** with a chatbot + memory graph.  
✅ **24-Hour Enhancements:** Adds **scientific credibility** using **real therapeutic techniques**.  
✅ **Emotional Connection:** Family uploads + music recall = **more engaging & human-centered**.  
✅ **Visually Impactful:** Memory Graph + Image Prompts = **impressive for judges**.  

---

### **🚀 Next Steps**
- **Confirm JSON vs. Neo4j for memory storage** (stick with JSON for MVP).  
- **Define chatbot’s structured recall prompts** for CST-based memory exercises.  
- **Finalize the UI for family uploads & visualization display.**  

Let’s make this the most impactful hackathon project! 🚀
