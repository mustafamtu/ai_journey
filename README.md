# 🚀 LangChain & LLM Agent Uygulamaları Serisi

Bu depo, sıfırdan ileri seviyeye LangChain, Vektör Veritabanları (ChromaDB), RAG (Retrieval-Augmented Generation) mimarisi ve Yapay Zeka Ajanları (AI Agents) geliştirmek üzere modüler olarak tasarlanmış örnek projeleri içerir.

---

## 📌 Proje Modülleri

### 🔍 01. Müşteri Analiz Sistemi (`01_musteri_analiz`)
Müşteri yorumlarını ve geri bildirimlerini LLM kullanarak analiz eden, özetleyen ve raporlayan modül.
- **Ana Dosyalar:** `main.py`, `analyzer.py`, `yorumlar.txt`
- **Çıktı:** Otomatik oluşturulan `analiz_raporu.txt`

### 🌐 02. SEO Uzmanı & Metin Çıkarıcı (`02_seo_uzmani`)
Web sayfalarındaki içerikleri çıkarıp SEO uyumluluğunu ve keyword stratejilerini analiz eden API ve agent aracı.
- **Ana Dosyalar:** `api.py`, `extractor.py`

### 🦜🔗 03. LangChain Temelleri (`03_langchain_basics`)
LangChain kütüphanesinin temel bileşenlerinin, stateless/stateful zincirlerin ve SQL veritabanı entegrasyonlarının gösterildiği eğitim modülü.
- **Kapsam:** Stateless vs Stateful Chat, SQLite Entegrasyonu (`history.db`)

### 🤖 04. Kişisel Asistan Chatbot (`04_kisisel_asistan`)
Kullanıcı geçmişini hafızada tutan ve API üzerinden hizmet veren kişisel asistan uygulaması.
- **Ana Dosyalar:** `chatbot.py`, `api.py`

### 🧠 05. RAG (Retrieval-Augmented Generation) Mimarisi (`05_rag_mimarisi`)
Dokümanların (PDF, TXT) parçalanması (text splitting), vektörleştirilmesi, ChromaDB veritabanına kaydedilmesi ve semantic search ile LLM'e beslenmesi süreçlerini gösteren çekirdek modül.
- **Ana Dosyalar:** `rag_split_pdf.py`, `rag_vector_db.py`, `rag_vector_search.py`, `vektor_goster.py`

### 💬 06. RAG Tabanlı Kurumsal Chatbot (`06_rag_chatbot`)
Kurumsal belgeler (örn. KVKK metinleri) üzerinden soru-cevap yapabilen, HTML arayüzü ve API desteği bulunan tam teşekküllü RAG chatbot uygulaması.
- **Arayüz & API:** `index.html`, `api.py`, `chatbot.py`

### 🛠️ 07. Yapay Zeka Ajanları - AI Agents (`07_agents`)
Dış araçları (Tools) kullanabilen, karar alabilen ve karmaşık görevleri otonom olarak yerine getiren LangChain Ajanları.

---

