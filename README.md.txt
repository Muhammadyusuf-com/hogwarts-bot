hogwarts-bot

A Telegram chatbot that answers questions from a `.docx` file using fuzzy search.


a. Architecture Overview

This bot uses a `.docx` file as the data source. It extracts all text from the document, then splits it into sentences, and then stores them in memory. 
When user asks a question, it uses the `rapidfuzz` library to match the user's question with the most closest matching sentence. 
There is no LLM or external API. Everything is local and simple.


b. Main Functionalities and Limitations

- Users can ask questions, and the bot will return the most relevant sentence from the document.
- It shows an estimated page number and a confidence bar to make the answer more readable.
- If the match is weak, it asks the user to rephrase.
- It only works for texts in `.docx` files, and it can not work with images, tables, or multiple languages.


c. Answer Accuracy

To make sure answers never go beyond the document, I used fuzzy search only on the text from the file. So all answers are just only from the `.docx` file only.
But as the bot uses simple algorithm not Artificial Intelligence to find the answer, the answers may not always be true.

