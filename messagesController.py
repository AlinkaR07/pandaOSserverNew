from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timezone

from models.messageModels import messages_pydantic, messages_pydanticIN, messages
from models.status_messageModels import status_message
from models.userModels import users
from models.chatModels import chats

from langchain_community.llms import LlamaCpp
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


router = APIRouter()


@router.get("/messages", tags=["Messages"])
async def get_all_messages(order_by: str = "date_sending"):
    if order_by not in ["date_sending", "-date_sending"]:
        order_by = "date_sending"  # По умолчанию сортировка по дате отправки

    messages_query = messages.all().order_by(order_by)
    response = await messages_pydantic.from_queryset(messages_query)
    return {"status": "ok", "data": response}


@router.get("/messages/{messages_id}", tags=["Messages"])
async def get_message(messages_id: int):
    response = await messages.get_or_none(id=messages_id).prefetch_related('status_message', 'user', 'chat')
    if response:        
        response_data = {
            "id": response.id,
            "content": response.content,
            "date_sending": response.date_sending,
            "status_message_id": response.status_message.id,
            "user_id": response.user.id,
            "chat_id": response.chat.id
        }
        return {"status": "ok", "data": response_data}
    else:
        return {"status": "error", "message": "Сообщение не найдено"}
    

@router.get("/messages/chat/{chat_id}", tags=["Messages"])
async def get_message_by_chat_id(chat_id: int, order_by: str = "date_sending"):
    if order_by not in ["date_sending", "-date_sending"]:
        order_by = "date_sending"
    # Получаем сообщение из базы данных, предварительно загружая связанные объекты
    response = await messages.filter(chat_id=chat_id).prefetch_related('status_message', 'user', 'chat').order_by(order_by)
    
    if response:
        # Создаем список словарей с данными для каждого сообщения
        response_data = []
        for msg in response:
            msg_data = {
                "id": msg.id,
                "content": msg.content,
                "date_sending": msg.date_sending,
                "status_message_id": msg.status_message.id,
                "user_id": msg.user.id,
                "chat_id": msg.chat.id
            }
            response_data.append(msg_data)
        return {"status": "ok", "data": response_data}
    else:
        return {"status": "error", "message": "Сообщение не найдено"}
    

@router.get("/messages/chat/{chat_id}/last", tags=["Messages"])
async def get_last_message_by_chat_id(chat_id: int):
    # Получаем последнее сообщение из базы данных для указанного чата
    last_message = await messages.filter(chat_id=chat_id).order_by("-date_sending").first().prefetch_related('status_message', 'user', 'chat')
    
    if last_message:
        # Создаем словарь с данными для последнего сообщения
        last_message_data = {
            "id": last_message.id,
            "content": last_message.content,
            "date_sending": last_message.date_sending,
            "status_message_id": last_message.status_message.id,
            "user_id": last_message.user.id,
            "chat_id": last_message.chat.id
        }
        return {"status": "ok", "data": last_message_data}
    else:
        return {"status": "error", "message": "Сообщение не найдено"}


@router.get("/messages/status/{status_id}", tags=["Messages"])
async def get_messages_by_status_id(status_id: int):
    response = await messages.filter(status_message_id = status_id).prefetch_related('status_message', 'user', 'chat')
    if response:
        # Создаем список словарей с данными для каждого сообщения
        response_data = []
        for msg in response:
            msg_data = {
                "id": msg.id,
                "content": msg.content,
                "date_sending": msg.date_sending,
                "status_message_id": msg.status_message.id,
                "user_id": msg.user.id,
                "chat_id": msg.chat.id
            }
            response_data.append(msg_data)        
        return {"status": "ok", "data": response_data}
    else:
        return {"status": "error", "message": "Сообщение не найдено"}


class MessageDTO(BaseModel):
    user_id: int
    chat_id: int
    status_message_id: int

SYSTEM_PROMPT = "Ты — русскоязычный автоматический ассистент. Твоя цель - помогать программисту в области аналитики, программирования и тестирования кода. Ты не затрагиваешь политические темы и личностей, обходя их стороной. В ответе должен быть только текст ответа на вопрос. Если ты пишешь код, оберни его в нотацию. Если не знаешь ответ, то скажи: Я не могу ответить на ваш вопрос. Попробуйте его уточнить."
explain_role = {
    "Программист": 'Как программист, ты специалист в области программирования и разработки программного обеспечения. Твоя работа связана с написанием кода, созданием алгоритмов, тестированием и отладкой программ. Ты обладаешь глубоким пониманием языков программирования, структур данных и алгоритмов. Твоя цель - писать качественные и понятные ответы-решения: текст, программный код, алгоритмы, для решения конкретной задачи или проблемы.',
    "Программист-C++": 'Как программист, ты специалист в области программирования и разработки программного обеспечения. Твоя работа связана с написанием кода на языке програмирования C++. Ты обладаешь глубоким пониманием всех алгоритмов, фреймворков и библиотек. Твоя цель - создать эффективное и надежное программное решение на языке C++ для решения конкретной задачи или проблемы.',
    "Аналитик": 'Как аналитик, ты специалист в области написания требований к программному обеспечению. Твоя работа связана с диаграммами и спецификациями при анализе требований. Ты умеешь писать техничексое задание.'
}

# Set up LLM chain
prompt_template = """Ты - программист.Пояснение твоей роли:{explain_role}.Как программист напиши ответ на вопрос {question}, учитывая правила: {context}"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question", "explain_role"])
llm = LlamaCpp(model_path="./controller/modelsLLM/llama-2-13b-chat.ggmlv3.q8_0.bin", temperature=0.6, n_ctx=2048)
llm_chain = LLMChain(llm=llm, prompt=prompt)


@router.post("/messages/{user_id}/{chat_id}/{status_message_id}", tags=["Messages"])
async def add_message(user_id: int, chat_id: int, status_message_id: int, message_info: messages_pydanticIN):  # type: ignore
    user_fk = await users.get(id = user_id)
    chat_fk = await chats.get(id = chat_id)
    status_message_fk = await status_message.get(id = status_message_id)
    message_info = message_info.dict(exclude_unset=True)
    message_obj = await messages.create(**message_info, user = user_fk, chat = chat_fk, status_message = status_message_fk)
    
    response_message = await messages_pydantic.from_tortoise_orm(message_obj)
    return {"status": "ok", "data_message" : response_message}


@router.post("/messages_answer/{user_id}/{chat_id}/{status_message_id}", tags=["Messages"])
async def add_message(user_id: int, chat_id: int, status_message_id: int, message_info: messages_pydanticIN):  # type: ignore
        user_fk = await users.get(id = user_id)
        chat_fk = await chats.get(id = chat_id)
        status_message_fk = await status_message.get(id = status_message_id)
        context = "Пиши ответ и описание к коду на русском языке. В ответе должен быть только текст ответа на вопрос. Пиши ответ полностью, не обрывай его. Если ты пишешь код, оберни его в нотацию. Если не знаешь ответ, то напиши: Я не могу ответить на Ваш вопрос. Уточните или замените его."
        message_info = message_info.dict(exclude_unset=True)

        role = "Программист"
        if "C++" not in message_info.get("content", ""):
            if any(word in message_info.get("content", "").lower() for word in ["диаграмма", "требования", "спецификации требований", "нотация"]):
                role = "Аналитик"
            else:
                role = "Программист"
        else:
            role = "Программист-C++"

        print(role)
        response_llm = llm_chain.invoke({"context": context, "question": message_info.get("content"), "explain_role": explain_role[role]})
        current_datetime_fal = datetime.now(timezone.utc)   
        answer_obj = await messages.create(content=response_llm.get("text", ""), date_sending=current_datetime_fal, user=user_fk, chat=chat_fk, status_message=status_message_fk)
        print(response_llm)

        response_answer = await messages_pydantic.from_tortoise_orm(answer_obj)
        return {"status": "ok", "data_answer" : response_answer}



@router.put("/messages/{messages_id}", tags=["Messages"])
async def update_message(messages_id: int, update_info: messages_pydanticIN): # type: ignore
    message = await messages.get(id = messages_id)
    update_info = update_info.dict(exclude_unset=True)
    message.content = update_info['content']
    message.date_sending = update_info['date_sending']
    await message.save()
    response = await messages_pydantic.from_tortoise_orm(message)
    return {"status": "ok", "data" : response}


@router.put("/messages_answer/{messages_id}", tags=["Messages"])
async def update_message(messages_id: int): # type: ignore
    message = await messages.get(id = messages_id)
    context = "Пиши ответ и описание к коду на русском языке. В ответе должен быть только текст ответа на вопрос. Пиши ответ полностью, не обрывай его. Если ты пишешь код, оберни его в нотацию. Если не знаешь ответ, то напиши: Я не могу ответить на Ваш вопрос. Уточните или замените его."
    message_question = await messages.get(id = messages_id-1)        #сообщение с вопросом

    role = "Программист"
    print(role)
    response_llm = llm_chain.invoke({"context": context, "question": message_question.content, "explain_role": explain_role[role]})
    current_datetime_tr = datetime.now(timezone.utc) 
    message.content = response_llm.get("text", "")
    message.date_sending = current_datetime_tr
    print(response_llm)
    await message.save()
    response = await messages_pydantic.from_tortoise_orm(message)
    return {"status": "ok", "data" : response}
    
@router.put("/messages_answer_regenerate/{messages_id}", tags=["Messages"])
async def update_message(messages_id: int): # type: ignore
    message = await messages.get(id = messages_id)
    context = "Пиши ответ и описание к коду на русском языке. В ответе должен быть только текст ответа на вопрос. Пиши ответ полностью, не обрывай его. Если ты пишешь код, оберни его в нотацию. Если не знаешь ответ, то напиши: Я не могу ответить на Ваш вопрос. Уточните или замените его."
    message_question = await messages.get(id = messages_id-1)        #сообщение с вопросом

    role = "Программист"
    print(role)
    response_llm = llm_chain.invoke({"context": context, "question": message_question.content, "explain_role": explain_role[role]})
    message.content = response_llm.get("text", "")
    print(response_llm)
    await message.save()
    response = await messages_pydantic.from_tortoise_orm(message)
    return {"status": "ok", "data" : response}


@router.delete("/messages/{messages_id}", tags=["Messages"])
async def delete_message(messages_id: int):
    await messages.get(id = messages_id).delete()
    return {"status": "ok"}


# Define Pydantic model for LLM query
class LLMQuery(BaseModel):
    context: str
    question: str



# Route for LLM queries
@router.post("/llm/query_llm", tags=["Messages"])
async def llm_query(llm_query: LLMQuery):
    response = llm_chain.invoke(llm_query.dict())
    return {"status": "ok", "response": response}

