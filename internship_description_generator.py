import json
from langchain.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader

def extract_description(link):
  loader = PyPDFLoader(link)
  # Define prompt
  prompt_template = """Write a concise description using less than 100 words of the internship proposal contained in the following:
  "{text}"
  CONCISE SUMMARY:"""
  prompt = PromptTemplate.from_template(prompt_template)

  # Define LLM chain
  llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", api_key="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")
  llm_chain = LLMChain(llm=llm, prompt=prompt)

  # Define StuffDocumentsChain
  stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

  docs = loader.load()
  description = stuff_chain.run(docs)
  return description


def main():
  path = './internship_scraper/internship_scraper/spiders/iasd.json'
  with open(path, encoding="utf8") as json_data:
    data = json.load(json_data)
    data = list(filter(lambda x: x['link'] not in [None, ''],data))
    total_len=len(data)

  with open('retrieved_iasd.json', encoding="utf8") as already_extracted_json:
    extracted_data=json.load(already_extracted_json)
    already_extracted = len(extracted_data)
    print(f'Already extracted {already_extracted} documents')

  links = [item['link'] for item in data]
  to_add = []
  for index, link in enumerate(links):
    if link == '' or link == None:
      continue
    if index >= total_len - already_extracted:
      continue
    print('-'*100)
    print(f'Extracting description of document {index + 1}. Title {data[index]["title"]}')
    description = extract_description(link)
    print(f'Extraction complete')
    current_json = data[index]
    current_json['description'] = description
    to_add.append(current_json)
    updated_json=to_add+extracted_data
    print('Dumping')
    with open('retrieved_iasd.json', 'w', encoding='utf-8') as f:
      json.dump(updated_json, f, ensure_ascii=False, indent=4)
   

if __name__=='__main__':
  main()
