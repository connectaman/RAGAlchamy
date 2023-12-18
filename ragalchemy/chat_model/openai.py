import openai
openai.api_key = "OPENAIKEY"

class ChatOpenAI:
    def __init__(self, model_name):
        self.model_name = model_name
        self.messages = []
        
    def add_system_prompt(
            self, 
            system_prompt:str
        ) -> None:
        """
        Adds a system prompt to the list of messages.

        Parameters:
            system_prompt (str): The system prompt to be added.

        Returns:
            None
        """
        message = {
            "role": "system",
            "content": system_prompt
        }
        self.messages.append(message)
    
    def add_history(
            self,
            user: str,
            assistant: str
        ) -> None:
        """
        Add a user and assistant message to the chat history.

        Parameters:
            user (str): The user message to be added.
            assistant (str): The assistant message to be added.

        Returns:
            None
        """
        # Create a dictionary representing the user message
        user_message = {"role": "user", "content": user}
        # Create a dictionary representing the assistant message
        assistant_message = {"role": "assistant", "content": assistant}
        # Append the user message to the chat history
        self.messages.append(user_message)
        # Append the assistant message to the chat history.
        self.messages.append(assistant_message)

    
    def predict(self, prompt : str):
        message = {"role": "user", "content": prompt}
        self.messages.append(message)
        response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=self.messages,
                temperature=0.0,
                max_tokens=1500,
                stream=False
            )
        return response.choices[0]["message"]["content"].strip()
