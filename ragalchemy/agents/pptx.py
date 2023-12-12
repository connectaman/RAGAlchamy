
from ..utils.common_functions import cosine_similarity
from ..extractors.pptx import PPTExtractor
from ..chat_model.openai import ChatOpenAI
from ..embedding.openai import get_embedding, count_tokens

class PPTSummarizer(PPTExtractor):
    def __init__(self, file_path, extraction_method: str = "slide", ocr_engine: str = "tesseract") -> None:
        super().__init__(file_path, extraction_method, ocr_engine)
        super().extract()
        
    def summarize(self,summarize_method : str = "slide",slide_number : int = 0 ,summarize_model : str = "gpt-3.5-turbo-16k", system_prompt : str = "You are passed PPT Slide Information like text,tables,charts table, image ocr extracted text. You have to generate the summary of the slide. Make sure to site your answer if answering from a table or charts and be accuracte."):
        if summarize_method == "slide":
            summarize_response = []
            for slide in self.slides:
                slide_text = slide.slide_text
                openai = ChatOpenAI(summarize_model)
                openai.add_system_prompt(system_prompt)
                response = openai.predict(slide_text)
                summarize_response.append({"Slide Number":slide.slide_number, "Title" : slide.slide_title, "Summary" : response})
            return summarize_response
        elif summarize_method == "all":
            prompt = ""
            for slide in self.slides:
                prompt += slide.slide_text + "\n\n"
            openai = ChatOpenAI(summarize_model)
            openai.add_system_prompt(system_prompt)
            response = openai.predict(slide_text)
            return response
        elif summarize_method == "single":
            for slide in self.slides:
                if (slide_number > len(self.slides)) or (slide_number <= 0):
                    raise Exception("Enter Slide Number for 'single' mode.")
                else:
                    prompt = ""
                    for slide in self.slides:
                        if int(slide.slide_number) == int(slide_number):
                            prompt += slide.slide_text
                            break
                    openai = ChatOpenAI(summarize_model)
                    openai.add_system_prompt(system_prompt)
                    response = openai.predict(slide_text)
                    return response
        else:
            raise Exception("Slide wise summary supported")
        
    def summarize_stream(self,summarize_method : str = "slide",slide_number : int = 0, summarize_model : str ="gpt-3.5-turbo-16k", system_prompt : str = "You are passed PPT Slide Information like text,tables,charts table, image ocr extracted text. You have to generate the summary of the slide. Make sure to site your answer if answering from a table or charts and be accuracte."):
        if summarize_method == "slide":
            for slide in self.slides:
                slide_text = slide.slide_text
                openai = ChatOpenAI(summarize_model)
                openai.add_system_prompt(system_prompt)
                response = openai.predict(slide_text)
                yield {"Slide Number":slide.slide_number, "Title" : slide.slide_title, "Summary" : response}
        elif summarize_method == "all":
            prompt = "Generate a detailed Summary for each slides, explain the charts and tables in detail. \n\n"
            for slide in self.slides:
                prompt += " SLIDE NUMBER : " + str(slide.slide_number) + "\n\n"
                prompt += slide.slide_text + "\n\n"
            openai = ChatOpenAI(summarize_model)
            openai.add_system_prompt(system_prompt)
            response = openai.predict(prompt)
            yield response
        elif summarize_method == "single":
            for slide in self.slides:
                if (slide_number >= len(self.slides)+1) or (slide_number <= 0):
                    raise Exception("Enter Slide Number for 'single' mode.")
                else:
                    prompt = ""
                    for slide in self.slides:
                        if int(slide.slide_number) == int(slide_number):
                            prompt += slide.slide_text
                            break
            openai = ChatOpenAI(summarize_model)
            openai.add_system_prompt(system_prompt)
            response = openai.predict(prompt)
            yield response
        elif summarize_method == "object":
            for slide in self.slides:
                slide_text = ''
                for entity in slide.entities:
                    if entity.chart_type == "text":
                        slide_text += entity.text
                    else:
                        openai = ChatOpenAI(summarize_model)
                        openai.add_system_prompt(system_prompt)
                        response = openai.predict(entity.text)
                        yield response
                if len(slide_text) > 0:
                    openai = ChatOpenAI(summarize_model)
                    openai.add_system_prompt(system_prompt)
                    response = openai.predict(entity.text)
                    yield response
        elif summarize_method == "charts":
            for slide in self.slides:
                for entity in slide.entities:
                    if entity.chart_type == "table" or entity.chart_type == "chart":
                        openai = ChatOpenAI(summarize_model)
                        openai.add_system_prompt(system_prompt)
                        response = openai.predict(entity.text)
                        yield response
        else:
            raise Exception("Slide wise summary supported")
        
class PPTQnA(PPTSummarizer):
    
    def __init__(self, file_path, extraction_method: str = "slide", ocr_engine: str = "tesseract") -> None:
        super().__init__(file_path, extraction_method, ocr_engine)
        self.retriever = []
        self.prompt = ""
        
    def run(self, query,method : str = "similarity" ,model : str ="gpt-3.5-turbo-16k", k=10, similarity_score=0.6):
        if method == "similarity":
            query_embedding = get_embedding(query)
            for slide in self.slides:
                sim = cosine_similarity(query_embedding,slide.embeddings)
                slide.similarity = sim if sim >= similarity_score else 0
            
            self.retriever = sorted(self.slides, key=lambda x: x.similarity, reverse=True)
            prompt = "You are provided with PPT slide content. Based on the provided Slide Content try to answer the following question. Be clear and answer accurately, if not answer 'I don't know'. While answering cite the slide number as source. Example ( Corrrect cites : [1] [2] [3] , Incorrect [1,2,3]). \n Question : " + query + " Slide Wise Content : \n\n"
            for slide in self.retriever[0:min(k,len(self.retriever))]:
                prompt += f"Slide [{slide.slide_number}] :  "+ slide.slide_text +"\n"
            
            self.prompt = prompt
            openai = ChatOpenAI(model)
            response = openai.predict(prompt)
            return response
        elif method == "all":
            prompt  = "You are provided with PPT slide content. Based on the provided Slide Content try to answer the following question. Be clear and answer accurately, if not answer 'I don't know'. While answering cite the slide number as source. Example ( Corrrect cites : [1] [2] [3] , Incorrect [1,2,3]). \n Question : " + query + " Slide Wise Content : \n\n"
            for slide in self.slides:
                prompt += f"Slide [{slide.slide_number}] :  "+ slide.slide_text +"\n"
            self.prompt = prompt
            openai = ChatOpenAI(model)
            response = openai.predict(prompt)
            return response
        else:
            raise Exception("Method",method,"not supported.")
        
        
        
        