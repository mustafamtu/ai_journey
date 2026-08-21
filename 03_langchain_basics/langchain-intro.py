# from dotenv import load_dotenv
# from langchain_google_genai import GoogleGenerativeAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
# from pydantic import BaseModel,Field



# load_dotenv()

# LLM = GoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.6)

# class TatliTarifi(BaseModel):
#     tatli_adi: str = Field(description="Tatlı Adı: ")
#     hazirlama_suresi: int = Field(description="Dakika Cinsinden Hazırlama Süresi: ")
#     malzemeler:list[str] = Field(description="Gerekli Malzemeler Listesi: ")
#     kalori:int = Field(description="Tatlının yaklaşık kalorisi: ")

# class TarifListesi(BaseModel):
#     tarifler: list[TatliTarifi] = Field(description="Tatlı tariflerinden oluşan bir liste.")


# # parser = StrOutputParser()
# parser = JsonOutputParser(pydantic_object=TatliTarifi)

# format_instructions = parser.get_format_instructions()

# prompt = ChatPromptTemplate.from_template("Bana {meyve} ile yapılan 3 tane tatlı tarifi ver.\n{format_instructions}")

# prompt = prompt.partial(format_instructions=format_instructions)

# # LCEL = LangChain Expression Language
# # LCEL ("|")

# chain = prompt | LLM | parser

# sonuc = chain.invoke({"meyve":"Muz"})

# import json
# print(json.dumps(sonuc, indent=2,ensure_ascii= False))