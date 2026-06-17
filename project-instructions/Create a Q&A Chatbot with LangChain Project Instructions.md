# Create a Q&A Chatbot with LangChain Project Instructions

Source DOCX: `Create a Q&A Chatbot with LangChain Project.docx`

Addressing Student Questions about the Introduction to Tableau Course freeadvanced

With Hristina Hristova

- Type: Course project

- Duration: 8 Hours

## Description

## Solution

## Discussion

## Case Description

LangChain is an advanced framework for developing language model-powered applications. One famous use case is creating customer support or Q&A chatbots. In this Create a Q&A Chatbot with LangChain Project, discover how to create a chatbot using Python and LangChain for the Introduction to Tableau course by Ned Krastev.

To achieve this goal, you'll employ Retrieval Augmented Generation (RAG)—a technique that has become increasingly popular for building AI-powered chatbots. This LangChain tutorial encompasses three stages: indexing, retrieval, and augmented generation.

First, we index by dividing the Introduction to Tableau course transcript into shorter sections with LangChain's Markdown header and token splitters. Next, we convert these sections into numerical vectors through embedding and store these embeddings in a Chroma vector store.

In the second stage, a retriever extracts the portion of the course that is most valuable for addressing a student's question.

In the final stage, the chat model uses the retrieved text and students' questions to generate an "augmented" response, demonstrating how to make a chatbot that provides accurate and contextual answers.

To implement the chain (representing the Q&A chatbot), we'll employ the LangChain Expression Language (LCEL) protocol. It allows connecting Runnable LangChain components so that the output of one serves as the input to the next component.

The student's question is inputted into a prompt template. Filling in the template creates a complete prompt to feed to a chat model. The response from the chat model is then fed to an output parser, ensuring we return the result to the student as a string.

## The Create a Q&A Chatbot with LangChain Project will test your skills in

Utilizing LangChain's text splitters

Managing chat messages and chat prompt templates

Applying LLMs and constructing LCEL chains for course transcription correction

Generating embeddings for storage in a vector store

Constructing RunnableLambdas from regular Python functions and lambda functions

Creating LCEL chains for a Q&A chatbot

So, ready to learn how to build a chatbot using LangChain and OpenAI? Let's begin this exciting chatbot project!

## Project requirements

For this Create a Q&A Chatbot with LangChain Project, you'll need a valid OpenAI API key.

Note: This project necessitates using OpenAI's embedding and language models. Accordingly, monitor your token consumption and the associated charges.

You'll also need Jupyter Notebook up and running.

You're advised to create and work in a new environment specifically designed for this exercise, with a version of Python <4.0, >= 3.9. The following installations are required for this LangChain project:

langchain v0.3.3

Note: pip install langchain==0.3.3 will also install langchain-core and langchain-text-splitters—both required for the project.

langchain-chroma v0.1.4

langchain-community v0.3.2

langchain-openai v0.2.2

pypdf v5.0.1

python-dotenv v1.0.1

You can execute the chatbot project with different package versions. Be mindful, however, of package incompatibilities and differences in the LangChain syntax.

Since LangChain is subject to continuous updates, you might encounter minor syntax differences compared to the Build Chat Applications with OpenAI and LangChain course. If this occurs, consult the LangChain API Reference page for current classes and methods.

The Introduction_to_Tableau.pdf file contains a transcript of the Introduction to Tableau course. The LangChain_Project.ipynb Jupyter Notebook includes a skeleton of the code used throughout the project. Download these files to create a chatbot step by step in this LangChain project.

## Project content

2 Project files

Guided and unguided instructions Up to 10 XP

## Part 1: Load the Course Transcript

## Part 2: Split the Course Transcript with MarkdownHeaderTextSplitter

## Part 3: Create a Chain to Correct the Course Transcript

## Part 4: Split the Lectures with TokenTextSplitter

## Part 5: Create Embeddings, Vector Store, and Retriever

## Part 6: Create Prompts and Prompt Templates for the Q&A Chatbot Chain

## Part 7: Create the First Version of the Q&A Chatbot Chain

## Part 8: Create a Runnable Function to Format the Context

## Part 9: Stream the Response

Quiz Up to 50 XP

## Featured tools

## Topics covered

Programming

## Related courses

## To complete this project you need expertise on the following topic(s)

Build Chat Applications with OpenAI and LangChain

Load the Course Transcript

In this Create a Q&A Chatbot with LangChain Project, you'll implement a chatbot for the Introduction to Tableau course by Ned Krastev. To achieve this goal, you'll employ Retrieval Augmented Generation (RAG) encompassing three stages: indexing, retrieval, and augmented generation.

First, we index by dividing the Introduction to Tableau course transcript into shorter sections with LangChain's Markdown header and token splitters. We convert these sections into numerical vectors through embedding and store these embeddings in a Chroma vector store.

In the second stage, a retriever extracts the portion of the course that is most valuable for addressing a student's question.

In the final stage, the chat model uses the retrieved text and students' questions to generate an "augmented" response, demonstrating how to make a chatbot that provides accurate and contextual answers.

Ready to learn how to build a chatbot using LangChain and OpenAI? Let's begin!

As with any project you undertake, best practice suggests you create a new virtual environment specifically tailored to this task—with the Python version and package set described in the Project Requirements section at the front page of the project.

Once you have this set up, open the LangChain_Project.ipynb file using your new environment. In the notebook, you'll find a skeleton of the code. Your first task is to execute the cell under "Set the OpenAI API Key as an Environment Variable."

## The following line of code

%load_ext dotenv

%dotenv

loads the dotenv extension and sets the content of a .env file as an environment variable. This implies that you have a .env file already prepared with your OpenAI API key stored in the format:

OPENAI_API_KEY="…"

For convenience, keep the .env file in the same folder as the LangChain_Project.ipynb file.

Next, execute the cell under "Import the Libraries." If any libraries are missing, pip-install them in your project environment, restart the notebook's kernel, and run the cell anew.

Once you've successfully executed these first two cells, you're ready to continue with the fun part!

Prepare a loader object for the Introduction_to_Tableau.pdf file. Call it loader_pdf.

Use the PyPDFLoader class and pass the path to the Introduction_to_Tableau.pdf file as a string.

Load the content of the file to a variable called docs_list.

Do so by applying the load() method to the loader_pdf object.

Before advancing with the code, open the PDF file and study its content. The course transcript is organized into lectures, with the names of the lectures preceded by two hash signs. The lectures are further organized into sections, with the names of the sections indicated by a single hash sign. These marks will later help split the transcript into sections and lectures using LangChain's Markdown Header Text Splitter.

Since the MarkdownHeaderTextSplitter class accepts a single string as an argument, our task is to concatenate the contents of the Document objects in the docs_list into such a string. Store the string (containing the entire course transcript) in a variable called string_list_concat.

You can do so by for-looping through the items in docs_list, extracting each page's content, and appending it to the string_list_concat variable. Alternatively, you can employ Python's built-in join() function.

string_list_concat = "".join([... for ... in ...])

Split the Course Transcript with MarkdownHeaderTextSplitter

Next up in our game plan is splitting the text using LangChain's MarkdownHeaderTextSplitter class. Doing so will create a list of Document objects, each corresponding to a single lecture, with the section and lecture names stored in the metadata.

All right, let's execute this plan.

Create an instance of the MarkdownHeaderTextSplitter class and call it md_splitter. Ensure that Header 1 titles are stored as "Section Title" and Header 2 titles correspond to "Course Title."

To achieve this, ensure you define the MarkdownHeaderTextSplitter instance with the parameter headers_to_split_on. As a list of tuples, define all titles marked by # as "Section Title" and the ones marked by ## as "Lecture Title."

md_splitter = MarkdownHeaderTextSplitter(

headers_to_split_on = [(...), (...)]

)

Use the object to split the string_list_concat variable. Store the result in a new one called docs_list_md_split.

Apply the split_text method on the MarkdownHeaderTextSplitter object and pass string_list_concat as an argument. This will create a list of Document objects, each containing the metadata and content of an Introduction to Tableau lecture.

Create a Chain to Correct the Course Transcript

All right! We now have the transcript split into documents, with each document corresponding to a separate lecture from the course. But if you inspect the content of the documents closely, you'll find that the transcript is not without flaws—the punctuation seems incorrect, the paragraphs are not split well, and some of the words are plain wrong.

So, to implement a high-quality final product, we must transform the page contents so that the text is readable. Of course, doing that by hand would be very time-consuming. So, let's employ an LLM to do that for us.

The approach would be to create a simple LCEL chain consisting of a chat prompt template (where we'll pass the lecture scripts one at a time), a chat model, and a sting output parser. We'll then invoke the chain to pass all lecture texts in parallel.

Let's execute this plan!

Extract the lecture texts from all Document objects in docs_list_md_split. Store them as a list of strings (string_list_split) so an individual string stores a particular lecture.

You can do that using a for-loop or a list comprehension.

string_list_split = [... for i in docs_list_md_split]

Split the Lectures with TokenTextSplitter

Okay, we now have a list of documents, each with a lecture from the Introduction to Tableau course. We've also improved the transcript with the help of the GPT-4o model. Still, glancing through the lectures, you’ll find some are quite long. For this project phase, your task is to divide the lectures further, now adhering to a maximum token count.

Create a token text splitter that uses the "cl100k_base" encoding, limits the chunk sizes to 500 tokens, and introduces a 50-tokens overlap between subsequent chunks. Use this object to split the documents in the docs_list_md_split list and store the result in a variable called docs_list_tokens_split.

## To execute this task

Create an instance of the TokenTextSplitter class with parameters encoding_name, chunk_size, and chunk_overlap set to the corresponding values.

token_splitter = TokenTextSplitter(encoding_name=...,

chunk_size=...,

chunk_overlap=...)

Apply the split_documents() methods to the splitter, passing the docs_list_md_split as an argument.

Ensure the new document list is stored in the docs_list_tokens_split variable.

Create Embeddings, Vector Store, and Retriever

Having split the text, we'll proceed to the next indexing phase: embedding the documents, storing them locally in a vector database, and establishing a vector store-backed retriever.

Create an OpenAI embedding instance called embedding that uses the "text-embedding-3-small" model.

Do so by initializing an instance of the OpenAIEmbeddings class and passing the model's name as an argument.

Next, use the embedding object and the docs_list_tokens_split list to define a Chroma vector database called vectorstore. Store the embeddings in a local folder called "intro-to-tableau."

To achieve this, create an instance of the Chroma class and apply the from_documents() method. Set the documents parameter to docs_list_tokens_split and the embedding parameter to embedding. To store the database locally, set the persist_directory parameter equal to the string "./intro-to-tableau." This will create the database in the same folder as your Jupyter Notebook file.

vectorstore = Chroma.from_documents(documents = ...,

embedding = ...,

persist_directory = ...)

Note that the from_documents() method only applies when creating the vector store. If you wish to define the vectorstore variable from an existing local database, create an instance of the Chroma class and specify the directory of the database and the embedding function.

vectorstore = Chroma(persist_directory = ...,

embedding_function = ...)

Finally, for the indexing part, use the Chroma vector store to create a Runnable retriever object that would later enter our LCEL Q&A chatbot chain. Apply the maximal marginal relevance search type, ensure the retriever fetches exactly two documents and set the lambda parameter of the MMR search to 0.7.

To do this, apply the as_retriever() method to the vectorstore object. As a first argument, set the search_type parameter to "mmr". The other two values—the number of retrieved documents and the lambda parameter—are specified inside a dictionary using the search_kwargs parameter.

retriever = vectorstore.as_retriever(search_type = ...,

search_kwargs = {...,

...})

Create Prompts and Prompt Templates for the Q&A Chatbot Chain

You've now reached the most intriguing part of the project—creating the components of the Q&A chatbot chain and, eventually, constructing the chain. In this section, your task is to create the prompts and prompt templates necessary for instructing the chatbot, providing the context, and feeding the students' questions.

Familiarize yourself with the strings PROMPT_CREATING_QUESTION, PROMPT_RETRIEVING_S, and PROMPT_TEMPLATE_RETRIEVING_H, which we'll explore further below. We've maintained consistent naming conventions, with "S" and "H" representing "system" and "human," respectively. Now, your task is to:

Create a prompt template using PROMPT_CREATING_QUESTION. Call it prompt_creating_question.

Create a system message using PROMPT_RETRIEVING_S. Call it prompt_retrieving_s.

Create a human message prompt template using PROMPT_TEMPLATE_RETRIEVING_H. Call it prompt_template_retrieving_h.

Create a chat prompt template combining the system message and the human message prompt template. Call it chat_prompt_template_retrieving.

If you need assistance creating these objects, refer to the similar instructions in Part 3: Create a Chain to Correct the Course Transcript.

Create the First Version of the Q&A Chatbot Chain

All right, everyone! We're now ready to construct the first version of the Q&A chatbot chain. (The second and final version will feature an improvement in context formatting. We'll create this chain in the final two parts of the project.)

The line of code result = chain_retrieving.invoke(…) in the Jupyter Notebook file shows that a question comprises three elements:

The corresponding lecture's name

The question's title

The question's body

The same line also tells us that the first component of the chain is prompt_creating_question.

As you can ensure, invoking the chain with this only component results in a StringPromptValue object.

Now, we must consider how we'll feed this result in the {question} input variable from chat_prompt_template_retrieving. The required format is a string and not a StringPromptValue.

Your task is to create a RunnableLambda function that extracts the text from the StringPromptValue object. Upon invoking this two-component chain, you should obtain the following string:

Lecture: Adding a custom calculationTitle: Why are we using SUM here? It's unclear to me.Body: This question refers to calculating the GM%.

Recall that the syntax to anonymous (lambda) functions wrapped in a RunnableLambda is:

RunnableLambda(lambda x: …)

Create the third component of the chain so that upon invocation, you obtain the following dictionary:

{'context': [Document(...),

Document(...)],

'question': 'Lecture: Adding a custom calculation\n'

"Title: Why are we using SUM here? It's unclear to me.\n"

'Body: This question refers to calculating the GM%.'}

To achieve this, pipe a dictionary as the third chain element. Remember, when piped, a dictionary becomes a RunnableParallel, meaning it can integrate into the chain.

The first key, context, should hold the two most relevant documents from the vector database.

The second key is question, which refers to our earlier formulated query. This question should be transmitted unchanged as the value in this key-value pair.

Pipe the final three components of the chain so that when the chain is invoked, the chatbot's response is returned as a string.

To achieve that, pipe the chat_prompt_template_retrieving, chat, and str_output_parser components at the end of the chain.

Create a Runnable Function to Format the Context

We're almost at the finish line. But there are still two more tasks lurking, and this one can be a bit tricky. 😊

Study the chat prompt template used for the chat model. You'll notice the {context} input variable is substituted with a list of two Document objects – a format that is not very clean or tidy. A better approach would be to format the context as follows:

Document 1

Section Title: ...

Lecture Title: ...

Content: ...

-------------------

Document 1

Section Title: ...

Lecture Title: ...

Content: ...

-------------------

Create a Runnable function named format_context(...) that accepts a dictionary formatted as

{'context': [Document(...),

Document(...)],

'question': ...}

and returns the dictionary with the context key as a string formatted as shown above.

To achieve this, consider the function skeleton below.

## def format_context(dictionary)

formatted_string = ...

retrieved_list = ...

## for i in range(len(retrieved_list))

formatted_string += f'''

Document {...}

Section Title: {...}

Lecture Title: {...}

Content: {...}

-------------------

'''

new_dictionary = ...

return new_dictionary

A variable called formatted_string is defined as an empty string where the formatted lectures will be appended consecutively.

Retrieve the list of Documents from dictionary in a variable called retrieved_list.

Inside a for-loop, continuously append the information from each Document object to obtain the desired format.

Outside the for-loop, create a variable new_dictionary representing the same dictionary as the one passed as an argument but with the context updated with the text in formatted_string.

Return this new dictionary.

Don't forget to wrap the function in a RunnableLambda or apply the @chain decorator.

After implementing the format_context(…) function, establish a new chain (chain_retrieving_improved) that incorporates it. Ensure chat_prompt_template_retrieving is formatted correctly.

Stream the Response

Okay, you're about to cross the finish line! So far, you've created a helpful Q&A chatbot that answers students' questions throughout an entire 365 course and provides the resources it has used to construct the answer. Congratulations!

Your final task is to make the chatbot more user-friendly by streaming the tokens as soon as they're generated rather than having the chatbot complete the response before it's displayed to the user. Make the corresponding changes to the code and enjoy your fully functional chatbot application!

To achieve this, substitute the invoke() method applied to the chain_retrieving_improved object with stream(). This will create a generator object stored inside result_streamed. Use a for-loop to print the generator's content consecutively, streaming the response to the user.

All right, everyone. I hope you've found this project interesting, valuable, and illuminating. I trust it allowed you to study LangChain's documentation, solidify your skills and knowledge, and learn more about this wonderful framework. You can enhance this chain with more functionalities and experiment with LangChain's integrations.

Good luck, and have fun!

## Quiz

## Question 1

Consider the Load the Course Transcript section of the project.

What is the length of the docs_list list?

25

43

49

52

## Question 2

Consider the Split the Course Transcript with MarkdownHeaderTextSplitter section of the project.

What is the length of the docs_list_md_split list?

25

43

49

52

## Question 3

Consider the Create a Chain to Correct the Course Transcript section of the project.

What does the string_list_formatted variable keep if the chain consists only of the chat prompt template and the chat objects—i.e., no string output parser enters the chain?

A list of HumanMessages

A list of AIMessages

A list of strings

A list of dictionaries

## Question 4

Consider the Split the Lectures with TokenTextSplitter section of the project.

What is the length of the docs_list_tokens_split list?

25

43

49

52

## Question 5

Consider the Create Embeddings, Vector Store, and a Retriever section of the project.

What is the significance of a lambda value of 0.7 when referring to the maximal marginal relevance search?

The search system places more emphasis on query relevance than on diversity.

The search system prioritizes diversity over relevance, ensuring the results are as different as possible.

The search system ignores relevance and focuses only on maximizing the diversity of the results.

The search system ensures that every search result is equally relevant and diverse, with no trade-off between the two factors.

## Question 6

Consider the Create the First Version of the Q&A Chatbot Chain section of the project.

Following the requirements for creating the chain_retrieving object, which would best replace (1) in the code snippet below?

chain_retrieving = (prompt_creating_question

| RunnableLambda(lambda x: (1))

| {'context': retriever,

'question': (2)}

| chat_prompt_template_retrieving

| chat

| str_output_parser)

text

content

x.text

x.content

## Question 7

Consider the Create the First Version of the Q&A Chatbot Chain section of the project.

Following the requirements for creating the chain_retrieving object, which would best replace (2) in the code snippet below?

chain_retrieving = (prompt_creating_question

| RunnableLambda(lambda x: (1))

| {'context': retriever,

'question': (2)}

| chat_prompt_template_retrieving

| chat

| str_output_parser)

Runnable()

RunnablePassthrough()

RunnableLambda()

RunnableParallel()

## Question 8

Consider the Stream the Response section of the project.

What kind of object is the result_streamed variable?

An AIMessage

A dictionary

An iterator

A generator
