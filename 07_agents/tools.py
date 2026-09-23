from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch

load_dotenv()

events_db = [
    {
        "id": "101",
        "title": "Temel Seviye Yüzme Kursu",
        "category": "Spor",
        "start_date": "2026-06-01",
        "end_date": "2026-08-30",
        "status": "active",
        "capacity": 0,
    },
    {
        "id": "102",
        "title": "İleri Seviye React Workshop",
        "category": "Yazılım",
        "start_date": "2026-04-15",
        "end_date": "2026-04-20",
        "status": "active",
        "capacity": 15,
    },
    {
        "id": "103",
        "title": "Yağlı Boya Resim Teknikleri",
        "category": "Sanat",
        "start_date": "2026-05-10",
        "end_date": "2026-07-10",
        "status": "passive",
        "capacity": 10,
    },
    {
        "id": "104",
        "title": "Piyano Başlangıç Eğitimi",
        "category": "Müzik",
        "start_date": "2026-09-01",
        "end_date": "2026-12-25",
        "status": "active",
        "capacity": 8,
    },
    {
        "id": "105",
        "title": "Python ile Veri Analizi",
        "category": "Yazılım",
        "start_date": "2026-05-01",
        "end_date": "2026-06-15",
        "status": "active",
        "capacity": 25,
    },
    {
        "id": "106",
        "title": "Diksiyon ve Hitabet Kursu",
        "category": "Kişisel Gelişim",
        "start_date": "2026-04-01",
        "end_date": "2026-04-30",
        "status": "active",
        "capacity": 12,
    },
]

tavily_search = TavilySearch(max_results=3, search_engine="google", language="tr", description="Kurs Merkezi etkinlikleri hakkında bilgi almak için internette aram yapar")

@tool
def get_all_events():
  """Tüm etkinlikleri döndürür"""
  return events_db


@tool
def get_event_by_id(event_id: str):
  """Belirli bir etkinliği ID'sine göre döndürür"""
  for event in events_db:
    if event["id"] == str(event_id):
      return event
  return None


@tool
def check_capacity(event_id: str):
  """Belirli bir etkinliğin kapasitesini kontrol eder"""
  for event in events_db:
    if event["id"] == str(event_id):
      return "BOŞ" if event["capacity"] > 0 else "DOLU"
  return "BULUNAMADI"


tools = [get_all_events, get_event_by_id, check_capacity, tavily_search]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

my_system_prompt = """
    Sen bir kurs merkezinde çalışan yapay zeka asistanısın. Kullanıcıların etkinlikler hakkında bilgi almasına yardımcı oluyorsun.

    KURALLAR:
    1. Kullanıcıdan gelen sorulara yanıt verirken, yalnızca mevcut etkinlik veritabanındaki bilgilere dayanabilirsin.
    2. Eğer kullanıcı, etkinliklerin kapasitesi hakkında bilgi almak isterse, kapasiteyi kontrol etmek için check_capacity aracını kullanabilirsin.
    3. Eğer kullanıcı, belirli bir etkinliği ID'sine göre sormak isterse, get_event_by_id aracını kullanabilirsin.
    4. Eğer kullanıcı, tüm etkinlikleri görmek isterse, get_all_events aracını kullanabilirsin.
    5. Eğer kullanıcı, veritabanında bulunmayan bir etkinlik hakkında bilgi almak isterse, tavily_search aracını kullanabilirsin.
    6. Kullanıcıya yanıt verirken, yalnızca veritabanındaki bilgilere dayan ve hayali bilgiler ekleme.
"""

checkpointer = MemorySaver()

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=my_system_prompt,
    checkpointer=checkpointer,
)


def invoke_with_user(user_id: str, question: str):
  """Belirli bir kullanıcı için soruyu yanıtlar"""
  thread_id = f"user_session_{user_id}"
  return agent.invoke(
      {"messages": [HumanMessage(content=question)]},
      config={"configurable": {"thread_id": thread_id}},
  )


response1 = invoke_with_user("1", "Bana tüm etkinlikleri gösterir misin?")
response2 = invoke_with_user(
    "1", "ID'si 102 olan etkinliğin kapasitesi dolmuş mu?"
)
response3 = invoke_with_user(
  "1", "React nedir?")

print("1. Yanıt:\n", response1["messages"][-1].content)
print("\n" + "=" * 50 + "\n")
print("2. Yanıt:\n", response2["messages"][-1].content)