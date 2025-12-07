# AILex: System Hiper-Precyzyjnej Analizy Przetargowej

> **Projekt zrealizowany w ramach HackNation 2025**
> *Wyzwanie: Asystent AI dla administracji - precyzja i tempo decyzji administracyjnych w służbie państwa.*

[![Prezentacja Projektu](https://img.shields.io/badge/Prezentacja-PDF-red?style=for-the-badge&logo=adobeacrobatreader)](./link_do_prezentacji.pdf)
[![Wideo Demo](https://img.shields.io/badge/Wideo-Demo-blue?style=for-the-badge&logo=youtube)](LINK_DO_TWOJEGO_FILMU)
[![Licencja](https://img.shields.io/badge/Licencja-MIT-green?style=for-the-badge)](./LICENSE)

---

## 🏛️ O Projekcie

**AILex** to zaawansowany system klasy Enterprise wspierający orzeczników i urzędników w procesie analizy dokumentacji przetargowej (SWZ). Projekt rozwiązuje problem *wąskich gardeł* decyzyjnych wynikających z obszerności dokumentacji i presji czasu.

System wyróżnia się **ekstremalną granulacją procesu analitycznego** – zamiast jednego modelu, zastosowano tu architekturę roju (Swarm Architecture) składającą się z **56 wyspecjalizowanych agentów**, co gwarantuje niespotykaną dotąd precyzję w wyłapywaniu niuansów prawnych.

---

## 🧠 Architektura: Massive Multi-Agent System

Sercem rozwiązania jest orkiestrator zarządzający armią dedykowanych mikro-agentów. Każdy aspekt dokumentu jest analizowany niezależnie, co eliminuje ryzyko pominięcia kluczowych informacji.

### 1. Centralny Orkiestrator (The Conductor)
* **Rola:** Nadzoruje cały proces, zarządza kolejką zadań i dystrybuuje fragmenty dokumentacji do odpowiednich podzespołów.
* **Funkcja:** Scalanie (Map-Reduce) wyników cząstkowych w spójny raport końcowy.

### 2. Rój Analityczny SWZ (23 Dedykowanych Agentów)
Dokumentacja SWZ (Specyfikacja Warunków Zamówienia) jest rozbijana na czynniki pierwsze. Każdy z **23 agentów** odpowiada za weryfikację jednego, konkretnego punktu dokumentacji, m.in.:
* 🤖 **Agent 01:** Przedmiot Zamówienia i CPV.
* 🤖 **Agent 05:** Warunki udziału (Wiedza i doświadczenie).
* 🤖 **Agent 12:** Kary umowne i odstąpienie od umowy.
* 🤖 **Agent 18:** Termin związania ofertą i wadia.
* 🤖 **Agent 23:** Kryteria oceny ofert (Cena vs Jakość).
* *...i 18 innych agentów specjalistycznych.*

### 3. Rój Syntezy i Decyzji (33 Agenci Podsumowania)
Po zebraniu faktów, do pracy przystępuje **33 agentów wnioskujących**, którzy przetwarzają dane na użyteczne rekomendacje:
* 📝 **Agenci Redakcyjni:** Generowanie poszczególnych sekcji uzasadnienia decyzji.
* ⚖️ **Agenci Ryzyka:** Osobna ocena ryzyk prawnych, finansowych i terminowych.
* ✅ **Agenci Compliance:** Weryfikacja zgodności z PZP (Prawo Zamówień Publicznych) i RODO.
* 🔎 **Cross-Check Agents:** Agenci weryfikujący spójność ustaleń między pozostałymi agentami.

---

## 🔐 Bezpieczeństwo i Dane (On-Premise)

Ze względu na wrażliwość danych przetargowych, AILex został zaprojektowany w architekturze **Local-First / On-Premise**:

* **100% Prywatności:** LLM jest hostowany bezpośrednio na serwerach organizacji. Żaden fragment SWZ nie opuszcza infrastruktury urzędu.
* **Brak Chmury Publicznej:** Eliminacja ryzyka przesyłania danych do zewnętrznych dostawców (brak API OpenAI/Anthropic w produkcji).
* **Guardrails:** System posiada wbudowane bezpieczniki uniemożliwiające generowanie treści niezgodnych z etyką urzędniczą.

---

## 🛠 Technologie

Projekt łączy skalowalny backend z intuicyjnym frontendem:

* **Backend & AI Orchestration:**
    * Python 3.11
    * **LangGraph / LangChain** (Zarządzanie stanem 56 agentów)
    * Local LLM (np. Bielik-7B-v2, Llama-3-70B)
* **Baza Wiedzy:**
    * Vector Store (Qdrant/ChromaDB) do obsługi orzecznictwa KIO.
* **Frontend:**
    * React + TypeScript
    * Vite & Tailwind CSS (Dashboard analityczny)
    * shadcn/ui (Komponenty interfejsu)

---

## 🚀 Instalacja i Uruchomienie

### Wymagania wstępne
* Docker
* Python 3.11+
* Node.js 18+
* Zalecane GPU z min. 24GB VRAM (dla lokalnej obsługi wszystkich agentów równolegle)

### Instrukcja

1.  **Sklonuj repozytorium:**
    ```bash
    git clone [https://github.com/twoj-nick/AILex-HackNation.git](https://github.com/twoj-nick/AILex-HackNation.git)
    cd AILex-HackNation
    ```

2.  **Uruchomienie Backendu (Orkiestratora):**
    ```bash
    cd backend
    pip install -r requirements.txt
    python main.py
    ```

3.  **Uruchomienie Frontendu:**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

---

## 📊 Scenariusz Użycia (Use Case)

1.  **Input:** Urzędnik wgrywa plik PDF z SWZ (200 stron).
2.  **Proces:** Orkiestrator uruchamia **23 agentów SWZ**. Każdy z nich w ciągu 30 sekund analizuje swój przydzielony punkt.
3.  **Wnioskowanie:** Wyniki trafiają do **33 agentów podsumowania**, którzy budują profil ryzyka i projekt decyzji.
4.  **Output:** Po 2 minutach użytkownik otrzymuje gotowy raport z podświetlonymi 3 krytycznymi ryzykami oraz gotowy draft pisma do wykonawcy.

---

## 👥 Zespół HackNation

* **KZC WAT**
---
*Wygenerowano dla potrzeb dokumentacji HackNation 2025. System zgodny z wymogami bezpieczeństwa sektora publicznego.*
