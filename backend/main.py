import logging
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import Column, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy import DateTime
from datetime import datetime
from uuid import uuid4
from typing import Optional, List
from fastapi.encoders import jsonable_encoder
import time

from modules.vanna_helper import prompt_from_template, vn 
from modules.db_selector import determine_database # Custom module
from modules.utils import get_keywords_from_db

# ──────────────────────────────────────────────────────────────────────────────
# Enable SQLAlchemy SQL logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DATABASE_URL = "postgresql+asyncpg://postgres:dsh20@localhost:5432/dsh_history"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)  # echo=True logs SQL
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# JWT configuration
SECRET_KEY = "your_super_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
users_db = {}

class UserModel(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    confirm_password = Column(String)

# ORM model
class Chat(Base):
    __tablename__ = "chat_history"
    chat_id = Column(String, primary_key=True, index=True)
    user_id = Column(String)
    title = Column(String, nullable=True)
    messages = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)  # NEW


class ContextualQuestionRequest(BaseModel):
    question: str
    chat_id: str
    context_window: Optional[int] = 3 

# Pydantic models
class QuestionRequest(BaseModel):
    question: str
    chat_id: str

class SignupRequest(BaseModel):
    username: str
    password: str
    confirm_password: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: str
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class UpdateChatTitleRequest(BaseModel):  
    title: str

# Create tables on startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with SessionLocal() as session:
        yield session

# Authentication helpers
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def authenticate_user(username: str, password: str, db: AsyncSession):
    result = await db.execute(select(UserModel).filter(UserModel.username == username))
    user = result.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None or email not in users_db:
#             raise credentials_exception
#         return users_db[email]
#     except JWTError:
#         raise credentials_exception

# Database session dependency

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username  is None:
            raise credentials_exception

        result = await db.execute(select(UserModel).filter(UserModel.username == username ))
        user = result.scalars().first()
        if user is None:
            raise credentials_exception

        return user
    except JWTError:
        raise credentials_exception


# ──────────────────────────────────────────────────────────────────────────────
# API endpoints

# 1. Signup
@app.post("/signup", status_code=201)
# async def signup(user: SignupRequest):
#     if user.password != user.confirm_password:
#         raise HTTPException(status_code=400, detail="Passwords do not match.")
    
#     if user.email in users_db:
#         raise HTTPException(status_code=400, detail="Email already registered.")
    
#     hashed = get_password_hash(user.password)
#     users_db[user.email] = UserInDB(
#         username=user.username,
#         email=user.email,
#         hashed_password=hashed
#     )
#     return {"msg": "User created successfully"}
async def signup(user: SignupRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).filter(UserModel.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists.")

    hashed_pw = get_password_hash(user.password)
    new_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    await db.commit()
    return {"msg": "User created successfully"}

# # 2. Login
# @app.post("/login", response_model=Token)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)  # username = email
#     if not user:
#         raise HTTPException(status_code=401, detail="Incorrect email or password")
#     token = create_access_token({"sub": user.email})
#     return {"access_token": token, "token_type": "bearer"}
@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# 3. Create a new chat session (title=None)
@app.post("/chats", response_model=dict)
async def create_chat(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    chat_id = str(uuid4())
    new_chat = Chat(chat_id=chat_id, user_id=current_user.username, title=None, messages=[])
    db.add(new_chat)
    await db.commit()
    return {"chat_id": chat_id}

# 4. List all chats for the current user
# @app.get("/chats", response_model=List[dict])
# async def get_chats(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
#     result = await db.execute(select(Chat).filter(Chat.user_id == current_user.username))
#     chats = result.scalars().all()
#     return [{"chat_id": c.chat_id, "title": c.title} for c in chats]

from sqlalchemy import desc

@app.get("/chats", response_model=List[dict])
async def get_chats(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Chat)
        .filter(Chat.user_id == current_user.username)
        # Optionally sort by created_at
        .order_by(desc(Chat.created_at))
    )
    chats = result.scalars().all()
    return [
        {
            "chat_id": c.chat_id,
            "title": c.title,
            "created_at": c.created_at.isoformat() if c.created_at else None
        }
        for c in chats
    ]


# 5. Get chat details
@app.get("/chats/{chat_id}", response_model=dict)
async def get_chat_details(chat_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Chat).filter(Chat.chat_id == chat_id, Chat.user_id == current_user.username)
    )
    chat = result.scalars().first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"chat_id": chat.chat_id, "title": chat.title, "messages": chat.messages or []}

# 6. Ask a question (first question sets title)
# from fastapi.encoders import jsonable_encoder

# @app.post("/ask")
# async def ask(
#     payload: QuestionRequest,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     question, chat_id = payload.question, payload.chat_id
#     database = determine_database(question)

#     # 1. Run the query
#     start_time = time.time()
#     sql_query, df = prompt_from_template(database, question)
#     exec_time = time.time() - start_time

#     # 2. Generate summary and follow-ups
#     summary = vn.generate_summary(question, df)
#     followups = vn.generate_followup_questions(question, sql_query, df, n_questions=5)

#     # 3. Fetch the chat record
#     result = await db.execute(
#         select(Chat).filter(Chat.chat_id == chat_id,
#                             Chat.user_id == current_user.username)
#     )
#     chat = result.scalars().first()
#     if not chat:
#         raise HTTPException(status_code=404, detail="Chat not found")

#     # 4. Set the title if it's the first question
#     if chat.title is None:
#         chat.title = question

#     # 5. Build the raw message dict
#     raw_msg = {
#         "question": question,
#         "sql_query": sql_query,
#         "execution_time": round(exec_time, 2),
#         # convert DataFrame to list of dicts (may contain Timestamps)
#         "results": df.to_dict(orient="records"),
#         "summary": summary,
#         "followup_questions": followups,
#     }

#     # 6. JSON‑encode the message (converts Timestamps → ISO strings, etc.)
#     safe_msg = jsonable_encoder(raw_msg)

#     # 7. Append and commit
#     chat.messages = (chat.messages or []) + [safe_msg]
#     await db.commit()

#     return safe_msg

# @app.post("/ask")
# async def ask(
#     payload: ContextualQuestionRequest,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     question, chat_id = payload.question, payload.chat_id
    
#     # 1. Fetch the chat record
#     result = await db.execute(
#         select(Chat).filter(Chat.chat_id == chat_id,
#                           Chat.user_id == current_user.username)
#     )
#     chat = result.scalars().first()
#     if not chat:
#         raise HTTPException(status_code=404, detail="Chat not found")

#     # 2. Build context from previous messages
#     def build_context(messages: list, window_size: int = payload.context_window):
#         if not messages:
#             return ""
        
#         context_parts = []
#         # Get last N exchanges (2 messages per exchange: user + assistant)
#         for msg in messages[-(window_size*2):]:
#             if msg.get("question"):
#                 context_parts.append(f"User: {msg['question']}")
#             if msg.get("summary"):
#                 context_parts.append(f"Assistant: {msg['summary']}")
#         return "\n".join(context_parts)
    
#     context = build_context(chat.messages or [])
#     contextual_question = f"Context:\n{context}\n\nQuestion: {question}"

#     database = determine_database(contextual_question,context)
#     # 4. Run the query with context
#     start_time = time.time()
#     sql_query, df = prompt_from_template(database, contextual_question)
#     exec_time = time.time() - start_time

#     # 5. Generate summary and follow-ups
#     summary = vn.generate_summary(question, df)
#     followups = vn.generate_followup_questions(question, sql_query, df, n_questions=5)

#     # 6. Set the title if it's the first question
#     if chat.title is None:
#         chat.title = question[:50] + ("..." if len(question) > 50 else "")

#     # 7. Build and store the message
#     raw_msg = {
#         "question": question,
#         "context": context,  # Store the actual context used
#         "sql_query": sql_query,
#         "execution_time": round(exec_time, 2),
#         "results": df.to_dict(orient="records"),
#         "summary": summary,
#         "followup_questions": followups,
#     }
#     safe_msg = jsonable_encoder(raw_msg)
#     chat.messages = (chat.messages or []) + [safe_msg]
#     await db.commit()

#     return safe_msg

@app.post("/ask")
async def ask(
    payload: ContextualQuestionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    question, chat_id = payload.question.strip(), payload.chat_id
    
    # 1. Fetch the chat record
    result = await db.execute(
        select(Chat).filter(Chat.chat_id == chat_id,
                            Chat.user_id == current_user.username)
    )
    chat = result.scalars().first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # 2. Check for repeated question
    for msg in reversed(chat.messages or []):
        if msg.get("question", "").strip().lower() == question.lower():
            return {
                "question": msg["question"],
                "context": msg.get("context", ""),
                "sql_query": msg.get("sql_query"),
                "execution_time": 0.0,
                "results": msg.get("results"),
                "summary": msg.get("summary"),
                "followup_questions": msg.get("followup_questions"),
                "cached": True  # Indicate reused answer
            }

    # 3. Build context from previous messages
    def build_context(messages: list, window_size: int = payload.context_window):
        if not messages:
            return ""
        context_parts = []
        for msg in messages[-(window_size*2):]:
            if msg.get("question"):
                context_parts.append(f"User: {msg['question']}")
            if msg.get("summary"):
                context_parts.append(f"Assistant: {msg['summary']}")
        return "\n".join(context_parts)

    context = build_context(chat.messages or [])
    contextual_question = f"Context:\n{context}\n\nQuestion: {question}"

    # 4. Determine DB and run query
    # database = determine_database(question, context)
    database = "snowflake"  # For testing purposes
    start_time = time.time()
    sql_query, df = prompt_from_template(database, contextual_question)
    exec_time = time.time() - start_time

    # 5. Generate summary and follow-ups
    summary = vn.generate_summary(question, df)
    followups = vn.generate_followup_questions(question, sql_query, df, n_questions=5)

    # 6. Set title if not set
    if chat.title is None:
        chat.title = question[:50] + ("..." if len(question) > 50 else "")

    # 7. Save message
    raw_msg = {
        "question": question,
        "context": context,
        "sql_query": sql_query,
        "execution_time": round(exec_time, 2),
        "results": df.to_dict(orient="records"),
        "summary": summary,
        "followup_questions": followups,
    }
    safe_msg = jsonable_encoder(raw_msg)
    chat.messages = (chat.messages or []) + [safe_msg]
    await db.commit()
    return safe_msg

# 7. Delete a chat by chat_id
@app.delete("/chats/{chat_id}", response_model=dict)
async def delete_chat(chat_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Chat).filter(Chat.chat_id == chat_id, Chat.user_id == current_user.username)
    )
    chat = result.scalars().first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    await db.delete(chat)
    await db.commit()
    return {"msg": f"Chat with id {chat_id} has been deleted successfully."}

# 8. Edit chat title
class UpdateChatTitleRequest(BaseModel):  
    title: str
@app.patch("/chats/{chat_id}/title", response_model=dict)
async def update_chat_title(
    chat_id: str,
    payload: UpdateChatTitleRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Chat).filter(Chat.chat_id == chat_id, Chat.user_id == current_user.username)
    )
    chat = result.scalars().first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    chat.title = payload.title
    await db.commit()

    return {"msg": f"Title updated to: {payload.title}"}

# from sqlalchemy import or_

# @app.get("/search", response_model=List[dict])
# async def search_chats(
#     q: str,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     # Step 1: Fetch all chats for the user
#     result = await db.execute(
#         select(Chat).filter(Chat.user_id == current_user.username)
#     )
#     chats = result.scalars().all()

#     # Step 2: Filter messages within chats
#     matching_results = []
#     for chat in chats:
#         if not chat.messages:
#             continue
#         for msg in chat.messages:
#             if q.lower() in msg.get("question", "").lower() or q.lower() in msg.get("summary", "").lower():
#                 matching_results.append({
#                     "chat_id": chat.chat_id,
#                     "question": msg.get("question"),
#                     "summary": msg.get("summary"),
#                     "execution_time": msg.get("execution_time"),
#                     "results": msg.get("results"),
#                     "followup_questions": msg.get("followup_questions")
#                 })

#     return matching_results
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)